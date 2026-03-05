import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(String(20), primary_key=True)
    equipment_id = Column(String(50), ForeignKey("equipment.id"))
    title_tr = Column(String(500), nullable=False)
    title_th = Column(String(500))
    description = Column(Text)
    priority = Column(String(20), nullable=False, default="medium")
    status = Column(String(30), nullable=False, default="open")
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    accepted_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    deadline = Column(DateTime(timezone=True))
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    materials_used = Column(JSON, default=[])
    loto_required = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    equipment = relationship("Equipment", back_populates="work_orders")
    photos = relationship("WorkOrderPhoto", back_populates="work_order", cascade="all, delete-orphan")

class WorkOrderPhoto(Base):
    __tablename__ = "work_order_photos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_id = Column(String(20), ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(512), nullable=False)
    caption = Column(String(500))
    photo_type = Column(String(50), default="documentation")
    taken_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    gps_lat = Column(Float)
    gps_lng = Column(Float)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    work_order = relationship("WorkOrder", back_populates="photos")
