from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from src.models.mst_organizations import MstOrganizations
from src.crud.usb_device import paginate_query, PaginationResult


class OrganizationCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_random_organization_code(self, organization_level: str = '1') -> Optional[str]:
        """
        获取随机组织代码
        
        Args:
            organization_level: 组织级别，默认为'1'
            
        Returns:
            str: 随机组织代码，如果没有找到则返回None
        """
        # 使用原生SQL查询获取随机组织代码
        result = self.db.execute(
            text("SELECT organization_code FROM mst_organizations WHERE organization_level = :level ORDER BY RANDOM() LIMIT 1"),
            {"level": organization_level}
        ).first()
        
        if result:
            return result[0]
        return None

    def get_by_organization_code(self, organization_code: str) -> Optional[MstOrganizations]:
        """根据组织代码获取组织信息"""
        return self.db.query(MstOrganizations).filter(
            MstOrganizations.organization_code == organization_code
        ).first()

    def get_all(self, page: int = 1, page_size: int = 10) -> PaginationResult[MstOrganizations]:
        """
        获取所有组织信息（分页）
        
        Args:
            page: 页码，从1开始
            page_size: 每页记录数
            
        Returns:
            PaginationResult: 分页查询结果
        """
        return paginate_query(
            db=self.db,
            model=MstOrganizations,
            page=page,
            page_size=page_size
        ) 