import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(String(50), primary_key=True)
    name_tr = Column(String(255), nullable=False)
    name_th = Column(String(255))
    type = Column(String(50), nullable=False)
    parent_id = Column(String(50), ForeignKey("equipment.id"))
    location = Column(String(255))
    specs = Column(JSON, default={})
    status = Column(String(30), default="standby")
    last_reading = Column(JSON, default={})
    last_reading_at = Column(DateTime(timezone=True))
    maintenance_interval_days = Column(Integer, default=90)
    last_maintenance_at = Column(DateTime(timezone=True))
    next_maintenance_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    children = relationship("Equipment", backref="parent", remote_side=[id], foreign_keys=[parent_id])
    readings = relationship("EquipmentReading", back_populates="equipment")
    work_orders = relationship("WorkOrder", back_populates="equipment")

class EquipmentReading(Base):
    __tablename__ = "equipment_readings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(String(50), ForeignKey("equipment.id"), nullable=False)
    reading_type = Column(String(50), nullable=False)
    value_l1 = Column(Float)
    value_l2 = Column(Float)
    value_l3 = Column(Float)
    value_avg = Column(Float)
    unit = Column(String(20))
    metadata = Column(JSON, default={})
    recorded_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    equipment = relationship("Equipment", back_populates="readings")
