import os
import cv2
import numpy as np

from bot.base.common import ImageMatchMode
from bot.base.resource import Template
import bot.base.log as logger

log = logger.get_logger(__name__)


class ImageMatchResult:
    # matched_area 匹配结果区域 [100, 100]
    matched_area = None
    # center_point 匹配结果的中心点
    center_point = None
    # find_match 匹配是否成功
    find_match: bool = False
    # score 匹配的相似得分（仅用于特征匹配）
    score: int = 0


def image_match(target, template: Template) -> ImageMatchResult:

    try:
        if template.image_match_config.match_mode == ImageMatchMode.IMAGE_MATCH_MODE_TEMPLATE_MATCH:
            if len(target.shape) == 3:
                tgt = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
            else:
                tgt = target
            area = template.image_match_config.match_area
            if area is not None:
                h, w = tgt.shape[:2]
                x1 = max(0, min(w, area.x1))
                y1 = max(0, min(h, area.y1))
                x2 = max(x1, min(w, area.x2))
                y2 = max(y1, min(h, area.y2))
                roi = tgt[y1:y2, x1:x2]
                res = template_match(roi, template, template.image_match_config.match_accuracy)
                if res.find_match:
                    cx, cy = res.center_point
                    res.center_point = (cx + x1, cy + y1)
                    (p1, p2) = res.matched_area
                    res.matched_area = ((p1[0] + x1, p1[1] + y1), (p2[0] + x1, p2[1] + y1))
                return res
            else:
                return template_match(tgt, template, template.image_match_config.match_accuracy)
        else:
            log.error("unsupported match mode")
    except Exception as e:
        log.error(f"image_match failed: {e}")
        return ImageMatchResult()


def template_match(target, template, accuracy: float = 0.86) -> ImageMatchResult:
    if target is None or target.size == 0:
        return ImageMatchResult()
    try:
        arr = getattr(template, 'template_img', None)
        if arr is None:
            arr = getattr(template, 'template_image', None)
        if arr is not None:
            try:
                th, tw = arr.shape[::]
            except Exception:
                return ImageMatchResult()
            if target.shape[0] < th or target.shape[1] < tw:
                return ImageMatchResult()
            result = cv2.matchTemplate(target, arr, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            match_result = ImageMatchResult()
            if max_val > accuracy:
                match_result.find_match = True
                match_result.center_point = (int(max_loc[0] + tw / 2), int(max_loc[1] + th / 2))
                match_result.matched_area = ((max_loc[0], max_loc[1]), (max_loc[0] + tw, max_loc[1] + th))
            else:
                match_result.find_match = False
            return match_result
        return ImageMatchResult()
    except Exception:
        return ImageMatchResult()


def compare_color_equal(p: list, target: list, tolerance: int = 10) -> bool:
    distance = np.sqrt(np.sum((np.array(target) - np.array(p)) ** 2))
    return distance < tolerance
