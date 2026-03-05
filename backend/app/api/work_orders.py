from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from app.database import get_db
from app.models.work_order import WorkOrder
from app.middleware.auth import get_current_user
from app.models.user import User
from datetime import datetime
import random, string

router = APIRouter(prefix="/api/workorders", tags=["workorders"])

def gen_wo_id():
    return f"WO-{datetime.now().year}-{random.randint(1000,9999)}"

class WOCreate(BaseModel):
    equipment_id: Optional[str] = None
    title_tr: str; title_th: Optional[str] = None
    priority: str = "medium"; assigned_to: Optional[str] = None
    deadline: Optional[str] = None; loto_required: bool = False

class WOUpdate(BaseModel):
    status: Optional[str] = None; notes: Optional[str] = None; actual_hours: Optional[float] = None

@router.get("/")
def list_work_orders(status: Optional[str] = None, priority: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(WorkOrder)
    if status: q = q.filter(WorkOrder.status == status)
    if priority: q = q.filter(WorkOrder.priority == priority)
    return q.order_by(WorkOrder.created_at.desc()).limit(50).all()

@router.post("/")
def create_work_order(wo: WOCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_wo = WorkOrder(id=gen_wo_id(), equipment_id=wo.equipment_id, title_tr=wo.title_tr, title_th=wo.title_th or wo.title_tr, priority=wo.priority, created_by=user.id, loto_required=wo.loto_required)
    db.add(new_wo); db.commit(); db.refresh(new_wo)
    return new_wo

@router.get("/{wo_id}")
def get_work_order(wo_id: str, db: Session = Depends(get_db)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo: raise HTTPException(404, "İş emri bulunamadı")
    return wo

@router.patch("/{wo_id}")
def update_work_order(wo_id: str, update: WOUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo: raise HTTPException(404, "İş emri bulunamadı")
    if update.status:
        wo.status = update.status
        if update.status == "accepted": wo.accepted_at = datetime.utcnow()
        if update.status == "in_progress": wo.started_at = datetime.utcnow()
        if update.status == "completed": wo.completed_at = datetime.utcnow()
    if update.notes: wo.notes = update.notes
    if update.actual_hours: wo.actual_hours = update.actual_hours
    wo.updated_at = datetime.utcnow()
    db.commit()
    return wo

@router.post("/{wo_id}/complete")
def complete_work_order(wo_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo: raise HTTPException(404)
    wo.status = "completed"; wo.completed_at = datetime.utcnow(); wo.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "completed", "id": wo_id}
