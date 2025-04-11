from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class ContractInformationManagers(BaseModel):
    """合同信息管理员表"""
    __tablename__ = "trn_contract_information_managers"

    contract_number = Column(String, ForeignKey("trn_contract_basic_information.contract_number"), primary_key=True)
    manager_oa_number = Column(String, primary_key=True)
    manager_department = Column(String, nullable=True)
    manager_phone = Column(String, nullable=True)

    # 创建索引
    __table_args__ = (
        Index('idx_contract_information_managers_01', 'manager_oa_number'),
    )

    # 关联合同基本信息表
    contract = relationship("ContractBasicInformation", backref="managers")

    def __repr__(self):
        return f"<ContractInformationManagers(contract_number='{self.contract_number}', manager_oa_number='{self.manager_oa_number}')>" 