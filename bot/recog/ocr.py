import cv2
import importlib, sys, threading
paddleocr = None
from difflib import SequenceMatcher
import bot.base.log as logger
import os
from config import CONFIG
import bot.base.gpu_utils as gpu_utils
from bot.recog.timeout_tracker import reset_timeout

log = logger.get_logger(__name__)
_paddleocr_import_lock = threading.RLock()
_USE_GPU = False
_GPU_INITIALIZED = False



def cpu_threads():
    try:
        alloc = getattr(CONFIG.bot.auto, 'cpu_alloc', None)
        return int(alloc) if alloc else os.cpu_count()
    except Exception:
        return os.cpu_count()


OCR_JP = None
OCR_CH = None
OCR_EN = None


def initialize_gpu_mode():
    global _USE_GPU, _GPU_INITIALIZED
    
    if _GPU_INITIALIZED:
        return
    
    _GPU_INITIALIZED = True
    
    try:
        gpu_config = getattr(CONFIG.bot, 'gpu', None)
        if gpu_config is None:
            _USE_GPU = False
            return
        
        gpu_enabled = getattr(gpu_config, 'enabled', 'auto')
        
        if gpu_enabled == 'false' or gpu_enabled is False:
            _USE_GPU = False
            return
        
        if gpu_enabled == 'auto' or gpu_enabled == 'true' or gpu_enabled is True:
            if gpu_utils.is_gpu_available():
                memory_fraction = float(getattr(gpu_config, 'memory_fraction', 0.5))
                device_id = int(getattr(gpu_config, 'device_id', 0))
                
                gpu_utils.set_gpu_config(memory_fraction, device_id)
                gpu_utils.configure_paddle_gpu()
                
                _USE_GPU = True
            else:
                _USE_GPU = False
        else:
            _USE_GPU = False
    
    except Exception as e:
        _USE_GPU = False

def ensure_paddleocr():
    global paddleocr
    try:
        if paddleocr is not None and 'paddleocr' in sys.modules:
            return
        if hasattr(sys, "is_finalizing") and sys.is_finalizing():
            raise RuntimeError("Interpreter finalizing; skip paddleocr import")
        with _paddleocr_import_lock:
            if paddleocr is None or 'paddleocr' not in sys.modules:
                paddleocr = importlib.import_module('paddleocr')
    except Exception as e:
        log.error(f"Failed to import paddleocr: {e}")
        raise

def init_ocr_if_needed():
    global OCR_JP, OCR_CH, OCR_EN
    
    initialize_gpu_mode()
    ensure_paddleocr()
    
    try:
        if _USE_GPU:
            if OCR_EN is None:
                OCR_EN = paddleocr.PaddleOCR(lang="en", show_log=False, use_angle_cls=False, use_gpu=True, gpu_mem=int(gpu_utils.get_gpu_memory_fraction() * 1000))
            if OCR_JP is None:
                OCR_JP = paddleocr.PaddleOCR(lang="japan", show_log=False, use_angle_cls=False, use_gpu=True, gpu_mem=int(gpu_utils.get_gpu_memory_fraction() * 1000))
            if OCR_CH is None:
                OCR_CH = paddleocr.PaddleOCR(lang="ch", show_log=False, use_angle_cls=False, use_gpu=True, gpu_mem=int(gpu_utils.get_gpu_memory_fraction() * 1000))
        else:
            os.environ['FLAGS_allocator_strategy'] = 'naive_best_fit'
            os.environ['FLAGS_fraction_of_cpu_memory_to_use'] = '0.27'
            
            if OCR_EN is None:
                OCR_EN = paddleocr.PaddleOCR(lang="en", show_log=False, use_angle_cls=False, use_gpu=False, enable_mkldnn=True, cpu_threads=cpu_threads())
            if OCR_JP is None:
                OCR_JP = paddleocr.PaddleOCR(lang="japan", show_log=False, use_angle_cls=False, use_gpu=False, enable_mkldnn=True, cpu_threads=cpu_threads())
            if OCR_CH is None:
                OCR_CH = paddleocr.PaddleOCR(lang="ch", show_log=False, use_angle_cls=False, use_gpu=False, enable_mkldnn=True, cpu_threads=cpu_threads())
    except Exception as e:
        log.error(f"Failed to initialize PaddleOCR: {e}")
        raise


