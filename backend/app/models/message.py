from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel = Column(String(20), nullable=False, default="app")
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    sender_name = Column(String(255))
    sender_type = Column(String(30), default="user")
    message_type = Column(String(30), default="text")
    content = Column(Text, nullable=False)
    extra_data = Column("metadata", JSON, default={})
    reply_to = Column(Integer, ForeignKey("messages.id"))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    original_name = Column(String(512), nullable=False)
    stored_path = Column(String(512), nullable=False)
    mime_type = Column(String(255))
    file_size = Column(Integer)
    file_category = Column(String(50))
    ai_analysis = Column(JSON)
    ai_analyzed_at = Column(DateTime(timezone=True))
    work_order_id = Column(String(20), ForeignKey("work_orders.id"))
    equipment_id = Column(String(50), ForeignKey("equipment.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
