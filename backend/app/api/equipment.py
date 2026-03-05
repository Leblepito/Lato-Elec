from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from app.database import get_db
from app.models.equipment import Equipment, EquipmentReading
from app.middleware.auth import get_current_user
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/api/equipment", tags=["equipment"])

class EquipmentResp(BaseModel):
    id: str; name_tr: str; name_th: Optional[str]; type: str; parent_id: Optional[str]
    location: Optional[str]; specs: dict; status: str; last_reading: dict
    class Config: from_attributes = True

class ReadingCreate(BaseModel):
    equipment_id: str; reading_type: str
    value_l1: Optional[float] = None; value_l2: Optional[float] = None; value_l3: Optional[float] = None
    value_avg: Optional[float] = None; unit: Optional[str] = None

@router.get("/", response_model=List[EquipmentResp])
def list_equipment(type: Optional[str] = None, parent_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Equipment).filter(Equipment.is_active == True)
    if type: q = q.filter(Equipment.type == type)
    if parent_id: q = q.filter(Equipment.parent_id == parent_id)
    return q.order_by(Equipment.id).all()

@router.get("/tree")
def equipment_tree(db: Session = Depends(get_db)):
    """Pano ağaç şeması — tüm hiyerarşi"""
    all_eq = db.query(Equipment).filter(Equipment.is_active == True).all()
    eq_map = {e.id: {**EquipmentResp.model_validate(e).model_dump(), "children": []} for e in all_eq}
    roots = []
    for e in all_eq:
        if e.parent_id and e.parent_id in eq_map:
            eq_map[e.parent_id]["children"].append(eq_map[e.id])
        elif not e.parent_id:
            roots.append(eq_map[e.id])
    return roots

@router.get("/{equipment_id}")
def get_equipment(equipment_id: str, db: Session = Depends(get_db)):
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq: raise HTTPException(404, "Ekipman bulunamadı")
    return eq

@router.post("/readings")
def create_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    eq = db.query(Equipment).filter(Equipment.id == reading.equipment_id).first()
    if not eq: raise HTTPException(404, "Ekipman bulunamadı")
    r = EquipmentReading(**reading.model_dump())
    db.add(r)
    eq.last_reading = {"L1": reading.value_l1, "L2": reading.value_l2, "L3": reading.value_l3, "avg": reading.value_avg, "type": reading.reading_type}
    eq.last_reading_at = datetime.utcnow()
    db.commit()
    return {"status": "ok", "id": r.id}

@router.post("/readings/bulk")
def create_readings_bulk(readings: List[ReadingCreate], db: Session = Depends(get_db)):
    """Gateway'den toplu veri girişi"""
    count = 0
    for reading in readings:
        eq = db.query(Equipment).filter(Equipment.id == reading.equipment_id).first()
        if not eq: continue
        r = EquipmentReading(**reading.model_dump())
        db.add(r)
        eq.last_reading = {"L1": reading.value_l1, "L2": reading.value_l2, "L3": reading.value_l3, "avg": reading.value_avg}
        eq.last_reading_at = datetime.utcnow()
        count += 1
    db.commit()
    return {"status": "ok", "count": count}

@router.get("/{equipment_id}/readings")
def get_readings(equipment_id: str, limit: int = 100, db: Session = Depends(get_db)):
    readings = db.query(EquipmentReading).filter(EquipmentReading.equipment_id == equipment_id).order_by(EquipmentReading.recorded_at.desc()).limit(limit).all()
    return readings
