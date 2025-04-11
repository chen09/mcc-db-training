from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class MstOrganizations(BaseModel):
    """组织表"""
    __tablename__ = "mst_organizations"

    organization_code = Column(String, primary_key=True)
    organization_level = Column(String, nullable=True)
    organization_name = Column(String, nullable=True)
    organization_name_en = Column(String, nullable=True)
    organization_shortened_name = Column(String, nullable=True)
    organization_shortened_name_en = Column(String, nullable=True)
    parent_organization_code = Column(String, ForeignKey("mst_organizations.organization_code"), nullable=True)
    display_order = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=True)

    # 自引用关系
    parent = relationship("MstOrganizations", remote_side=[organization_code], backref="children")

    def __repr__(self):
        return f"<MstOrganizations(organization_code='{self.organization_code}', organization_name='{self.organization_name}')>" 