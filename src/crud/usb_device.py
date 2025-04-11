from typing import List, Optional, Tuple, TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.usb_device import ContractUsbDeviceRegistration

T = TypeVar('T')

class PaginationResult(Generic[T]):
    """分页查询结果"""
    def __init__(self, items: List[T], total: int, page: int, page_size: int):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = (total + page_size - 1) // page_size

    def __repr__(self):
        return f"<PaginationResult(items={len(self.items)}, total={self.total}, page={self.page}, page_size={self.page_size})>"


def paginate_query(
    db: Session,
    model: Type[T],
    page: int = 1,
    page_size: int = 10,
    **filters
) -> PaginationResult[T]:
    """
    通用分页查询函数
    
    Args:
        db: 数据库会话
        model: 模型类
        page: 页码，从1开始
        page_size: 每页记录数
        **filters: 过滤条件
        
    Returns:
        PaginationResult: 分页查询结果
    """
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 构建查询
    query = db.query(model)
    
    # 应用过滤条件
    for key, value in filters.items():
        if hasattr(model, key) and value is not None:
            query = query.filter(getattr(model, key) == value)
    
    # 获取总记录数
    total = query.count()
    
    # 获取分页数据
    items = query.offset(offset).limit(page_size).all()
    
    return PaginationResult(items=items, total=total, page=page, page_size=page_size)


class UsbDeviceCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, device: ContractUsbDeviceRegistration) -> ContractUsbDeviceRegistration:
        """创建新的USB设备注册记录"""
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def get_by_contract(self, contract_number: str) -> Optional[ContractUsbDeviceRegistration]:
        """根据合同号获取USB设备注册记录"""
        return self.db.query(ContractUsbDeviceRegistration).filter(
            ContractUsbDeviceRegistration.contract_number == contract_number
        ).first()

    def get_all(self, page: int = 1, page_size: int = 10) -> PaginationResult[ContractUsbDeviceRegistration]:
        """
        获取所有USB设备注册记录（分页）
        
        Args:
            page: 页码，从1开始
            page_size: 每页记录数
            
        Returns:
            PaginationResult: 分页查询结果
        """
        return paginate_query(
            db=self.db,
            model=ContractUsbDeviceRegistration,
            page=page,
            page_size=page_size
        )

    def update(self, device: ContractUsbDeviceRegistration) -> ContractUsbDeviceRegistration:
        """更新USB设备注册记录"""
        self.db.commit()
        self.db.refresh(device)
        return device

    def delete(self, contract_number: str) -> bool:
        """删除USB设备注册记录"""
        device = self.get_by_contract(contract_number)
        if device:
            self.db.delete(device)
            self.db.commit()
            return True
        return False

    def get_by_serial_number(self, serial_number: str) -> Optional[ContractUsbDeviceRegistration]:
        """根据USB序列号获取设备注册记录"""
        return self.db.query(ContractUsbDeviceRegistration).filter(
            ContractUsbDeviceRegistration.usb_serial_number == serial_number
        ).first() 