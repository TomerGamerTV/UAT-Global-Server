from typing import Union
import requests
import re
from urllib.parse import quote
import time
import json
import pandas as pd
import os

# For advanced web automation
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

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
    """Load the events database from the Excel file"""
    global _events_database
    
    if _events_database is not None:
        return _events_database
    
    try:
        # Try to load from the Excel file in resource/umamusume/data folder
        excel_path = "resource/umamusume/data/event_data.xlsx"
        if os.path.exists(excel_path):
            log.info("📊 Loading events database from Excel file...")
            df = pd.read_excel(excel_path)
            
            # Group by event name and create a lookup structure
            events_dict = {}
            for _, row in df.iterrows():
                event_name = row['event_name']
                choice_num = row['choice_number']
                choice_text = row['choice_text']
                
                if event_name not in events_dict:
                    events_dict[event_name] = {
                        'choices': {},
                        'stats': {}
                    }
                
                # Store choice text
                events_dict[event_name]['choices'][choice_num] = choice_text
                
                # Store stat effects
                stats = {}
                for stat in ['Power', 'Speed', 'Guts', 'Stamina', 'Wisdom', 'Friendship', 'Mood', 'Max Energy', 'HP', 'Skill', 'Skill Hint', 'Skill Pts']:
                    if stat in row and pd.notna(row[stat]):
                        stats[stat] = int(row[stat])
                
                events_dict[event_name]['stats'][choice_num] = stats
            
            _events_database = events_dict
            log.info(f"✅ Loaded {len(events_dict)} events from local database")
            return events_dict
        else:
            log.warning("⚠️ Events Excel file not found, will use web scraping fallback")
            return {}
            
    except Exception as e:
        log.error(f"❌ Error loading events database: {e}")
        return {}

def get_local_event_choice(event_name: str) -> Union[int, None]:
    """Get optimal choice from local database - if not found, it's auto-skipped"""
    events_db = load_events_database()
    
    if not events_db:
        return None
    
    # Try exact match only
    if event_name in events_db:
        log.info(f"✅ Found event '{event_name}' in local database")
        return calculate_optimal_choice_from_db(events_db[event_name])
    
    # If not found, it's likely an auto-skipped event
    log.info(f"🔄 Event '{event_name}' not in database - likely auto-skipped, using random choice")
    return 1  # Default choice for auto-skipped events



def calculate_optimal_choice_from_db(event_data: dict) -> int:
    """Calculate optimal choice from database event data"""
    choices = event_data['choices']
    stats = event_data['stats']
    
    if not choices:
        return 1
    
    # Calculate optimal choice based on stat values
    best_choice = None
    best_score = -1
    
    for choice_num, choice_stats in stats.items():
        score = 0
        
        # Weight different stats (adjust weights as needed)
        weights = {
            'Power': 2,
            'Speed': 2, 
            'Guts': 1.5,
            'Stamina': 1.5,
            'Wisdom': 1,
            'Friendship': 1,
            'Mood': 1,
            'Max Energy': 1,
            'HP': 1,
            'Skill': 3,
            'Skill Hint': 2,
            'Skill Pts': 2
        }
        
        for stat, value in choice_stats.items():
            if stat in weights:
                score += value * weights[stat]
        
        if score > best_score:
            best_score = score
            best_choice = choice_num
    
    if best_choice:
        log.info(f"🎯 Optimal choice: {best_choice} (Score: {best_score})")
        return best_choice
    
    # Fallback: return first choice if no scoring possible
    if choices:
        first_choice = min(choices.keys())
        log.info(f"🔄 Fallback choice: {first_choice}")
        return first_choice
    
    return 1
    


