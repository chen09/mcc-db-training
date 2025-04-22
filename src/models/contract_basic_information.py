from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class ContractBase(BaseModel):
    """合同基本信息基类"""
    __abstract__ = True

    contract_number = Column(String, primary_key=True)


class ContractBasicInformation(ContractBase):
    """合同基本信息表"""
    __tablename__ = "trn_contract_basic_information"

    contract_status = Column(Integer, nullable=False)
    latest_apply_number = Column(String, nullable=True)
    service_id = Column(Integer, nullable=True)
    versatile_remarks1 = Column(String, nullable=True)
    versatile_remarks2 = Column(String, nullable=True)
    versatile_remarks3 = Column(String, nullable=True)
    versatile_remarks4 = Column(String, nullable=True)
    versatile_remarks5 = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    usage_start_date = Column(DateTime(timezone=True), nullable=True)
    usage_end_date = Column(DateTime(timezone=True), nullable=True)
    desired_start_date = Column(DateTime(timezone=True), nullable=True)
    scheduled_end_date = Column(DateTime(timezone=True), nullable=True)
    bill_to_company_code = Column(String, nullable=True)
    cost_center_code = Column(String, nullable=True)
    invoice_address_company_code_master_id = Column(Integer, nullable=True)
    invoice_address_company_code_column_id = Column(Integer, nullable=True)
    invoice_address_company_code_id = Column(Integer, nullable=True)
    service_plan_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ContractBasicInformation(contract_number='{self.contract_number}')>" 