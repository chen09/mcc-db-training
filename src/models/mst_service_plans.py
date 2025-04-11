from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class MstServicePlans(BaseModel):
    """服务计划表"""
    __tablename__ = "mst_service_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("mst_services.id"), nullable=False)
    unit_price = Column(Integer, nullable=False)
    message_plan_name_id = Column(Integer, nullable=False)
    display_order = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False)

    # 关联服务表
    service = relationship("MstServices", backref="service_plans")

    def __repr__(self):
        return f"<MstServicePlans(id={self.id}, service_id={self.service_id})>" 