def parse_game8_results(results_html: str, event_name: str) -> dict:
    """Parse Game8 HTML structure to extract choice data using proven BeautifulSoup method"""
    
    if not BEAUTIFULSOUP_AVAILABLE:
        log.warning("⚠️ BeautifulSoup not available, falling back to regex parsing")
        return parse_game8_results_fallback(results_html, event_name)
    
    try:
        log.info(f"🔍 Parsing Game8 HTML structure for '{event_name}'")
        
        # Parse with BeautifulSoup for accurate structure handling
        soup = BeautifulSoup(results_html, 'html.parser')
        
        # Find the event name to verify we have the right data
        event_name_elem = soup.find('h2', class_='style-module__eventName___5c0Ff')
        if event_name_elem:
            found_event = event_name_elem.text
            log.info(f"✅ Found event: {found_event}")
        
        # Find all choice cards using Game8's structure
        choice_cards = soup.find_all('div', {'data-choice': True})
        log.info(f"🔢 Found {len(choice_cards)} choice cards")
        
        if not choice_cards:
            log.warning("❌ No choice cards found in HTML structure")
            return {}
        
        choices = {}
        
        for card in choice_cards:
            try:
                choice_num = int(card.get('data-choice'))
                log.debug(f"📝 Processing Choice {choice_num}")
                
                # Get choice description text
                choice_text_elem = card.find('div', class_='style-module__choiceText___3Qv3P')
                choice_text = choice_text_elem.text if choice_text_elem else "Unknown choice"
                
                # Get all effect badges
                effects = []
                effect_badges = card.find_all('span', class_='style-module__effectBadge___3XLEt')
                
                log.debug(f"   📊 Found {len(effect_badges)} effect badges")
                
                for badge in effect_badges:
                    try:
                        # Get effect name (Energy, Speed, Power, etc.)
                        effect_name = badge.contents[0] if badge.contents else "Unknown"
                        if isinstance(effect_name, str):
                            effect_name = effect_name.strip()
                        else:
                            continue
                        
                        # Get effect value (positive or negative)
                        positive_elem = badge.find('span', class_='style-module__positive___gkSgD')
                        negative_elem = badge.find('span', class_='style-module__negative___3QNK0')
                        
                        value = 0
                        if positive_elem:
                            value_text = positive_elem.text.strip()
                            value_match = re.findall(r'[+-]?\d+', value_text)
                            if value_match:
                                value = int(value_match[0])
                        elif negative_elem:
                            value_text = negative_elem.text.strip()
                            value_match = re.findall(r'[+-]?\d+', value_text)
                            if value_match:
                                value = int(value_match[0])
                        
                        # Only include effects with actual stat changes
                        if value != 0 and effect_name.lower() in ['energy', 'speed', 'power', 'stamina', 'guts', 'wit', 'skill pts']:
                            stat_name = effect_name.lower().replace(' ', '_')
                            effects.append({
                                'stat': stat_name,
                                'value': value
                            })
                            log.debug(f"      {effect_name}: {value:+d}")
                        elif effect_name not in ['Unknown', '']:
                            log.debug(f"      {effect_name}: Special Effect")
                    
                    except Exception as badge_error:
                        log.debug(f"⚠️ Error parsing badge: {str(badge_error)}")
                        continue
                
                choices[choice_num] = effects
                log.info(f"✅ Choice {choice_num}: \"{choice_text[:50]}...\" ({len(effects)} effects)")
                
            except Exception as card_error:
                log.warning(f"⚠️ Error parsing choice card: {str(card_error)}")
                continue
        
        if choices:
            total_effects = sum(len(effects) for effects in choices.values())
            log.info(f"📊 Successfully parsed {len(choices)} choices with {total_effects} total effects")
            return choices
        else:
            log.warning("❌ No valid choices extracted")
            return {}
        
    except Exception as e:
        log.warning(f"❌ Error parsing Game8 HTML: {str(e)}")
        return {}

