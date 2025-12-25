import logging
import os
import sys
import time
import threading
from collections import deque
from logging import Logger
from bot.base.user_data import base_path
from bot.base.localization import localization
import colorlog

# Fix Windows console encoding for Unicode support
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
log_path = os.path.join(base_path, "log_" + current_time + ".txt")
ENABLE_FILE_LOG = False

_last_log_time = time.time()
_log_time_lock = threading.RLock()
_registered_controller = None
_registered_executor = None
_abort_flag = threading.Event()
_monitor_thread = None
_monitor_active = False

class TaskLogHandler(logging.Handler):
    def __init__(self, capacity=1000):
        super().__init__()
        self.task_id = None
        self.buffer = {}
        self.lock = threading.RLock()
        self.capacity = capacity

    def emit(self, record):
        if hasattr(record, "task_id"):
            self.task_id = record.task_id
        if self.task_id is not None:
            if self.task_id not in self.buffer:
                self.buffer[self.task_id] = deque(maxlen=self.capacity)
            log_text = localization(self.format(record))
            with self.lock:
                self.buffer[self.task_id].append(log_text)

    def get_task_log(self, task_id):
        with self.lock:
            if task_id in self.buffer:
                logs = list(self.buffer[task_id])
            else:
                logs = []
        return logs

task_log_handler = TaskLogHandler()
fmt = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
task_log_handler.setFormatter(fmt)
task_log_handler.setLevel(logging.INFO)

class ActivityTrackingHandler(logging.Handler):
    def emit(self, record):
        global _last_log_time
        if record.levelno >= logging.INFO:
            with _log_time_lock:
                _last_log_time = time.time()

activity_handler = ActivityTrackingHandler()
activity_handler.setLevel(logging.INFO)


def get_logger(name) -> Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = colorlog.ColoredFormatter(
            fmt='%(log_color)s%(asctime)s  %(levelname)-8s [%(funcName)34s] %(filename)-20s: %(message)s',
            log_colors=log_colors_config
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(fmt)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        logger.addHandler(task_log_handler)
        logger.addHandler(activity_handler)

        fmt = logging.Formatter('%(asctime)s  %(levelname)-8s [%(funcName)34s] %(filename)-20s: %(message)s')
        if ENABLE_FILE_LOG:
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(fmt)
            file_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
    return logger

def register_controller(controller):
    global _registered_controller
    _registered_controller = controller

def register_executor(executor):
    global _registered_executor
    _registered_executor = executor

def get_abort_flag():
    return _abort_flag

def clear_abort_flag():
    _abort_flag.clear()

def _abort_all_operations():
    _abort_flag.set()
    
    if _registered_executor is not None:
        try:
            _registered_executor.close_pool()
        except Exception:
            pass
    
    try:
        from bot.recog.ocr import reset_ocr
        reset_ocr()
    except Exception:
        pass
    
    if _registered_controller is not None:
        try:
            _registered_controller.trigger_decision_reset = True
        except Exception:
            pass

def _log_inactivity_monitor():
    global _monitor_active
    log = get_logger(__name__)
    
    while _monitor_active:
        time.sleep(10)
        
        if not _monitor_active:
            break
        
        with _log_time_lock:
            inactive_duration = time.time() - _last_log_time
        
        if inactive_duration >= 60.0:
            try:
                log.warning(f"log inactivity detected for {int(inactive_duration)}s, triggering decision reset")
            except Exception:
                pass
            
            try:
                _abort_all_operations()
            except Exception:
                pass
            
            with _log_time_lock:
                _last_log_time = time.time()
            
            time.sleep(5)

def start_inactivity_monitor():
    global _monitor_thread, _monitor_active
    
    if _monitor_thread is not None and _monitor_thread.is_alive():
        return
    
    _monitor_active = True
    _monitor_thread = threading.Thread(target=_log_inactivity_monitor, daemon=True)
    _monitor_thread.start()

def stop_inactivity_monitor():
    global _monitor_active
    _monitor_active = False


