"""Equipment / MCC API — in-memory data store"""
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/equipment", tags=["equipment"])

# In-memory equipment store
_equipment = [
    {"id": "MCC-01", "name": "Chiller CW Pump", "name_th": "ปั๊ม CW ชิลเลอร์", "kW": 22, "current": 38.5, "status": "running", "thermal": "36-42A", "breaker": "63A", "temp": 48, "vibration": 1.2},
    {"id": "MCC-02", "name": "AHU Fan", "name_th": "พัดลม AHU", "kW": 15, "current": 26.1, "status": "running", "thermal": "24-30A", "breaker": "40A", "temp": 42, "vibration": 0.9},
    {"id": "MCC-03", "name": "Fire Pump", "name_th": "ปั๊มดับเพลิง", "kW": 37, "current": 0, "status": "standby", "thermal": "58-68A", "breaker": "100A", "temp": 28, "vibration": 0},
    {"id": "MCC-04", "name": "Jockey Pump", "name_th": "ปั๊มจ็อคกี้", "kW": 2.2, "current": 4.1, "status": "running", "thermal": "3.8-5A", "breaker": "10A", "temp": 38, "vibration": 0.6},
    {"id": "MCC-05", "name": "Kitchen Fan", "name_th": "พัดลมครัว", "kW": 7.5, "current": 13.2, "status": "running", "thermal": "12-16A", "breaker": "25A", "temp": 44, "vibration": 1.0},
]


class EquipmentUpdate(BaseModel):
    status: Optional[str] = None
    current: Optional[float] = None
    temp: Optional[float] = None


@router.get("")
def list_equipment():
    return {"equipment": _equipment, "total": len(_equipment)}


@router.get("/{eq_id}")
def get_equipment(eq_id: str):
    for eq in _equipment:
        if eq["id"] == eq_id:
            return eq
    raise HTTPException(404, "Equipment not found")


@router.patch("/{eq_id}")
def update_equipment(eq_id: str, data: EquipmentUpdate):
    for eq in _equipment:
        if eq["id"] == eq_id:
            if data.status is not None:
                eq["status"] = data.status
                if data.status == "standby":
                    eq["current"] = 0
                    eq["vibration"] = 0
                    eq["temp"] = 28
            if data.current is not None:
                eq["current"] = data.current
            if data.temp is not None:
                eq["temp"] = data.temp
            return eq
    raise HTTPException(404, "Equipment not found")
