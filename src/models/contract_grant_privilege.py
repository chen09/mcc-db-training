from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class ContractGrantPrivilege(BaseModel):
    """
    契約権限付与情報モデル
    
    契約に対する権限付与情報を管理するモデル
    """
    __tablename__ = 'trn_contract_grant_privilege'

    # 主キー
    contract_number = Column(String, primary_key=True, comment='契約番号')
    
    # 権限情報
    url_name = Column(String, nullable=True, comment='URL名')
    apply_reason_type = Column(Integer, nullable=False, comment='申請理由種別')
    job_description = Column(String, nullable=True, comment='業務内容')
    install_app_name = Column(String, nullable=True, comment='インストールアプリ名')
    execute_app_name = Column(String, nullable=True, comment='実行アプリ名')
    app_feature = Column(String, nullable=True, comment='アプリ機能')
    target_faq_url_name = Column(String, nullable=True, comment='対象FAQ URL名')
    app_name = Column(String, nullable=True, comment='アプリ名')
    
    # 管理者デバイス情報
    administrator_privilege_device_master_id = Column(Integer, nullable=True, comment='管理者権限デバイスマスタID')
    administrator_privilege_device_column_id = Column(Integer, nullable=True, comment='管理者権限デバイスカラムID')
    administrator_privilege_device_id = Column(Integer, nullable=True, comment='管理者権限デバイスID')
    
