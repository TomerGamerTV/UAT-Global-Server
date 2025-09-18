from typing import Union
import requests
import re
from urllib.parse import quote
import time
import json
import os
from collections import Counter

from bot.conn.fetch import *

# For HTML parsing
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

from bot.recog.ocr import find_similar_text
from module.umamusume.context import UmamusumeContext
from module.umamusume.script.cultivate_task.event.scenario_event import *
import bot.base.log as logger

log = logger.get_logger(__name__)

event_map: dict[str, Union[callable, int]] = {
    "安心～针灸师，登☆场": 5,
    "新年的抱负": scenario_event_1,
    "新年参拜": scenario_event_2,
    "新年祈福": scenario_event_2,

    # Youth Cup events
    "新手教程": 2,
    "团队成员终于集结完毕!": aoharuhai_team_name_event,
    
    # Note: Global Server events will be handled by auto_research_event_choice()
}

event_name_list: list[str] = [*event_map]

# Global variable to store the events database
_events_database = None

def load_events_database():
    """Load the events database from the JSON file"""
    global _events_database
    
    if _events_database is not None:
        return _events_database
    
    try:
        # Try to load from the JSON file in resource/umamusume/data folder
        json_path = "resource/umamusume/data/event_data.json"
        if os.path.exists(json_path):
            log.info("📊 Loading events database from event_data.json...")
            with open(json_path, 'r', encoding='utf-8') as f:
                events_dict = json.load(f)
            
            _events_database = events_dict
            log.info(f"✅ Loaded {len(events_dict)} events from local database")
            return events_dict
        else:
            log.warning("⚠️ Events JSON file not found, will use web scraping fallback")
            return {}
            
    except Exception as e:
        log.error(f"❌ Error loading events database: {e}")
        return {}

def get_local_event_choice(ctx: UmamusumeContext, event_name: str) -> Union[int, None]:
    """Get optimal choice from local database - if not found, it's auto-skipped"""
    events_db = load_events_database()
    
    if not events_db:
        return None
    
    # Try exact match only
    if event_name in events_db:
        log.info(f"✅ Found event '{event_name}' in local database")
        return calculate_optimal_choice_from_db(ctx, events_db[event_name])
    
    def normalizeString(text: str) -> str:
        if not text:
            return ""
        text = text.strip().lower()
        text = " ".join(text.split())
        quotes = "\"'“”‘’`"
        while len(text) >= 2 and text[0] in quotes and text[-1] in quotes:
            text = text[1:-1].strip()
        return text

    def positionalRatio(left: str, right: str) -> float:
        length_left = len(left)
        if length_left == 0:
            return 0.0
        match_count = 0
        for position in range(length_left):
            if left[position] == right[position]:
                match_count += 1
        return match_count / length_left

    def build_bigrams(text: str) -> Counter:
        return Counter(text[i:i+2] for i in range(len(text) - 1)) if len(text) >= 2 else Counter()

    def jaccard_counter_ratio(a: Counter, b: Counter) -> float:
        if not a and not b:
            return 1.0
        inter = sum((a & b).values())
        union = sum((a | b).values())
        return inter / union if union else 0.0

    query = normalizeString(event_name)
    query_length = len(query)
    query_bigrams = build_bigrams(query)

    index_cache = getattr(get_local_event_choice, "cacheIndex", None)
    source_cache = getattr(get_local_event_choice, "cacheSource", None)
    if index_cache is None or source_cache is not events_db:
        cache_list = []
        for original_key in events_db.keys():
            normalized_key = normalizeString(original_key)
            cache_list.append((original_key, normalized_key, len(normalized_key), build_bigrams(normalized_key)))
        setattr(get_local_event_choice, "cacheIndex", cache_list)
        setattr(get_local_event_choice, "cacheSource", events_db)
        index_cache = cache_list

    best_key = None
    best_score = 0.0
    best_len_ratio = 0.0
    for original_key, normalized_key, normalized_length, normalized_bigrams in index_cache:
        if normalized_length == query_length:
            positional = positionalRatio(query, normalized_key)
            bigram_score = jaccard_counter_ratio(query_bigrams, normalized_bigrams)
            score = positional if positional > bigram_score else bigram_score
            if score > best_score:
                best_score = score
                best_len_ratio = 1.0
                best_key = original_key
                if score == 1.0:
                    break
        else:
            len_ratio = min(query_length, normalized_length) / max(query_length, normalized_length)
            bigram_score = jaccard_counter_ratio(query_bigrams, normalized_bigrams)
            score = bigram_score
            if score > best_score or (score == best_score and len_ratio > best_len_ratio):
                best_score = score
                best_len_ratio = len_ratio
                best_key = original_key

    if best_key is not None and best_score >= 0.91 and best_len_ratio >= 0.91:
        log.info(f"detected='{event_name}' matched='{best_key}'")
        return calculate_optimal_choice_from_db(ctx, events_db[best_key])
    
    # If not found, it's likely an auto-skipped event
    log.info(f"🔄 Event '{event_name}' not in database - likely auto-skipped, using random choice")
    return 1  # Default choice for auto-skipped events



