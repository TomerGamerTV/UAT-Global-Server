import time
from datetime import datetime
import pytz

import cv2

from bot.base.task import TaskStatus, EndTaskReason
from module.umamusume.task import EndTaskReason as UEndTaskReason
from bot.recog.image_matcher import image_match
from bot.recog.ocr import ocr_line, find_similar_text
from module.umamusume.asset.point import *
from module.umamusume.asset.ui import INFO
from module.umamusume.context import UmamusumeContext
import bot.base.log as logger

log = logger.get_logger(__name__)

TITLE = [
    "Race Details",
    "Rest & Outing Confirmation",
    "Rest & Recreation",
    "Network Error",
    "Retry Challenge",
    "Earned Title",
    "Training Complete",
    "Event Skip Settings",
    "Outing Confirmation",
    "Skill Acquisition Confirmation",
    "Successfully Acquired Skill",
    "Training End Confirmation",
    "Uma Musume Details",
    "Fan Count Below Target Race Requirement",
    "Outing",
    "Skip Confirmation",
    "Rest Confirmation",
    "Race Recommendation Feature",
    "Tactics",
    "Strategy",
    "Goal Not Reached",
    "Target Fan Count Insufficient",
    "Consecutive Racing",
    "Infirmary Confirmation",
    "Gift Box",
    "Collection Successful",
    "Character Story Unlocked",
    "Target Achievement Count Insufficient",
    "Event Story Unlocked",
    "Confirm",
    "Training Value Recovery",
    "Select Training Difficulty",
    "Factor Confirmation",
    # Limited Time: Fujikiseki Show
    "New Difficulty Unlocked",
    # Aoharu Cup
    "Auto Formation",
    "Battle Confirmation",
    "Try Again",
    "Skills Learned",
    "Complete Career",
]


