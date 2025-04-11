from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class ContractInformationUsers(BaseModel):
    """合同信息用户表"""
    __tablename__ = "trn_contract_information_users"

    contract_number = Column(String, ForeignKey("trn_contract_basic_information.contract_number"), primary_key=True)
    user_oa_number = Column(String, primary_key=True)
    user_department = Column(String, nullable=True)
    user_phone = Column(String, nullable=True)

    # 创建索引
    __table_args__ = (
        Index('idx_contract_information_users_01', 'user_oa_number'),
    )

    # 关联合同基本信息表
    contract = relationship("ContractBasicInformation", backref="users")

    def __repr__(self):
        return f"<ContractInformationUsers(contract_number='{self.contract_number}', user_oa_number='{self.user_oa_number}')>" 