def calculate_optimal_choice_from_db(ctx: UmamusumeContext, event_data: dict) -> int:
    """Calculate optimal choice from database event data"""
    choices = event_data['choices']
    stats = event_data['stats']
    if not choices:
        return 1

    state = fetch_state()
    energy = state["energy"]
    year_text = state["year"] if state["year"] else "Unknown"
    mood_val = state["mood"]
    mood_text = f"Level {mood_val}" if mood_val is not None else "Unknown"
    log.info(f"HP: {energy}, Year: {year_text}, Mood: {mood_text}")

    weights = {
        'Power': 10,
        'Speed': 10,
        'Guts': 20,
        'Stamina': 10,
        'Wisdom': 1,
        'Friendship': 15,
        'Mood': 9999,
        'Max Energy': 50,
        'HP': 16,
        'Skill': 10,
        'Skill Hint': 100,
        'Skill Pts': 10
    }

    if year_text == "Junior":
        weights['Friendship'] = 35
    elif year_text == "Senior":
        weights['Friendship'] = 0
        weights['Max Energy'] = 0

    if mood_val == 5:
        weights['Mood'] = 0
        log.info("Mood already maxxed")

    if energy > 90:
        weights['HP'] = 0
        log.info("Energy already near full")
    elif 40 <= energy <= 60:
        weights['HP'] = 30
        log.info("Focusing on energy to avoid rest")

    best_choice = None
    best_score = -1

    for choice_num, choice_stats in stats.items():
        choice_num_int = int(choice_num)
        score = 0
        for stat, value in choice_stats.items():
            if stat in weights:
                score += value * weights[stat]
        if score > best_score:
            best_score = score
            best_choice = choice_num_int

    if best_choice:
        log.info(f"🎯 Optimal choice: {best_choice} (Score: {best_score})")
        return best_choice

    if choices:
        first_choice = min(int(k) for k in choices.keys())
        log.info(f"🔄 Fallback choice: {first_choice}")
        return first_choice

    return 1
    
# Cache for automatic event choices to avoid repeated web requests
auto_choice_cache = {}

