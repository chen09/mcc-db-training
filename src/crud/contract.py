from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.contract_basic_information import ContractBasicInformation
from src.crud.usb_device import paginate_query, PaginationResult


class ContractCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_max_contract_number(self) -> str:
        """
        获取当前最大的合同号
        
        Returns:
            str: 最大合同号，如果没有合同则返回"0"
        """
        max_contract = self.db.query(func.max(ContractBasicInformation.contract_number)).scalar()
        return max_contract if max_contract is not None else "0"

    def create(self, contract: ContractBasicInformation) -> ContractBasicInformation:
        """创建新的合同基本信息记录"""
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def get_by_contract_number(self, contract_number: str) -> Optional[ContractBasicInformation]:
        """根据合同号获取合同基本信息记录"""
        return self.db.query(ContractBasicInformation).filter(
            ContractBasicInformation.contract_number == contract_number
        ).first()

    def get_all(self, page: int = 1, page_size: int = 10) -> PaginationResult[ContractBasicInformation]:
        """
        获取所有合同基本信息记录（分页）
        
        Args:
            page: 页码，从1开始
            page_size: 每页记录数
            
        Returns:
            PaginationResult: 分页查询结果
        """
        return paginate_query(
            db=self.db,
            model=ContractBasicInformation,
            page=page,
            page_size=page_size
        )

    def update(self, contract: ContractBasicInformation) -> ContractBasicInformation:
        """更新合同基本信息记录"""
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def delete(self, contract_number: str) -> bool:
        """删除合同基本信息记录"""
        contract = self.get_by_contract_number(contract_number)
        if contract:
            self.db.delete(contract)
            self.db.commit()
            return True
        return False

    def get_by_latest_apply_number(self, latest_apply_number: str) -> Optional[ContractBasicInformation]:
        """根据最新申请号获取合同基本信息记录"""
        return self.db.query(ContractBasicInformation).filter(
            ContractBasicInformation.latest_apply_number == latest_apply_number
        ).first()

    def get_contract_with_usb_devices(self, contract_number: str) -> Optional[ContractBasicInformation]:
        """获取合同基本信息及其关联的USB设备记录"""
        return self.db.query(ContractBasicInformation).filter(
            ContractBasicInformation.contract_number == contract_number
        ).first()

    def create_next_contract(self, contract: ContractBasicInformation) -> ContractBasicInformation:
        """
        获取最大合同号并创建新合同，合同号补零到12位
        
        Args:
            contract: 合同基本信息对象（contract_number字段会被自动生成）
            
        Returns:
            ContractBasicInformation: 新创建的合同记录
        """
        # 获取当前最大合同号
        max_contract = self.db.query(func.max(ContractBasicInformation.contract_number)).scalar()
        
        # 如果没有现有合同，从1开始
        if max_contract is None:
            new_contract_number = "000000000001"
        else:
            # 假设合同号是数字字符串，将其转换为整数并加1，然后补零到12位
            new_contract_number = str(int(max_contract) + 1).zfill(12)
        
        # 设置新的合同号
        contract.contract_number = new_contract_number
        
        # 保存到数据库
        return self.create(contract) 