def get_ocr(lang: str):
    init_ocr_if_needed()
    if lang == "en":
        return OCR_EN
    if lang == "japan":
        return OCR_JP
    if lang == "ch":
        return OCR_CH
    return OCR_EN






def reset_ocr():
    global OCR_EN, OCR_JP, OCR_CH, paddleocr
    try:
        for obj in (OCR_EN, OCR_JP, OCR_CH):
            try:
                if obj is None:
                    continue
                for attr in ("text_detector", "text_recognizer", "text_classifier"):
                    if hasattr(obj, attr):
                        try:
                            setattr(obj, attr, None)
                        except Exception:
                            pass
            except Exception:
                pass
    finally:
        OCR_EN = None
        OCR_JP = None
        OCR_CH = None
        try:
            import importlib as _il
            _il.invalidate_caches()
        except Exception:
            pass
        try:
            mods = list(sys.modules.keys())
            for name in mods:
                if name.startswith("paddleocr") or name.startswith("ppocr"):
                    try:
                        del sys.modules[name]
                    except Exception:
                        pass
        except Exception:
            pass
        try:
            _paddle = sys.modules.get("paddle")
            if _paddle is not None:
                try:
                    if hasattr(_paddle, "device") and hasattr(_paddle.device, "cuda") and hasattr(_paddle.device.cuda, "empty_cache"):
                        _paddle.device.cuda.empty_cache()
                except Exception:
                    pass
                try:
                    if hasattr(_paddle, "framework") and hasattr(_paddle.framework, "core"):
                        core = _paddle.framework.core
                        if hasattr(core, 'set_flags'):
                            core.set_flags({})
                except Exception:
                    pass
        except Exception:
            pass
        paddleocr = None
        try:
            import gc as _gc
            _gc.collect()
        except Exception:
            pass


def ocr(img, lang="en"):
    reset_timeout()
    o = get_ocr(lang)
    return o.ocr(img, cls=False)



def normalize_ocr_result(result):
    if not result:
        return []
    try:
        if isinstance(result, (list, tuple)):
            first = result[0] if len(result) > 0 else []
            if first is None:
                return []
            if isinstance(first, dict):
                return first.get("res") or first.get("data") or []
            if isinstance(first, (list, tuple)):
                return first
            return []
        if isinstance(result, dict):
            return result.get("res") or result.get("data") or []
    except Exception:
        return []
    return []

def parse_text_items(result):
    res = normalize_ocr_result(result)
    items = []
    for info in (res or []):
        try:
            if not info:
                continue
            if isinstance(info, dict):
                txt = info.get("text") or ""
                score = info.get("score") or 0
            else:
                txt = info[1][0] if len(info) > 1 else ""
                if len(info) > 1 and isinstance(info[1], (list, tuple)) and len(info[1]) > 1:
                    score = info[1][1]
                else:
                    score = 0
            if txt:
                items.append((str(txt), score))
        except Exception:
            continue
    return items

# ocr_line 文字识别图片，返回所有出现的文字

def ocr_line(img, lang="en"):
    reset_timeout()
    raw = ocr(img, lang)
    items = parse_text_items(raw)
    text = ""
    for candidate, _ in (items or []):
        text += candidate
    return text


def ocr_digits(img):
    reset_timeout()
    raw = get_ocr("en").ocr(img, cls=False)
    items = parse_text_items(raw)
    if not items:
        return ""
    best, _ = max(items, key=lambda x: x[1])
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
