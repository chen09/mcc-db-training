from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.models.contract_basic_information import ContractBase

class ContractUsbDeviceRegistration(ContractBase):
    """USB设备注册表"""
    __tablename__ = "trn_contract_usb_device_registration"

    contract_number = Column(String, ForeignKey("trn_contract_basic_information.contract_number"), primary_key=True)
    usb_device_usage_type_master_id = Column(Integer, nullable=False)
    usb_device_usage_type_column_id = Column(Integer, nullable=False)
    usb_device_usage_type_id = Column(Integer, nullable=False)
    usb_device_usage_reason_master_id = Column(Integer, nullable=False)
    usb_device_usage_reason_column_id = Column(Integer, nullable=False)
    usb_device_usage_reason_id = Column(Integer, nullable=False)
    device_type_master_id = Column(Integer, nullable=False)
    device_type_column_id = Column(Integer, nullable=False)
    device_type_id = Column(Integer, nullable=False)
    maker_name_master_id = Column(Integer, nullable=False)
    maker_name_column_id = Column(Integer, nullable=False)
    maker_name_id = Column(Integer, nullable=False)
    maker_name_manual_input = Column(String, nullable=True)
    model_name_master_id = Column(Integer, nullable=False)
    model_name_column_id = Column(Integer, nullable=False)
    model_name_id = Column(Integer, nullable=False)
    model_name_manual_input = Column(String, nullable=True)
    usb_serial_number = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_by = Column(String, nullable=False)
    created_pg_id = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)
    updated_pg_id = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    handling_data_content = Column(String, nullable=False)
    external_storage_device_required_reason = Column(String, nullable=False)
    work_name = Column(String, nullable=False)

    # 关联合同基本信息
    contract = relationship("ContractBasicInformation", back_populates="usb_devices")

    def __repr__(self):
        return f"<ContractUsbDeviceRegistration(contract_number='{self.contract_number}')>" 