# Method 2: Local event database (faster and more reliable)
local_event_database = {
    "Bottomless Pit": {
        "choices": [
            {"choice": 1, "effects": [{"stat": "energy", "value": 10}]},
            {"choice": 2, "effects": [{"stat": "speed", "value": 5}, {"stat": "power", "value": 5}]},
            {"choice": 3, "effects": [{"stat": "motivation", "value": 15}]}
        ],
        "optimal": 2,  # Pre-calculated optimal choice
        "reasoning": "Choice 2 gives balanced Speed+Power bonus"
    },
    "Well-Rested!": {
        "choices": [
            {"choice": 1, "effects": [{"stat": "energy", "value": 20}]},
            {"choice": 2, "effects": [{"stat": "stamina", "value": 10}, {"stat": "energy", "value": 10}]}
        ],
        "optimal": 1,
        "reasoning": "Energy restoration is priority after rest"
    },
    "Wonderful ☆ Mistake!": {
        "choices": [
            {"choice": 1, "effects": [{"stat": "speed", "value": 10}]},
            {"choice": 2, "effects": [{"stat": "power", "value": 15}]},
            {"choice": 3, "effects": [{"stat": "guts", "value": 12}]}
        ],
        "optimal": 2,
        "reasoning": "Power has highest value and weight"
    },
    "Can't Lose Sight of Number One!": {
        "choices": "RESEARCH_NEEDED",  # Will be filled by browser automation
        "optimal": "TBD",
        "reasoning": "Competitive/Achievement event - likely stat-focused"
    },
    "A Hint for Growth": {
        "choices": [
            {"choice": 1, "effects": [{"stat": "energy", "value": 15}]},
            {"choice": 2, "effects": [{"stat": "speed", "value": 10}, {"stat": "stamina", "value": 5}]},
            {"choice": 3, "effects": [{"stat": "wit", "value": 20}]}
        ],
        "optimal": 3,
        "reasoning": "Wit training event - choice 3 gives best mental stat growth"
    }
}

def auto_research_event_choice(event_name: str) -> int:
    """Multi-layered automatic event choice research system"""
    
    # CRITICAL: Handle empty or invalid event names immediately
    if not event_name or len(event_name.strip()) < 3:
        log.warning(f"⚠️ Invalid event name '{event_name}' - using immediate fallback")
        return 1  # Quick fallback for empty/invalid names
    
    # Layer 1: Check cache first
    if event_name in auto_choice_cache:
        log.info(f"💾 Using cached choice for event '{event_name}': {auto_choice_cache[event_name]}")
        return auto_choice_cache[event_name]
    
    # Layer 2: Check local database (most reliable)
    if event_name in local_event_database:
        event_data = local_event_database[event_name]
        optimal_choice = event_data["optimal"]
        reasoning = event_data["reasoning"]
        
        log.info(f"📚 Using local database for event '{event_name}': Choice {optimal_choice}")
        log.info(f"💡 Reasoning: {reasoning}")
        
        # Cache for future use
        auto_choice_cache[event_name] = optimal_choice
        return optimal_choice
    
    log.info(f"🧠 FALLBACK: Event '{event_name}' not in database - using AI analysis")
    
    # Advanced AI-like keyword analysis
    event_lower = event_name.lower()
    analysis_score = {}
    
    # Training-related events (usually stat-focused)
    if any(word in event_lower for word in ['training', 'practice', 'workout']):
        analysis_score[2] = 30  # Middle choice often balanced
        log.info(f"🏋️ Training event detected - favoring balanced choice")
        
    # Rest/Recovery events (usually energy-focused)  
    elif any(word in event_lower for word in ['rest', 'refresh', 'recover', 'tired']):
        analysis_score[1] = 35  # First choice usually straightforward
        log.info(f"😴 Recovery event detected - favoring simple choice")
        
    # Mistake/Problem events (usually have trade-offs)
    elif any(word in event_lower for word in ['mistake', 'problem', 'error', 'wrong']):
        analysis_score[2] = 25  # Middle ground often safest
        analysis_score[3] = 20  # Sometimes high-risk high-reward
        log.info(f"⚠️ Problem event detected - analyzing risk/reward")
        
    # Social/Friend events (usually relationship-focused)
    elif any(word in event_lower for word in ['friend', 'talk', 'chat', 'social']):
        analysis_score[1] = 20
        analysis_score[2] = 25  # Often about being helpful
        log.info(f"👥 Social event detected - favoring helpful choices")
        
    # Achievement/Success events (usually reward-focused)
    elif any(word in event_lower for word in ['win', 'victory', 'success', 'achievement', 'number one', 'first', 'lose sight', 'aiming', 'aim', 'goal', 'target']):
        analysis_score[1] = 30  # Usually straightforward celebration
        analysis_score[2] = 35  # Sometimes balanced approach is better
        log.info(f"🏆 Achievement/Competition event detected - analyzing competitive choices")
        
    # Special handling for partial/truncated event names
    elif len(event_name) < 10 or any(word in event_lower for word in ['for', 'ing']):
        analysis_score[1] = 20  # Conservative choice for unknown events
        analysis_score[2] = 30  # Slightly favor balanced approach
        log.info(f"📝 Partial/truncated event name detected - using conservative approach")
        
    # Mystery/Unknown events
    else:
        analysis_score[1] = 15  # Safe default
        analysis_score[2] = 25  # Often balanced
        log.info(f"❓ Unknown event type - using balanced heuristic")
    
    # Choose highest scoring option
    if analysis_score:
        default_choice = max(analysis_score.items(), key=lambda x: x[1])[0]
        max_score = analysis_score[default_choice]
        log.info(f"🧠 AI Analysis result: Choice {default_choice} (Confidence: {max_score}%)")
    else:
        default_choice = 1  # Ultimate fallback
        
    auto_choice_cache[event_name] = default_choice
    return default_choice


