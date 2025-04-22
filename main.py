import argparse
import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import settings
from src.db import engine
from src.models.contract_basic_information import ContractBasicInformation
from src.models.contract_grant_privilege import ContractGrantPrivilege
from src.models.contract_information_managers import ContractInformationManagers
from src.models.contract_information_users import ContractInformationUsers
from src.models.contract_usb_device_registration import ContractUsbDeviceRegistration
from src.crud.contract import ContractCRUD
from src.crud.usb_device import UsbDeviceCRUD
from src.crud.organization import OrganizationCRUD


def main() -> int:    
    try:
        # 测试数据库连接
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("数据库连接成功!")
            print(f"连接URI: {settings.DATABASE_DEV_URI}")

        # 创建数据库会话
        session = Session(engine)
        contract_crud = ContractCRUD(session)
        usb_device_crud = UsbDeviceCRUD(session)
        organization_crud = OrganizationCRUD(session)

        # 获取随机组织代码
        random_org_code = organization_crud.get_random_organization_code()
        print(f"获取随机组织代码: {random_org_code}")

        # 创建新合同
        contract = ContractBasicInformation(
            contract_status=1,
            created_by="admin",
            created_pg_id="system",
            updated_by="admin",
            updated_pg_id="system",
            version=1,
            service_id=76,
            bill_to_company_code=random_org_code,  # 设置随机组织代码
            cost_center_code='A001'
        )
        next_contract = contract_crud.create_next_contract(contract)
        print(f"创建新合同: {next_contract.contract_number}, bill_to_company_code: {next_contract.bill_to_company_code}")

        # 创建USB设备记录
        usb_device = ContractUsbDeviceRegistration(
            contract_number=next_contract.contract_number,
            usb_device_usage_type_master_id=1,
            usb_device_usage_type_column_id=1,
            usb_device_usage_type_id=1,
            usb_device_usage_reason_master_id=1,
            usb_device_usage_reason_column_id=1,
            usb_device_usage_reason_id=1,
            device_type_master_id=1,
            device_type_column_id=1,
            device_type_id=1,
            maker_name_master_id=1,
            maker_name_column_id=1,
            maker_name_id=1,
            model_name_master_id=1,
            model_name_column_id=1,
            model_name_id=1,
            usb_serial_number="SN123456",
            created_by="admin",
            created_pg_id="system",
            updated_by="admin",
            updated_pg_id="system",
            version=1,
            handling_data_content="测试数据",
            external_storage_device_required_reason="测试原因",
            work_name="测试工作"
        )
        new_usb_device = usb_device_crud.create(usb_device)
        print(f"创建USB设备记录: {new_usb_device.contract_number}")

        return 0
    except Exception as e:
        print(f"操作失败: {str(e)}")
        return 1
    finally:
        session.close()

def test_contract_crud():
    """测试合同基本信息CRUD操作"""
    print("\n=== 测试合同基本信息CRUD操作 ===")
    
    # 创建合同基本信息
    contract = ContractBasicInformation(
        contract_status=1,
        created_by="admin",
        created_pg_id="system",
        updated_by="admin",
        updated_pg_id="system",
        version=1
    )
    
    # 使用create_next_contract创建新合同
    new_contract = contract_crud.create_next_contract(contract)
    print(f"创建新合同: {new_contract.contract_number}")
    
    # 更新合同状态
    new_contract.contract_status = 2
    updated_contract = contract_crud.update(new_contract)
    print(f"更新合同状态: {updated_contract.contract_status}")
    
    # 获取合同信息
    contract_info = contract_crud.get_by_contract_number(new_contract.contract_number)
    print(f"获取合同信息: {contract_info.contract_number}, 状态: {contract_info.contract_status}")
    
    # 分页获取所有合同
    result = contract_crud.get_all(page=1, page_size=10)
    print(f"分页获取合同列表: 总数={result.total}, 当前页={result.page}, 每页数量={result.page_size}")
    for contract in result.items:
        print(f"合同号: {contract.contract_number}, 状态: {contract.contract_status}")
    
    # 删除合同
    if contract_crud.delete(new_contract.contract_number):
        print(f"删除合同: {new_contract.contract_number}")
    else:
        print("删除合同失败")

def test_usb_device_crud():
    """测试USB设备注册CRUD操作"""
    print("\n=== 测试USB设备注册CRUD操作 ===")
    
    # 创建合同基本信息
    contract = ContractBasicInformation(
        contract_status=1,
        created_by="admin",
        created_pg_id="system",
        updated_by="admin",
        updated_pg_id="system",
        version=1
    )
    new_contract = contract_crud.create_next_contract(contract)
    
    # 创建USB设备注册记录
    usb_device = ContractUsbDeviceRegistration(
        contract_number=new_contract.contract_number,
        created_by="admin",
        created_pg_id="system",
        updated_by="admin",
        updated_pg_id="system",
        version=1
    )
    
    # 创建USB设备记录
    new_usb_device : ContractUsbDeviceRegistration = usb_device_crud.create(usb_device)
    print(f"创建USB设备记录: {new_usb_device.contract_number}")
    
    # 更新USB设备状态
    new_usb_device.device_status = 2
    updated_usb_device = usb_device_crud.update(new_usb_device)
    print(f"更新USB设备状态: {updated_usb_device.device_status}")
    
    # 获取USB设备信息
    usb_device_info = usb_device_crud.get_by_device_id(new_usb_device.device_id)
    print(f"获取USB设备信息: {usb_device_info.device_id}, 状态: {usb_device_info.device_status}")
    
    # 分页获取所有USB设备
    result = usb_device_crud.get_all(page=1, page_size=10)
    print(f"分页获取USB设备列表: 总数={result.total}, 当前页={result.page}, 每页数量={result.page_size}")
    for device in result.items:
        print(f"设备ID: {device.device_id}, 状态: {device.device_status}")
    
    # 删除USB设备记录
    if usb_device_crud.delete(new_usb_device.device_id):
        print(f"删除USB设备记录: {new_usb_device.device_id}")
    else:
        print("删除USB设备记录失败")
    
    # 删除关联的合同
    contract_crud.delete(new_contract.contract_number)

if __name__ == "__main__":
    for i in range(1000):
        print(f"执行第{i+1}次")
        main()
    sys.exit(0)