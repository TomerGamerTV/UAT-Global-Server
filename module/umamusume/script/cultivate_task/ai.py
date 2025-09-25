from module.umamusume.context import *
from module.umamusume.types import TurnOperation
import cv2
from module.umamusume.asset.template import UI_CULTIVATE_URA_RACE_1, UI_CULTIVATE_URA_RACE_2, UI_CULTIVATE_URA_RACE_3
from bot.recog.image_matcher import image_match
from bot.conn.fetch import fetch_state
log = logger.get_logger(__name__)

_race_cache = {}

def _get_races_for_period_cached(period: int) -> list[int]:
    if period not in _race_cache:
        from module.umamusume.asset.race_data import get_races_for_period
        _race_cache[period] = get_races_for_period(period)
    return _race_cache[period]


def get_operation(ctx: UmamusumeContext) -> TurnOperation | None:
    turn_operation = TurnOperation()
    if not ctx.cultivate_detail.debut_race_win:
        turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_RACE
    state = fetch_state()
    energy = state.get("energy", 0)
    mood_raw = state.get("mood")
    mood_val = mood_raw if mood_raw is not None else 4

    date_for_threshold = ctx.cultivate_detail.turn_info.date
    if date_for_threshold <= 36:
        mood_threshold = ctx.cultivate_detail.motivation_threshold_year1
    elif date_for_threshold <= 60:
        mood_threshold = ctx.cultivate_detail.motivation_threshold_year2
    else:
        mood_threshold = ctx.cultivate_detail.motivation_threshold_year3
    if (mood_raw is not None) and energy < 80 and mood_val < mood_threshold:
        log.info("mood fast path")
        turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_TRIP
        return turn_operation

    if ctx.cultivate_detail.turn_info.medic_room_available and energy <= 80:
        log.info(f"🏥 Fast path: Low stamina ({energy}) - prioritizing medic")
        turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_MEDIC
        return turn_operation
    if energy <= 48:
        log.info(f"🏥 Fast path: Low stamina ({energy}) - prioritizing rest")
        turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_REST
        return turn_operation

    cached_screen = None
    if ctx.current_screen is not None:
        cached_screen = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)

    turn_info = ctx.cultivate_detail.turn_info
    date = turn_info.date

    try:
        support_card_max = max(len(ti.support_card_info_list) for ti in turn_info.training_info_list)
    except Exception:
        support_card_max = 0

    from module.umamusume.define import SupportCardType, SupportCardFavorLevel, TrainingType
    type_map = [
        SupportCardType.SUPPORT_CARD_TYPE_SPEED,
        SupportCardType.SUPPORT_CARD_TYPE_STAMINA,
        SupportCardType.SUPPORT_CARD_TYPE_POWER,
        SupportCardType.SUPPORT_CARD_TYPE_WILL,
        SupportCardType.SUPPORT_CARD_TYPE_INTELLIGENCE,
    ]

    if date <= 24:
        w_lv1, w_lv2, w_rainbow = 0.11, 0.10, 0.01
    elif 24 < date <= 48:
        w_lv1, w_lv2, w_rainbow = 0.11, 0.10, 0.09
    elif 48 < date <= 60:
        w_lv1, w_lv2, w_rainbow = 0.11, 0.10, 0.12
    else:
        w_lv1, w_lv2, w_rainbow = 0.03, 0.05, 0.15

    training_score = [0.0, 0.0, 0.0, 0.0, 0.0]
    total_rainbows_all = 0
    for idx in range(5):
        til = turn_info.training_info_list[idx]
        target_type = type_map[idx]
        score = 0.0
        rainbow_count = 0
        for sc in (getattr(til, "support_card_info_list", []) or []):
            favor = getattr(sc, "favor", SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN)
            ctype = getattr(sc, "card_type", SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN)
            if ctype == SupportCardType.SUPPORT_CARD_TYPE_NPC:
                score += 0.05
                continue
            if ctype == SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN:
                continue
            if favor == SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                continue
            is_rb = False
            if hasattr(sc, "is_rainbow") and bool(getattr(sc, "is_rainbow")) and (ctype == target_type):
                is_rb = True
            if not is_rb and (favor in (SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_3, SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_4) and ctype == target_type):
                is_rb = True
            if is_rb:
                rainbow_count += 1
                score += w_rainbow
                continue
            if favor in (SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_3, SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_4):
                continue
            if favor == SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_1:
                score += w_lv1
            elif favor == SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_2:
                score += w_lv2
        total_rainbows_all += rainbow_count
        training_score[idx] = score

    log.debug("Overall training score: " + str(training_score))

    rainbow_counts = [0, 0, 0, 0, 0]
    for idx in range(5):
        til = turn_info.training_info_list[idx]
        target_type = type_map[idx]
        rc = 0
        for sc in (getattr(til, "support_card_info_list", []) or []):
            favor = getattr(sc, "favor", SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN)
            ctype = getattr(sc, "card_type", SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN)
            is_rb = False
            if hasattr(sc, "is_rainbow") and bool(getattr(sc, "is_rainbow")) and (ctype == target_type):
                is_rb = True
            if not is_rb and (favor in (SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_3, SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_4) and ctype == target_type):
                is_rb = True
            if is_rb:
                rc += 1
        rainbow_counts[idx] = rc

    if ctx.cultivate_detail.debut_race_win:
        from module.umamusume.asset.race_data import get_races_for_period
        ura_race_id = None
        if ctx.task.detail.scenario == ScenarioType.SCENARIO_TYPE_URA:
            date_now = ctx.cultivate_detail.turn_info.date
            if 73 <= date_now <= 75:
                ura_race_id = 2381
            elif 76 <= date_now <= 78:
                ura_race_id = 2382
            elif 79 <= date_now <= 99:
                ura_race_id = 2385
            if ura_race_id and cached_screen is not None:
                ura_race_available = False
                if 73 <= date_now <= 75:
                    ura_race_available = image_match(cached_screen, UI_CULTIVATE_URA_RACE_1).find_match
                elif 76 <= date_now <= 78:
                    ura_race_available = image_match(cached_screen, UI_CULTIVATE_URA_RACE_2).find_match
                elif 79 <= date_now <= 99:
                    ura_race_available = image_match(cached_screen, UI_CULTIVATE_URA_RACE_3).find_match
                if not ura_race_available:
                    ura_race_id = None
            elif ura_race_id and cached_screen is None:
                ura_race_id = None
        if ura_race_id:
            log.info(f"🏆 Detected URA championship race: {ura_race_id} at date {date}")
            medic = False
            if ctx.cultivate_detail.turn_info.medic_room_available and energy <= 85:
                medic = True
            trip = False
            if not ctx.cultivate_detail.turn_info.medic_room_available and (
                (ctx.cultivate_detail.turn_info.date <= 36 and mood_val < ctx.cultivate_detail.motivation_threshold_year1 and energy < 90 and not support_card_max >= 2)
                or (40 < ctx.cultivate_detail.turn_info.date <= 60 and mood_val < ctx.cultivate_detail.motivation_threshold_year2 and energy < 90)
                or (64 < ctx.cultivate_detail.turn_info.date <= 99 and mood_val < ctx.cultivate_detail.motivation_threshold_year3 and energy < 90)
            ):
                try:
                    best_idx = max(range(5), key=lambda i: training_score[i]) if len(training_score) == 5 else 0
                    best_score = training_score[best_idx] if len(training_score) == 5 else 0.0
                except Exception:
                    best_score = 0.0
                if best_score > 0.3:
                    log.info("No recreation as good training detected")
                    trip = False
                else:
                    trip = True
            rest = False
            if energy <= 48:
                rest = True
            elif (ctx.cultivate_detail.turn_info.date == 36 or ctx.cultivate_detail.turn_info.date == 60) and energy < 65:
                rest = True
            if rest:
                log.info(f"🏥 Low stamina ({energy}) - prioritizing rest over URA race")
                turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_REST
                return turn_operation
            elif trip:
                log.info(f"🏖️ Low stamina/motivation - prioritizing trip over URA race")
                turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_TRIP
                return turn_operation
            elif medic:
                log.info(f"🏥 Low stamina - prioritizing medic over URA race")
                turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_MEDIC
                return turn_operation
            else:
                log.info(f"🏆 Proceeding with URA race - stamina: {energy}")
                turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_RACE
                turn_operation.race_id = ura_race_id
                return turn_operation
        available_races = _get_races_for_period_cached(ctx.cultivate_detail.turn_info.date)
        extra_race_this_turn = [race_id for race_id in ctx.cultivate_detail.extra_race_list if race_id in available_races]
        if len(extra_race_this_turn) != 0:
            turn_operation.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_RACE
            turn_operation.race_id = extra_race_this_turn[0]
            return turn_operation

    medic = False
    if ctx.cultivate_detail.turn_info.medic_room_available and energy <= 85:
        medic = True

    trip = False
    if not ctx.cultivate_detail.turn_info.medic_room_available and (ctx.cultivate_detail.turn_info.date <= 36 and mood_val < ctx.cultivate_detail.motivation_threshold_year1 and energy < 90 and not support_card_max >= 3
                                                                    or 40 < ctx.cultivate_detail.turn_info.date <= 60 and mood_val < ctx.cultivate_detail.motivation_threshold_year2 and energy < 90
                                                                    or 64 < ctx.cultivate_detail.turn_info.date <= 99 and mood_val < ctx.cultivate_detail.motivation_threshold_year3 and energy < 90):
        try:
            best_idx = max(range(5), key=lambda i: training_score[i]) if len(training_score) == 5 else 0
            best_score = training_score[best_idx] if len(training_score) == 5 else 0.0
        except Exception:
            best_score = 0.0
        if best_score > 0.3:
            log.info("No recreation as good training detected")
            trip = False
        else:
            trip = True

    rest = False
    if energy <= 48:
        rest = True
    elif (ctx.cultivate_detail.turn_info.date == 36 or ctx.cultivate_detail.turn_info.date == 60) and energy < 65:
        rest = True

    expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN

    if medic and expect_operation_type is TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN:
        expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_MEDIC
    if trip and expect_operation_type is TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN:
        expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_TRIP
    if rest and expect_operation_type is TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN:
        expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_REST

    if expect_operation_type is TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN:
        date_num = ctx.cultivate_detail.turn_info.date
        if date_num in (59, 60):
            rainbow = 0
            try:
                best_idx = max(range(5), key=lambda i: training_score[i]) if len(training_score) == 5 else 0
                til = ctx.cultivate_detail.turn_info.training_info_list[best_idx]
                target_type = type_map[best_idx]
                for sc in (getattr(til, "support_card_info_list", []) or []):
                    ctype = getattr(sc, "card_type", None)
                    favor = getattr(sc, "favor", None)
                    is_rb = False
                    if hasattr(sc, "is_rainbow") and bool(getattr(sc, "is_rainbow")) and (ctype == target_type):
                        is_rb = True
                    if not is_rb and (ctype == target_type and favor in (SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_3, SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_4)):
                        is_rb = True
                    if is_rb:
                        rainbow += 1
            except Exception:
                rainbow = 0
            if rainbow < 2:
                log.info("Low rainbow count conserving energy for summer")
                if energy < 60:
                    expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_REST
                else:
                    expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_TRAINING
                    turn_operation.training_type = TrainingType.TRAINING_TYPE_INTELLIGENCE

    if expect_operation_type is TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN:
        expect_operation_type = TurnOperationType.TURN_OPERATION_TYPE_TRAINING

    if turn_operation.turn_operation_type != TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN:
        turn_operation.turn_operation_type_replace = expect_operation_type
    else:
        turn_operation.turn_operation_type = expect_operation_type
    return turn_operation
