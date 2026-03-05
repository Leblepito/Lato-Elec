"""Work Orders API — in-memory store"""
import random
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/workorders", tags=["workorders"])

_workorders = [
    {"id": "WO-341", "equipment": "PP-01", "task": "ตรวจเทอร์มอลรีเลย์", "task_tr": "Termik Röle Kontrol", "priority": "high", "status": "open", "assignee": "สมชาย", "created_at": "2026-03-04T09:00:00"},
    {"id": "WO-342", "equipment": "MDB", "task": "สแกนเทอร์โมกราฟี Q1", "task_tr": "Termografi Tarama", "priority": "medium", "status": "in_progress", "assignee": "ประเสริฐ", "created_at": "2026-03-04T10:00:00"},
]


class CreateWO(BaseModel):
    equipment: str
    task: str
    assignee: str = ""
    priority: str = "medium"


class UpdateWO(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None


@router.get("")
def list_workorders(status: Optional[str] = None):
    if status:
        filtered = [w for w in _workorders if w["status"] == status]
    else:
        filtered = _workorders
    return {"workorders": filtered, "total": len(filtered)}


@router.post("")
def create_workorder(wo: CreateWO):
    new_wo = {
        "id": f"WO-{random.randint(400, 999)}",
        "equipment": wo.equipment,
        "task": wo.task,
        "task_tr": wo.task,
        "priority": wo.priority,
        "status": "open",
        "assignee": wo.assignee,
        "created_at": datetime.now().isoformat(),
    }
    _workorders.insert(0, new_wo)
    return new_wo


@router.patch("/{wo_id}")
def update_workorder(wo_id: str, data: UpdateWO):
    for wo in _workorders:
        if wo["id"] == wo_id:
            if data.status is not None:
                wo["status"] = data.status
            if data.priority is not None:
                wo["priority"] = data.priority
            return wo
    raise HTTPException(404, "Work order not found")