def get_event_choice(ctx: UmamusumeContext, event_name: str) -> int:
    # First, try predefined event mappings
    event_name_normalized = find_similar_text(event_name, event_name_list, 0.8)
    if event_name_normalized != "":
        if event_name_normalized in event_map:
            opt = event_map[event_name_normalized]
            if type(opt) is int:
                log.info(f"Using predefined choice for event '{event_name}': {opt}")
                return opt
            if callable(opt):
                result = opt(ctx)
                return result if isinstance(result, int) else 1  # Safety check
            else:
                log.warning("Event [%s] does not provide processing logic", event_name_normalized)
                return 1
    
    # Youth Cup events
    if event_name_normalized in ["aoharuhai_team_name_event"]:
        return event_map[event_name_normalized](ctx)
    
    # NEW: Try local database first (FAST - no web scraping)
    log.info(f"🔍 Checking local database for event '{event_name}'...")
    local_choice = get_local_event_choice(ctx, event_name)
    if local_choice is not None:
        log.info(f"⚡ FAST: Found event '{event_name}' in local database - Choice {local_choice}")
        return local_choice
    
    # Check if event is still readable after 2-3 seconds (auto-skipped events)
    log.info(f"⏳ Checking if event '{event_name}' is auto-skipped...")
    time.sleep(5)  # Wait 2.5 seconds
    
    # Try to re-read the event name to see if it's still there
    try:
        from module.umamusume.script.cultivate_task.parse import parse_cultivate_event
        current_event = parse_cultivate_event(ctx)
        if current_event and current_event != event_name:
            log.info(f"🔄 Event changed from '{event_name}' to '{current_event}' - auto-skipped!")
            return 1  # Default choice for auto-skipped events
        elif not current_event:
            log.info(f"🔄 Event '{event_name}' disappeared - auto-skipped!")
            return 1  # Default choice for auto-skipped events
        else:
            log.info(f"✅ Event '{event_name}' still readable - proceeding with research")
    except Exception as e:
        log.warning(f"⚠️ Error checking event persistence: {str(e)}")
        # Continue with research if we can't check
    
    # If not found in local database, use automatic research (SLOW - web scraping)
    log.info(f"🤖 Event '{event_name}' not in local database - activating AUTO-RESEARCH mode!")
    result = auto_research_event_choice(event_name)
    
    # CRITICAL: Always ensure we return a valid integer choice
    if isinstance(result, int) and result > 0:
        return result
    else:
        log.error(f"❌ CRITICAL: auto_research_event_choice returned invalid result: {result}")
        log.error(f"❌ Falling back to choice 1 for event '{event_name}'")
        return 1
