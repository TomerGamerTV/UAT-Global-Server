import os
import time
from typing import Dict, Any

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from bot.base.log import task_log_handler
from bot.engine import ctrl as bot_ctrl
from bot.server.protocol.task import *
from starlette.responses import FileResponse

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for manual skill notifications
manual_skill_notification_state = {
    "show": False,
    "message": "",
    "timestamp": 0,
    "confirmed": False,
    "cancelled": False
}

@server.post("/api/manual-skill-notification")
def manual_skill_notification(notification_data: Dict[str, Any]):
    """Receive manual skill purchase notification from bot"""
    global manual_skill_notification_state
    manual_skill_notification_state.update({
        "show": True,
        "message": notification_data.get("message", ""),
        "timestamp": notification_data.get("timestamp", time.time()),
        "confirmed": False,
        "cancelled": False
    })
    return {"status": "success"}

@server.get("/api/manual-skill-notification-status")
def get_manual_skill_notification_status():
    """Get current notification status for frontend polling"""
    global manual_skill_notification_state
    return manual_skill_notification_state

@server.post("/api/manual-skill-notification-confirm")
def confirm_manual_skill_notification():
    """Confirm manual skill purchase completion"""
    global manual_skill_notification_state
    manual_skill_notification_state.update({
        "show": False,
        "confirmed": True,
        "cancelled": False
    })
    return {"status": "confirmed"}

@server.post("/api/manual-skill-notification-cancel")
def cancel_manual_skill_notification():
    """Cancel manual skill purchase"""
    global manual_skill_notification_state
    manual_skill_notification_state.update({
        "show": False,
        "confirmed": False,
        "cancelled": True
    })
    return {"status": "cancelled"}


@server.post("/task")
def add_task(req: AddTaskRequest):
    bot_ctrl.add_task(req.app_name, req.task_execute_mode, req.task_type, req.task_desc,
                      req.cron_job_config, req.attachment_data)


@server.delete("/task")
def delete_task(req: DeleteTaskRequest):
    bot_ctrl.delete_task(req.task_id)


@server.get("/task")
def get_task():
    return bot_ctrl.get_task_list()

@server.get("/log/{task_id}")
def get_task_log(task_id):
    return task_log_handler.get_task_log(task_id)


@server.post("/action/bot/reset-task")
def reset_task(req: ResetTaskRequest):
    bot_ctrl.reset_task(req.task_id)


@server.post("/action/bot/start")
def start_bot():
    bot_ctrl.start()


@server.post("/action/bot/stop")
def stop_bot():
    bot_ctrl.stop()


@server.get("/")
async def get_index():
    return FileResponse('public/index.html', headers={
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    })


@server.get("/{whatever:path}")
async def get_static_files_or_404(whatever):
    # try open file for path
    file_path = os.path.join("public", whatever)
    # 设置防缓存头
    no_cache_headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    
    if os.path.isfile(file_path):
        if file_path.endswith((".js", ".mjs")):
            return FileResponse(file_path, media_type="application/javascript", headers=no_cache_headers)
        else:
            return FileResponse(file_path, headers=no_cache_headers)
    return FileResponse('public/index.html', headers=no_cache_headers)
