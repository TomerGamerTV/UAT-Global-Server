import cv2
import paddleocr
from difflib import SequenceMatcher
import bot.base.log as logger
import os
from config import CONFIG

log = logger.get_logger(__name__)


def cpu_threads():
    try:
        alloc = getattr(CONFIG.bot.auto, 'cpu_alloc', None)
        return int(alloc) if alloc else os.cpu_count()
    except Exception:
        return os.cpu_count()


OCR_JP = paddleocr.PaddleOCR(lang="japan", show_log=False, use_angle_cls=False, use_gpu=False, enable_mkldnn=True, cpu_threads=cpu_threads())
OCR_CH = paddleocr.PaddleOCR(lang="ch", show_log=False, use_angle_cls=False, use_gpu=False, enable_mkldnn=True, cpu_threads=cpu_threads())
OCR_EN = paddleocr.PaddleOCR(lang="en", show_log=False, use_angle_cls=False, use_gpu=False, enable_mkldnn=True, cpu_threads=cpu_threads())


# ocr 文字识别图片
def ocr(img, lang="en"):
    if lang == "en":
        return OCR_EN.ocr(img, cls=False)
    if lang == "japan":
        return OCR_JP.ocr(img, cls=False)
    if lang == "ch":
        return OCR_CH.ocr(img, cls=False)


# ocr_line 文字识别图片，返回所有出现的文字

def ocr_line(img, lang="en"):
    ocr_result = ocr(img, lang)
    text = ""
    ocr_result = ocr_result[0] if ocr_result else []
    for text_info in ocr_result:
        if len(text_info) > 0:
            text += text_info[1][0]
    return text

# ocr_digits 限制只识别数字，可以提升数字识别的准确度

def ocr_digits(img):
    res = OCR_EN.ocr(img, cls=False)
    res = res[0] if res else []
    digits = [(info[1][0], info[1][1]) for info in res]
    if not digits:
        return ""
    best, _ = max(digits, key=lambda x: x[1])
    return best

# find_text_pos 查找目标文字在图片中的位置
def find_text_pos(ocr_result, target):
    threshold = 0.6
    result = None
    for text_info in ocr_result:
        if len(text_info) > 0:
            s = SequenceMatcher(None, target, text_info[0][1][0])
            if s.ratio() > threshold:
                result = text_info[0]
                threshold = s.ratio()
    return result


def find_similar_text(target_text, ref_text_list, threshold=0):
    result = ""
    for ref_text in ref_text_list:
        s = SequenceMatcher(None, target_text, ref_text)
        if s.ratio() > threshold:
            result = ref_text
            threshold = s.ratio()
    return result
