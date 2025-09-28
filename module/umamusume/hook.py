import cv2
import time

from bot.recog.image_matcher import image_match
from module.umamusume.context import UmamusumeContext
from module.umamusume.script.cultivate_task.ai import get_operation
from module.umamusume.asset.point import *
from module.umamusume.asset.template import *
from module.umamusume.asset.template import UI_INFO
from bot.recog.ocr import ocr_line, find_similar_text
import bot.base.log as logger

log = logger.get_logger(__name__)

DOUBLE_TOGGLE = {}
DOUBLE_LAST = {}

def double_click(ctx: UmamusumeContext, first: tuple[int, int, str], second: tuple[int, int, str], key: str = "default"):
    try:
        last = DOUBLE_LAST.get(key, 0)
        if time.time() - last < 0.8:
            return
        use_second = DOUBLE_TOGGLE.get(key, False)
        x, y, desc = (second if use_second else first)
        ctx.ctrl.click(x, y, desc)
        DOUBLE_TOGGLE[key] = not use_second
        DOUBLE_LAST[key] = time.time()
    except Exception:
        try:
            DOUBLE_TOGGLE[key] = not DOUBLE_TOGGLE.get(key, False)
        except Exception:
            pass

RULES_BY_MODE = {
    "TASK_EXECUTE_MODE_TEAM_TRIALS": [
        {"type": "image", "ref": REF_HOME_GIFT, "action": lambda ctx: ctx.ctrl.click(522, 1228, "team trials resume")},
        {"type": "image", "ref": REF_TEAM_TRIALS, "action": lambda ctx: ctx.ctrl.click(106, 812, "team trials resume2")},
        {"type": "image", "ref": REF_TEAM_RACE, "action": lambda ctx: ctx.ctrl.click(351, 839, "team trials resume3")},
        {"type": "image", "ref": REF_SELECT_OPP, "action": lambda ctx: ctx.ctrl.click(73, 278, "team trials resume4")},
        {"type": "image", "ref": REF_NEXT, "action": lambda ctx: double_click(ctx, (354, 1077, "team trials next 1"), (365, 1142, "team trials next 1"), key="next")},
        {"type": "title", "ref": "Items Selected", "action": lambda ctx: ctx.ctrl.click(610, 908, "tt6")},
        {"type": "title", "ref": "Daily Sale", "action": lambda ctx: ctx.ctrl.click(0, 0, "daily sale")},
        {"type": "image", "ref": REF_SEE_RESULTS, "action": lambda ctx: ctx.ctrl.click(514, 1208, "tt7")},
        {"type": "image", "ref": REF_NEXT2, "action": lambda ctx: ctx.ctrl.click(393, 1183, "tt8")},
    ]
}


def apply_rules(ctx: UmamusumeContext, img_gray):
    mode = getattr(ctx.task.task_execute_mode, "name", None)
    if not mode:
        return False
    rules = RULES_BY_MODE.get(mode, [])
    title_raw = None
    need_title = any(r.get("type") == "title" for r in rules)
    if need_title:
        res = image_match(img_gray, UI_INFO)
        if res.find_match:
            pos = res.matched_area
            title_img = img_gray[pos[0][1] - 5:pos[1][1] + 5, pos[0][0] + 150: pos[1][0] + 405]
            title_raw = ocr_line(title_img)
    for r in rules:
        try:
            if r.get("type") == "image":
                if image_match(img_gray, r["ref"]).find_match:
                    r["action"](ctx)
                    return True
            elif r.get("type") == "title" and title_raw:
                matched = find_similar_text(title_raw, [r["ref"]], 0.8)
                if matched == r["ref"]:
                    r["action"](ctx)
                    return True
        except Exception:
            pass
    return False
    mode = getattr(ctx.task.task_execute_mode, "name", None)
    if not mode:
        return False
    rules = RULES_BY_MODE.get(mode, [])
    for r in rules:
        try:
            if r.get("type") == "image":
                if image_match(img_gray, r["ref"]).find_match:
                    r["action"](ctx)
                    return True
            elif r.get("type") == "title":
                pass
        except Exception:
            pass
    return False


def before_hook(ctx: UmamusumeContext):
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if apply_rules(ctx, img):
        return
    if image_match(img, REF_HOME_GIFT).find_match:
        if ctx.task.task_execute_mode.name == "TASK_EXECUTE_MODE_TEAM_TRIALS":
            ctx.ctrl.click(0, 0, "team trials resume 1")
        else:
            ctx.ctrl.click(552, 1082, "resume 1")
        time.sleep(1)
        img = cv2.cvtColor(ctx.ctrl.get_screen(), cv2.COLOR_BGR2GRAY)
        if image_match(img, REF_RESUME_CAREER).find_match:
            if ctx.task.task_execute_mode.name == "TASK_EXECUTE_MODE_TEAM_TRIALS":
                ctx.ctrl.click(0, 0, "team trials resume 2")
            else:
                ctx.ctrl.click(505, 908, "resume 2")
        return
    if image_match(img, REF_RESUME_CAREER).find_match:
        if ctx.task.task_execute_mode.name == "TASK_EXECUTE_MODE_TEAM_TRIALS":
            ctx.ctrl.click(0, 0, "team trials resume 2")
        else:
            ctx.ctrl.click(505, 908, "resume 2")
        return



def after_hook(ctx: UmamusumeContext):
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if apply_rules(ctx, img):
        return
    if image_match(img, BTN_SKIP).find_match:
        ctx.ctrl.click_by_point(SKIP)
    if image_match(img, BTN_SKIP_OFF).find_match:
        ctx.ctrl.click_by_point(SCENARIO_SKIP_OFF)
    if image_match(img, BTN_SKIP_SPEED_1).find_match:
        ctx.ctrl.click_by_point(SCENARIO_SKIP_SPEED_1)
    if ctx.cultivate_detail and ctx.cultivate_detail.turn_info is not None:
        if ctx.cultivate_detail.turn_info.parse_train_info_finish and ctx.cultivate_detail.turn_info.parse_main_menu_finish:
            if not ctx.cultivate_detail.turn_info.turn_info_logged:
                ctx.cultivate_detail.turn_info.log_turn_info(ctx.task.detail.scenario)
                ctx.cultivate_detail.turn_info.turn_info_logged = True
            if ctx.cultivate_detail.turn_info.turn_operation is None:
                # Only get operation if we haven't already decided on training
                # This prevents AI from overriding training decisions with race decisions
                # Also check if we're in training selection screen - don't override training decisions there
                from module.umamusume.asset.template import UI_CULTIVATE_TRAINING_SELECT
                in_training_select = image_match(img, UI_CULTIVATE_TRAINING_SELECT).find_match
                
                if not in_training_select:
                    log.info(f"🔍 Not in training selection screen - calling AI decision")
                    log.info(f"🔍 Extra race list: {ctx.cultivate_detail.extra_race_list}")
                    log.info(f"🔍 Debut race win status: {ctx.cultivate_detail.debut_race_win}")
                    ctx.cultivate_detail.turn_info.turn_operation = get_operation(ctx)
                    ctx.cultivate_detail.turn_info.turn_operation.log_turn_operation()
                else:
                    log.info("🔍 In training selection screen - skipping AI decision to avoid overriding training")




