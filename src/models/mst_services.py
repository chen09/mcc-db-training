from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class MstServices(BaseModel):
    """服务主表"""
    __tablename__ = "mst_services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    message_caption_id = Column(Integer, nullable=False)
    message_description_id = Column(Integer, nullable=False)
    message_attached_file_id = Column(Integer, nullable=True)
    tag = Column(String, nullable=True)
    target_link = Column(String, nullable=True)
    attached_file_url = Column(String, nullable=True)
    apply_component_key = Column(String, nullable=True)
    is_contract_excluded = Column(Integer, nullable=True)
    usage_start_date = Column(DateTime(timezone=True), nullable=True)
    usage_end_date = Column(DateTime(timezone=True), nullable=True)
    is_show_apply_for_end_of_use_button = Column(Integer, nullable=False, default=1)
    is_workflow = Column(Integer, nullable=False, default=0)
    workflow_application_name = Column(String, nullable=True)
    is_work_management = Column(Integer, nullable=False, default=0)
    lead_time_new = Column(Integer, nullable=True)
    lead_time_change = Column(Integer, nullable=True)
    lead_time_end_of_use = Column(Integer, nullable=True)
    is_show_apply_for_change_button = Column(Integer, nullable=False, default=1)
    is_servicenow = Column(Integer, nullable=False, default=0)
    servicenow_url_new = Column(String, nullable=True)
    servicenow_url_change = Column(String, nullable=True)
    servicenow_url_end_of_use = Column(String, nullable=True)
    provided_cost_center_code = Column(String, nullable=True)
    provided_cost_center_name = Column(String, nullable=True)
    expense_details_code = Column(String, nullable=True)
    expense_details_name = Column(String, nullable=True)
    message_new_mail_id = Column(Integer, nullable=True)
    message_modify_mail_id = Column(Integer, nullable=True)
    message_cancel_mail_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<MstServices(id={self.id}, type={self.type})>" 