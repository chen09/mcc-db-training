from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    """基础模型类，包含公共字段"""
    __abstract__ = True

    created_by = Column(String, nullable=False)
    created_pg_id = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)
    updated_pg_id = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()) 