def script_info(ctx: UmamusumeContext):
    img = ctx.current_screen
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = image_match(img, UI_INFO)
    if result.find_match:
        pos = result.matched_area
        title_img = img[pos[0][1] - 5:pos[1][1] + 5, pos[0][0] + 150: pos[1][0] + 405]
        title_text = ocr_line(title_img)
        log.debug(title_text)
        
        # Debug: Log the original OCR text and similarity matching
        original_text = title_text
        title_text = find_similar_text(title_text, TITLE, 0.8)
        
        if title_text == "":
            log.warning(f"Unknown option box - OCR: '{original_text}'")
            # Try with lower threshold for better matching
            title_text = find_similar_text(original_text, TITLE, 0.6)
            if title_text == "":
                log.warning(f"Still no match with lower threshold - OCR: '{original_text}'")
                return
            else:
                log.info(f"✅ Found match with lower threshold: '{original_text}' -> '{title_text}'")
        else:
            log.info(f"✅ Found match: '{original_text}' -> '{title_text}'")
        if title_text == TITLE[0]:
            ctx.ctrl.click_by_point(CULTIVATE_GOAL_RACE_INTER_3)
            time.sleep(1)
        if title_text == TITLE[1]:  # "Rest & Outing Confirmation"
            log.info("🏖️ Handling Rest & Outing Confirmation")
            ctx.ctrl.click_by_point(INFO_SUMMER_REST_CONFIRM)
        if title_text == TITLE[2]:  # "Rest & Recreation"
            log.info("🏖️ Handling Rest & Recreation")
            ctx.ctrl.click_by_point(INFO_SUMMER_REST_CONFIRM)
        if title_text == TITLE[3]:
            ctx.ctrl.click_by_point(NETWORK_ERROR_CONFIRM)
        if title_text == TITLE[4]:
            if ctx.prev_ui is INFO:
                ctx.cultivate_detail.clock_used -= 1
            if ctx.cultivate_detail.clock_use_limit > ctx.cultivate_detail.clock_used:
                ctx.ctrl.click_by_point(RACE_FAIL_CONTINUE_USE_CLOCK)
                ctx.cultivate_detail.clock_used += 1
            else:
                ctx.ctrl.click_by_point(RACE_FAIL_CONTINUE_CANCEL)
            log.debug("Clock limit %s, used %s", str(ctx.cultivate_detail.clock_use_limit),
                      str(ctx.cultivate_detail.clock_used))
        if title_text == TITLE[5]:
            ctx.ctrl.click_by_point(GET_TITLE_CONFIRM)
        if title_text == TITLE[6]:
            ctx.ctrl.click_by_point(CULTIVATE_FINISH_RETURN_CONFIRM)
        if title_text == TITLE[7]:
            ctx.ctrl.click_by_point(SCENARIO_SHORTEN_SET_2)
            time.sleep(0.5)
            ctx.ctrl.click_by_point(SCENARIO_SHORTEN_CONFIRM)
        if title_text == TITLE[8]:
            ctx.ctrl.click_by_point(CULTIVATE_OPERATION_COMMON_CONFIRM)
        if title_text == TITLE[9]:
            ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN)
        if title_text == TITLE[10]:
            ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_DONE_CONFIRM)
            ctx.cultivate_detail.learn_skill_selected = False
        if title_text == TITLE[11]:
            ctx.ctrl.click_by_point(CULTIVATE_FINISH_CONFIRM_AGAIN)
        if title_text == TITLE[12]:
            ctx.ctrl.click_by_point(CULTIVATE_RESULT_CONFIRM)
        if title_text == TITLE[13]:
            ctx.ctrl.click_by_point(CULTIVATE_FAN_NOT_ENOUGH_RETURN)
        if title_text == TITLE[14]:
            ctx.ctrl.click_by_point(CULTIVATE_TRIP_WITH_FRIEND)
        if title_text == TITLE[15]:  # Skip Confirmation
            # Check if this might be a skill confirmation by looking for the template
            img = ctx.current_screen
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            from module.umamusume.asset.ui import CONFIRMATION_LEARNSKILL_BUTTON
            result = image_match(img_gray, CONFIRMATION_LEARNSKILL_BUTTON)
            log.info(f"🔍 Skip Confirmation - Template matching result: {result.find_match}")
            if result.find_match:
                # Use template matching coordinates for skill confirmation
                center_x = (result.matched_area[0][0] + result.matched_area[1][0]) // 2
                center_y = (result.matched_area[0][1] + result.matched_area[1][1]) // 2
                ctx.ctrl.click(center_x, center_y, "Skill confirmation using template matching (Skip Confirmation)")
                log.info(f"✅ Found skill confirmation button at ({center_x}, {center_y}) via Skip Confirmation")
            else:
                # Use CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN coordinates for skill confirmations
                ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN)
                log.info("⚠️ Using skill confirmation coordinates for Skip Confirmation - template not found")
        if title_text == TITLE[16]:
            ctx.ctrl.click_by_point(CULTIVATE_OPERATION_COMMON_CONFIRM)
        if title_text == TITLE[17]:
            ctx.ctrl.click_by_point(RACE_RECOMMEND_CONFIRM)
        if title_text == TITLE[18] or title_text == TITLE[19]:  # "Tactics" or "Strategy"
            date = ctx.cultivate_detail.turn_info.date
            if date != -1:
                if date <= 72:
                    ctx.ctrl.click_by_point(TACTIC_LIST[ctx.cultivate_detail.tactic_list[int((date - 1)/ 24)] - 1])
                else:
                    ctx.ctrl.click_by_point(TACTIC_LIST[ctx.cultivate_detail.tactic_list[2] - 1])
            time.sleep(0.5)
            ctx.ctrl.click_by_point(BEFORE_RACE_CHANGE_TACTIC_CONFIRM)
        if title_text == TITLE[20]:  # "Goal Not Reached" - Navigate to races to fulfill goal
            # For Oguri Cap G1 race goals, go to race selection instead of failing
            log.info("🏆 Goal Not Reached detected - navigating to races to fulfill G1 requirements")
            ctx.ctrl.click_by_point(CULTIVATE_OPERATION_COMMON_CONFIRM)  # Close the goal screen first
            time.sleep(1)
            ctx.ctrl.click_by_point(CULTIVATE_RACE)  # Navigate to race menu
            log.info("📋 Navigated to race selection to work towards G1 goals")
        if title_text == TITLE[21]:  # Target Fan Count Insufficient (was TITLE[19])
            ctx.ctrl.click_by_point(CULTIVATE_FAN_NOT_ENOUGH_RETURN)
        if title_text == TITLE[22]:  # Consecutive Racing (was TITLE[20])
            ctx.ctrl.click_by_point(CULTIVATE_TOO_MUCH_RACE_WARNING_CONFIRM)
        if title_text == TITLE[23]:  # Infirmary Confirmation (was TITLE[21])
            ctx.ctrl.click_by_point(CULTIVATE_OPERATION_COMMON_CONFIRM)
        if title_text == TITLE[24]:  # Gift Box (was TITLE[22])
            ctx.ctrl.click_by_point(RECEIVE_GIFT)
        if title_text == TITLE[25]:  # Collection Successful (was TITLE[23])
            ctx.ctrl.click_by_point(RECEIVE_GIFT_SUCCESS_CLOSE)
        if title_text == TITLE[26]:  # Character Story Unlocked (was TITLE[24])
            ctx.ctrl.click_by_point(UNLOCK_STORY_TO_HOME_PAGE)
        if title_text == TITLE[27]:  # Skill Acquisition Confirmation
            # Try to find the confirmation button using template matching first
            img = ctx.current_screen
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            from module.umamusume.asset.ui import CONFIRMATION_LEARNSKILL_BUTTON
            result = image_match(img_gray, CONFIRMATION_LEARNSKILL_BUTTON)
            log.info(f"🔍 Primary template matching result: {result.find_match}")
            if result.find_match:
                # Use template matching coordinates
                center_x = (result.matched_area[0][0] + result.matched_area[1][0]) // 2
                center_y = (result.matched_area[0][1] + result.matched_area[1][1]) // 2
                ctx.ctrl.click(center_x, center_y, "Skill confirmation using template matching")
                log.info(f"✅ Found skill confirmation button at ({center_x}, {center_y})")
            else:
                # Fallback to hardcoded coordinates
                ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN)
                log.info("⚠️ Using fallback coordinates for skill confirmation - template not found")
        if title_text == TITLE[27]:  # Successfully Acquired Skill  
            ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_DONE_CONFIRM)
            ctx.cultivate_detail.learn_skill_selected = False
        if title_text == TITLE[28]:  # Target Achievement Count Insufficient
            ctx.ctrl.click_by_point(WIN_TIMES_NOT_ENOUGH_RETURN)
        if title_text == TITLE[29]:  # Event Story Unlocked
            ctx.ctrl.click_by_point(ACTIVITY_STORY_UNLOCK_CONFIRM)
        if title_text == TITLE[30]:  # Confirm 
            # Check if this is a skill learning exit confirmation
            if ctx.cultivate_detail.learn_skill_done:
                log.info("✅ Skill learning exit confirmation - clicking confirm to exit")
                ctx.ctrl.click_by_point(CULTIVATE_OPERATION_COMMON_CONFIRM)
                # Reset the flag to prevent further skill learning loops
                ctx.cultivate_detail.learn_skill_done = False
                return
            else:
                # Check if this might be a skill confirmation by looking for the template
                img = ctx.current_screen
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                from module.umamusume.asset.ui import CONFIRMATION_LEARNSKILL_BUTTON
                result = image_match(img_gray, CONFIRMATION_LEARNSKILL_BUTTON)
                log.info(f"🔍 Template matching result: {result.find_match}")
                if result.find_match:
                    # Use template matching coordinates for skill confirmation
                    center_x = (result.matched_area[0][0] + result.matched_area[1][0]) // 2
                    center_y = (result.matched_area[0][1] + result.matched_area[1][1]) // 2
                    ctx.ctrl.click(center_x, center_y, "Skill confirmation using template matching (fallback)")
                    log.info(f"✅ Found skill confirmation button at ({center_x}, {center_y}) via fallback")
                else:
                    # Use CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN coordinates for skill confirmations
                    ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN)
                    log.info("⚠️ Using skill confirmation coordinates - template not found")
        if title_text == TITLE[31]:  # Training Value Recovery
            if not ctx.cultivate_detail.allow_recover_tp:
                ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.TP_NOT_ENOUGH)
            else:
                ctx.ctrl.click_by_point(TO_RECOVER_TP)
        if title_text == TITLE[32]:  # Select Training Difficulty
            if image_match(ctx.ctrl.get_screen(to_gray=True), REF_RECOVER_TP_1).find_match:
                ctx.ctrl.click_by_point(USE_TP_DRINK)
            elif image_match(ctx.ctrl.get_screen(to_gray=True), REF_RECOVER_TP_2).find_match:
                ctx.ctrl.click_by_point(USE_TP_DRINK_CONFIRM)
            elif image_match(ctx.ctrl.get_screen(to_gray=True), REF_RECOVER_TP_3).find_match:
                ctx.ctrl.click_by_point(USE_TP_DRINK_RESULT_CLOSE)
        if title_text == TITLE[33]:  # Factor Confirmation
            # Limited time: Fuji Kiseki Show
            # Currently seems only used here "Select cultivation difficulty, if there are others in the future, need to adjust code structure"
            beijing_tz = pytz.timezone('Asia/Shanghai')
            cutoff_time = beijing_tz.localize(datetime(2025, 7, 13, 11, 59))
            current_time_beijing = datetime.now(beijing_tz)

            if current_time_beijing <= cutoff_time:
                if ctx.task.detail.fujikiseki_show_mode == False:
                    ctx.ctrl.click(360, 300, "Select normal mode")
                else :
                    ctx.ctrl.click(360, 500, "Select Fuji Kiseki Show mode")
                    match = False
                    for i in range(5):
                        screen = ctx.ctrl.get_screen(to_gray=True)
                        if ((not image_match(screen, FUJIKISEKI_SHOW_DIFFICULTY_LOCKED).find_match) 
                            and image_match(screen, FUJIKISEKI_SHOW_DIFFICULTY[ctx.task.detail.fujikiseki_show_difficulty-1]).find_match):
                            log.info(f"Selected difficulty {ctx.task.detail.fujikiseki_show_difficulty}")
                            match = True
                            break
                        ctx.ctrl.click(675, 800, "Switch to next difficulty")
                        time.sleep(1)
                    if not match:
                        log.error(f"Selected difficulty {ctx.task.detail.fujikiseki_show_difficulty} is not unlocked yet, please play lower difficulty modes first!")
                        ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.DIFFICULTY_LOCKED)
                        return
                        
                ctx.ctrl.click(520, 1180, "")
            else:
                # Fallback for non-Fujikiseki Factor Confirmation
                ctx.ctrl.click_by_point(CULTIVATE_RESULT_DIVISOR_CONFIRM)
            
        if title_text == TITLE[34]:  # New Difficulty Unlocked
            # Limited time: Fuji Kiseki Show
            ctx.ctrl.click(360, 850, "Confirm unlock new difficulty")
        if title_text == TITLE[35]:  # Try Again
            # Handle retry/retry challenge screens with proven coordinates
            log.info("🔄 Handling 'Try Again' screen")
            ctx.ctrl.click(515, 921, "Try Again confirmation")
            log.info("✅ Clicked Try Again confirmation at (515, 921)")
        if title_text == TITLE[36]:  # Skills Learned
            # Handle skills learned confirmation with user-provided coordinates
            log.info("🎓 Handling 'Skills Learned' screen")
            ctx.ctrl.click(358, 837, "Skills Learned confirmation")
            log.info("✅ Clicked Skills Learned confirmation at (358, 837)")
            # After confirming skills learned, click back button to exit
            time.sleep(1)
            log.info("✅ Skills confirmed - clicking back button to exit skill learning")
            ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_FINISH)
        if title_text == TITLE[37]:  # Complete Career
            # Handle complete career confirmation with user-provided coordinates
            log.info("🏆 Handling 'Complete Career' screen")
            ctx.ctrl.click(511, 918, "Complete Career finish button")
            log.info("✅ Clicked Complete Career finish button at (511, 918)")
        time.sleep(1)

