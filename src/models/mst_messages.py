from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class MstMessages(BaseModel):
    """消息表"""
    __tablename__ = "mst_messages"

    id = Column(Integer, primary_key=True)
    language = Column(Integer, primary_key=True)
    message = Column(String, nullable=True)

    def __repr__(self):
        return f"<MstMessages(id={self.id}, language={self.language})>" 