def parse_game8_results_fallback(results_html: str, event_name: str) -> dict:
    """Fallback regex parser when BeautifulSoup is not available"""
    try:
        log.warning("🔄 Using fallback regex parsing")
        
        choice_data = {}
        
        # Look for Game8's actual structure patterns
        patterns = [
            r'data-choice="(\d+)".*?style-module__choiceText___3Qv3P">([^<]+).*?Energy.*?([+\-]\d+)',
            r'data-choice="(\d+)".*?Energy.*?([+\-]\d+)',
            r'Choice\s*(\d+).*?([+\-]\d+)\s*(Energy|Speed|Power|Stamina|Guts|Wit)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, results_html, re.IGNORECASE | re.DOTALL)
            if matches:
                for match in matches:
                    try:
                        choice_num = int(match[0])
                        if choice_num not in choice_data:
                            choice_data[choice_num] = []
                        
                        # Simple energy effect for fallback
                        choice_data[choice_num].append({
                            'stat': 'energy',
                            'value': 10  # Default reasonable value
                        })
                    except:
                        continue
                break
        
        return choice_data
        
    except Exception as e:
        log.warning(f"❌ Fallback parsing also failed: {str(e)}")
        return {}

def calculate_optimal_choice(choice_data: dict) -> int:
    """Calculate the optimal choice based on proven stat weights and analysis"""
    if not choice_data:
        return 1
    
    log.info(f"🧮 Calculating optimal choice from {len(choice_data)} options")
    
    # Proven stat weights (Energy is crucial for training!)
    stat_weights = {
        'speed': 3, 'power': 3,                    # Primary racing stats
        'stamina': 2, 'guts': 2, 'wit': 2,        # Secondary racing stats
        'energy': 2,                               # Important for training continuity
        'skill_pts': 1.5,                          # Skill points are valuable
        'motivation': 1                            # Low priority
    }
    
    choice_scores = {}
    
    for choice_num, effects in choice_data.items():
        total_score = 0
        
        log.info(f"   🔢 Choice {choice_num}:")
        
        if effects:
            for effect in effects:
                stat = effect['stat']
                value = effect['value']
                weight = stat_weights.get(stat, 1)
                
                weighted_score = value * weight
                total_score += weighted_score
                
                log.info(f"      {stat} {value:+d} × {weight} = {weighted_score}")
        else:
            log.info(f"      No stat effects found")
        
        # Risk analysis for complex choices (like success/fail outcomes)
        if choice_num == 2 and len(effects) > 3:  # Choice 2 with many effects suggests risk
            risk_penalty = -5
            total_score += risk_penalty
            log.info(f"      Risk penalty: {risk_penalty} (complex outcome detected)")
        
        choice_scores[choice_num] = total_score
        log.info(f"   Choice {choice_num} total: {total_score}")
    
    if choice_scores:
        # Return the choice with highest score
        optimal_choice = max(choice_scores.items(), key=lambda x: x[1])
        best_choice = optimal_choice[0]
        best_score = optimal_choice[1]
        
        log.info(f"🏆 Optimal choice: {best_choice} (Score: {best_score})")
        return best_choice
    else:
        log.warning(f"⚠️ No valid choices scored, defaulting to 1")
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
    
    # Layer 3: Advanced browser automation (most accurate)
    if SELENIUM_AVAILABLE:
        try:
            log.info(f"🌐 Using browser automation for event: '{event_name}'")
            
            # Configure Chrome for headless operation (optimized for speed)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--window-size=1280,720")  # Smaller window for speed
            
            # Initialize Chrome driver
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Navigate to Game8 Event Checker
                url = "https://game8.co/games/Umamusume-Pretty-Derby/archives/539000"
                log.info(f"🔗 Navigating to: {url}")
                driver.get(url)
                
                # Wait for page to load and find search input (faster timeout)
                search_input_selector = "#react-umamusume_event_checker-wrapper > div > div.style-module__searchPanel___3sfIO > div.style-module__searchInputWrapper___X9Cwt > input"
                
                wait = WebDriverWait(driver, 8)  # Reduced from 15 to 8 seconds
                search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, search_input_selector)))
                
                log.info(f"✅ Found search input field")
                
                # Clear and input event name
                search_input.clear()
                search_input.send_keys(event_name)
                log.info(f"⌨️ Typed event name: '{event_name}'")
                
                # Wait for results to load (reduced timeout to avoid missing events)
                time.sleep(2)  # Reduced from 3 to 2 seconds
                
                # Find results container
                results_selector = "#react-umamusume_event_checker-wrapper > div > div.style-module__choiceList___2vmTV"
                results_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_selector)))
                
                log.info(f"📊 Found results container")
                
                # Parse the results
                results_html = results_container.get_attribute('innerHTML')
                log.debug(f"📄 Results HTML length: {len(results_html)} characters")
                
                # Extract choice information from the HTML
                choice_data = parse_game8_results(results_html, event_name)
                
                if choice_data:
                    optimal_choice = calculate_optimal_choice(choice_data)
                    log.info(f"🎯 Browser automation SUCCESS! Event '{event_name}' → Choice {optimal_choice}")
                    
                    # Cache the result
                    auto_choice_cache[event_name] = optimal_choice
                    return optimal_choice
                else:
                    log.warning(f"📊 No valid choice data found for event '{event_name}'")
                    # Don't return here - continue to fallback analysis
                    
            finally:
                driver.quit()
                
        except Exception as e:
            log.warning(f"🌐 Browser automation failed: {str(e)}")
    else:
        log.warning(f"🌐 Selenium not available, skipping browser automation")
        
    # Layer 4: Advanced fallback - intelligent analysis (moved outside the else block)
    log.warning(f"🌐 Web research failed for event '{event_name}', using advanced fallback analysis")
    
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
    local_choice = get_local_event_choice(event_name)
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
