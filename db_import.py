import argparse
import sys
import csv
import os
from datetime import datetime
from sqlalchemy import text, select, update
from sqlalchemy.orm import Session
from config import settings
from src.db import engine
from src.models.contract_basic_information import ContractBasicInformation
from src.models.contract_grant_privilege import ContractGrantPrivilege
from src.models.contract_information_managers import ContractInformationManagers
from src.models.contract_information_users import ContractInformationUsers
from src.models.mst_messages import MstMessages
from src.models.mst_organizations import MstOrganizations
from src.models.mst_service_plans import MstServicePlans
from src.models.mst_services import MstServices
from src.models.contract_usb_device_registration import ContractUsbDeviceRegistration
from src.crud.contract import ContractCRUD
from src.crud.usb_device import UsbDeviceCRUD
from src.crud.organization import OrganizationCRUD


def parse_date(date_str):
    """
    日付文字列をdatetimeオブジェクトに変換する
    
    Args:
        date_str: 日付文字列
        
    Returns:
        datetimeオブジェクト、またはNone（日付文字列が空の場合）
    """
    if not date_str:
        return None
    
    try:
        # まず標準形式を試す
        return datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    except ValueError:
        try:
            # ミリ秒を含む形式を試す
            return datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S.%f')
        except ValueError:
            try:
                # 別の形式を試す
                return datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S.%f')
            except ValueError:
                print(f"警告: 日付形式を解析できません: {date_str}")
                return None


def get_usb_device_by_contract_number(session: Session, contract_number: str):
    """
    契約番号でUSBデバイス情報を取得する
    
    Args:
        session: データベースセッション
        contract_number: 契約番号
        
    Returns:
        USBデバイス情報、またはNone（見つからない場合）
    """
    return session.query(ContractUsbDeviceRegistration).filter(
        ContractUsbDeviceRegistration.contract_number == contract_number
    ).first()


def get_contract_basic_info_by_contract_number(session: Session, contract_number: str):
    """
    契約番号で契約基本情報を取得する
    
    Args:
        session: データベースセッション
        contract_number: 契約番号
        
    Returns:
        契約基本情報、またはNone（見つからない場合）
    """
    return session.query(ContractBasicInformation).filter(
        ContractBasicInformation.contract_number == contract_number
    ).first()


def get_contract_grant_privilege_by_contract_number(session: Session, contract_number: str):
    """
    契約番号で契約権限付与情報を取得する
    
    Args:
        session: データベースセッション
        contract_number: 契約番号
        
    Returns:
        契約権限付与情報、またはNone（見つからない場合）
    """
    return session.query(ContractGrantPrivilege).filter(
        ContractGrantPrivilege.contract_number == contract_number
    ).first()


def get_contract_information_managers_by_contract_number(session: Session, contract_number: str):
    """
    契約番号で契約情報管理者情報を取得する
    
    Args:
        session: データベースセッション
        contract_number: 契約番号
        
    Returns:
        契約情報管理者情報、またはNone（見つからない場合）
    """
    return session.query(ContractInformationManagers).filter(
        ContractInformationManagers.contract_number == contract_number
    ).first()


def get_contract_information_users_by_contract_number(session: Session, contract_number: str):
    """
    契約番号で契約情報ユーザー情報を取得する
    
    Args:
        session: データベースセッション
        contract_number: 契約番号
        
    Returns:
        契約情報ユーザー情報、またはNone（見つからない場合）
    """
    return session.query(ContractInformationUsers).filter(
        ContractInformationUsers.contract_number == contract_number
    ).first()


def get_mst_messages_by_id(session: Session, message_id: int):
    """
    メッセージIDでメッセージ情報を取得する
    
    Args:
        session: データベースセッション
        message_id: メッセージID
        
    Returns:
        メッセージ情報、またはNone（見つからない場合）
    """
    return session.query(MstMessages).filter(
        MstMessages.id == message_id
    ).first()


def get_mst_organizations_by_id(session: Session, organization_id: int):
    """
    組織IDで組織情報を取得する
    
    Args:
        session: データベースセッション
        organization_id: 組織ID
        
    Returns:
        組織情報、またはNone（見つからない場合）
    """
    return session.query(MstOrganizations).filter(
        MstOrganizations.id == organization_id
    ).first()


def get_mst_service_plans_by_id(session: Session, service_plan_id: int):
    """
    サービスプランIDでサービスプラン情報を取得する
    
    Args:
        session: データベースセッション
        service_plan_id: サービスプランID
        
    Returns:
        サービスプラン情報、またはNone（見つからない場合）
    """
    return session.query(MstServicePlans).filter(
        MstServicePlans.id == service_plan_id
    ).first()


def get_mst_services_by_id(session: Session, service_id: int):
    """
    サービスIDでサービス情報を取得する
    
    Args:
        session: データベースセッション
        service_id: サービスID
        
    Returns:
        サービス情報、またはNone（見つからない場合）
    """
    return session.query(MstServices).filter(
        MstServices.id == service_id
    ).first()


def import_usb_devices_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルからUSBデバイス情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_device = get_usb_device_by_contract_number(session, row['contract_number'])
                
                if existing_device:
                    # 既存のレコードを更新
                    existing_device.usb_device_usage_type_master_id = int(row['usb_device_usage_type_master_id'])
                    existing_device.usb_device_usage_type_column_id = int(row['usb_device_usage_type_column_id'])
                    existing_device.usb_device_usage_type_id = int(row['usb_device_usage_type_id'])
                    existing_device.usb_device_usage_reason_master_id = int(row['usb_device_usage_reason_master_id'])
                    existing_device.usb_device_usage_reason_column_id = int(row['usb_device_usage_reason_column_id'])
                    existing_device.usb_device_usage_reason_id = int(row['usb_device_usage_reason_id'])
                    existing_device.device_type_master_id = int(row['device_type_master_id'])
                    existing_device.device_type_column_id = int(row['device_type_column_id'])
                    existing_device.device_type_id = int(row['device_type_id'])
                    existing_device.maker_name_master_id = int(row['maker_name_master_id'])
                    existing_device.maker_name_column_id = int(row['maker_name_column_id'])
                    existing_device.maker_name_id = int(row['maker_name_id'])
                    existing_device.maker_name_manual_input = row['maker_name_manual_input']
                    existing_device.model_name_master_id = int(row['model_name_master_id'])
                    existing_device.model_name_column_id = int(row['model_name_column_id'])
                    existing_device.model_name_id = int(row['model_name_id'])
                    existing_device.model_name_manual_input = row['model_name_manual_input']
                    existing_device.usb_serial_number = row['usb_serial_number']
                    existing_device.created_at = created_at
                    existing_device.created_by = row['created_by']
                    existing_device.created_pg_id = row['created_pg_id']
                    existing_device.updated_at = updated_at
                    existing_device.updated_by = row['updated_by']
                    existing_device.updated_pg_id = row['updated_pg_id']
                    existing_device.version = int(row['version'])
                    existing_device.handling_data_content = row['handling_data_content']
                    existing_device.external_storage_device_required_reason = row['external_storage_device_required_reason']
                    existing_device.work_name = row['work_name']
                    
                    session.add(existing_device)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    usb_device = ContractUsbDeviceRegistration(
                        contract_number=row['contract_number'],
                        usb_device_usage_type_master_id=int(row['usb_device_usage_type_master_id']),
                        usb_device_usage_type_column_id=int(row['usb_device_usage_type_column_id']),
                        usb_device_usage_type_id=int(row['usb_device_usage_type_id']),
                        usb_device_usage_reason_master_id=int(row['usb_device_usage_reason_master_id']),
                        usb_device_usage_reason_column_id=int(row['usb_device_usage_reason_column_id']),
                        usb_device_usage_reason_id=int(row['usb_device_usage_reason_id']),
                        device_type_master_id=int(row['device_type_master_id']),
                        device_type_column_id=int(row['device_type_column_id']),
                        device_type_id=int(row['device_type_id']),
                        maker_name_master_id=int(row['maker_name_master_id']),
                        maker_name_column_id=int(row['maker_name_column_id']),
                        maker_name_id=int(row['maker_name_id']),
                        maker_name_manual_input=row['maker_name_manual_input'],
                        model_name_master_id=int(row['model_name_master_id']),
                        model_name_column_id=int(row['model_name_column_id']),
                        model_name_id=int(row['model_name_id']),
                        model_name_manual_input=row['model_name_manual_input'],
                        usb_serial_number=row['usb_serial_number'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version']),
                        handling_data_content=row['handling_data_content'],
                        external_storage_device_required_reason=row['external_storage_device_required_reason'],
                        work_name=row['work_name']
                    )
                    session.add(usb_device)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_contract_basic_info_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルから契約基本情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                usage_start_date = parse_date(row['usage_start_date']) if 'usage_start_date' in row and row['usage_start_date'] else None
                usage_end_date = parse_date(row['usage_end_date']) if 'usage_end_date' in row and row['usage_end_date'] else None
                desired_start_date = parse_date(row['desired_start_date']) if 'desired_start_date' in row and row['desired_start_date'] else None
                scheduled_end_date = parse_date(row['scheduled_end_date']) if 'scheduled_end_date' in row and row['scheduled_end_date'] else None
                
                # 既存のレコードを検索
                existing_contract = get_contract_basic_info_by_contract_number(session, row['contract_number'])
                
                if existing_contract:
                    # 既存のレコードを更新
                    existing_contract.contract_status = row['contract_status']
                    existing_contract.service_id = int(row['service_id']) if row['service_id'] else None
                    existing_contract.usage_start_date = usage_start_date
                    existing_contract.usage_end_date = usage_end_date
                    existing_contract.desired_start_date = desired_start_date
                    existing_contract.scheduled_end_date = scheduled_end_date
                    existing_contract.latest_apply_number = row['latest_apply_number']
                    existing_contract.bill_to_company_code = row['bill_to_company_code']
                    existing_contract.cost_center_code = row['cost_center_code']
                    existing_contract.remarks = row['remarks']
                    existing_contract.versatile_remarks1 = row['versatile_remarks1']
                    existing_contract.versatile_remarks2 = row['versatile_remarks2']
                    existing_contract.versatile_remarks3 = row['versatile_remarks3']
                    existing_contract.versatile_remarks4 = row['versatile_remarks4']
                    existing_contract.versatile_remarks5 = row['versatile_remarks5']
                    existing_contract.created_at = created_at
                    existing_contract.created_by = row['created_by']
                    existing_contract.created_pg_id = row['created_pg_id']
                    existing_contract.updated_at = updated_at
                    existing_contract.updated_by = row['updated_by']
                    existing_contract.updated_pg_id = row['updated_pg_id']
                    existing_contract.version = int(row['version'])
                    
                    session.add(existing_contract)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    contract = ContractBasicInformation(
                        contract_number=row['contract_number'],
                        contract_status=row['contract_status'],
                        service_id=int(row['service_id']) if row['service_id'] else None,
                        usage_start_date=usage_start_date,
                        usage_end_date=usage_end_date,
                        desired_start_date=desired_start_date,
                        scheduled_end_date=scheduled_end_date,
                        latest_apply_number=row['latest_apply_number'],
                        bill_to_company_code=row['bill_to_company_code'],
                        cost_center_code=row['cost_center_code'],
                        remarks=row['remarks'],
                        versatile_remarks1=row['versatile_remarks1'],
                        versatile_remarks2=row['versatile_remarks2'],
                        versatile_remarks3=row['versatile_remarks3'],
                        versatile_remarks4=row['versatile_remarks4'],
                        versatile_remarks5=row['versatile_remarks5'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(contract)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_contract_grant_privilege_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルから契約権限付与情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_privilege = get_contract_grant_privilege_by_contract_number(session, row['contract_number'])
                
                if existing_privilege:
                    # 既存のレコードを更新
                    existing_privilege.url_name = row['url_name']
                    existing_privilege.apply_reason_type = int(row['apply_reason_type'])
                    existing_privilege.job_description = row['job_description']
                    existing_privilege.install_app_name = row['install_app_name']
                    existing_privilege.execute_app_name = row['execute_app_name']
                    existing_privilege.app_feature = row['app_feature']
                    existing_privilege.target_faq_url_name = row['target_faq_url_name']
                    existing_privilege.app_name = row['app_name']
                    existing_privilege.administrator_privilege_device_master_id = int(row['administrator_privilege_device_master_id']) if row['administrator_privilege_device_master_id'] else None
                    existing_privilege.administrator_privilege_device_column_id = int(row['administrator_privilege_device_column_id']) if row['administrator_privilege_device_column_id'] else None
                    existing_privilege.administrator_privilege_device_id = int(row['administrator_privilege_device_id']) if row['administrator_privilege_device_id'] else None
                    existing_privilege.created_at = created_at
                    existing_privilege.created_by = row['created_by']
                    existing_privilege.created_pg_id = row['created_pg_id']
                    existing_privilege.updated_at = updated_at
                    existing_privilege.updated_by = row['updated_by']
                    existing_privilege.updated_pg_id = row['updated_pg_id']
                    existing_privilege.version = int(row['version'])
                    
                    session.add(existing_privilege)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    privilege = ContractGrantPrivilege(
                        contract_number=row['contract_number'],
                        url_name=row['url_name'],
                        apply_reason_type=int(row['apply_reason_type']),
                        job_description=row['job_description'],
                        install_app_name=row['install_app_name'],
                        execute_app_name=row['execute_app_name'],
                        app_feature=row['app_feature'],
                        target_faq_url_name=row['target_faq_url_name'],
                        app_name=row['app_name'],
                        administrator_privilege_device_master_id=int(row['administrator_privilege_device_master_id']) if row['administrator_privilege_device_master_id'] else None,
                        administrator_privilege_device_column_id=int(row['administrator_privilege_device_column_id']) if row['administrator_privilege_device_column_id'] else None,
                        administrator_privilege_device_id=int(row['administrator_privilege_device_id']) if row['administrator_privilege_device_id'] else None,
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(privilege)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_contract_information_managers_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルから契約情報管理者情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_manager = get_contract_information_managers_by_contract_number(session, row['contract_number'])
                
                if existing_manager:
                    # 既存のレコードを更新
                    existing_manager.manager_id = row['manager_id']
                    existing_manager.manager_name = row['manager_name']
                    existing_manager.manager_email = row['manager_email']
                    existing_manager.manager_phone = row['manager_phone']
                    existing_manager.created_at = created_at
                    existing_manager.created_by = row['created_by']
                    existing_manager.created_pg_id = row['created_pg_id']
                    existing_manager.updated_at = updated_at
                    existing_manager.updated_by = row['updated_by']
                    existing_manager.updated_pg_id = row['updated_pg_id']
                    existing_manager.version = int(row['version'])
                    
                    session.add(existing_manager)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    manager = ContractInformationManagers(
                        contract_number=row['contract_number'],
                        manager_id=row['manager_id'],
                        manager_name=row['manager_name'],
                        manager_email=row['manager_email'],
                        manager_phone=row['manager_phone'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(manager)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_contract_information_users_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルから契約情報ユーザー情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_user = get_contract_information_users_by_contract_number(session, row['contract_number'])
                
                if existing_user:
                    # 既存のレコードを更新
                    existing_user.user_id = row['user_id']
                    existing_user.user_name = row['user_name']
                    existing_user.user_email = row['user_email']
                    existing_user.user_phone = row['user_phone']
                    existing_user.created_at = created_at
                    existing_user.created_by = row['created_by']
                    existing_user.created_pg_id = row['created_pg_id']
                    existing_user.updated_at = updated_at
                    existing_user.updated_by = row['updated_by']
                    existing_user.updated_pg_id = row['updated_pg_id']
                    existing_user.version = int(row['version'])
                    
                    session.add(existing_user)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    user = ContractInformationUsers(
                        contract_number=row['contract_number'],
                        user_id=row['user_id'],
                        user_name=row['user_name'],
                        user_email=row['user_email'],
                        user_phone=row['user_phone'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(user)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_mst_messages_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルからメッセージ情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_message = get_mst_messages_by_id(session, int(row['id']))
                
                if existing_message:
                    # 既存のレコードを更新
                    existing_message.message_code = row['message_code']
                    existing_message.message_type = row['message_type']
                    existing_message.message_text = row['message_text']
                    existing_message.created_at = created_at
                    existing_message.created_by = row['created_by']
                    existing_message.created_pg_id = row['created_pg_id']
                    existing_message.updated_at = updated_at
                    existing_message.updated_by = row['updated_by']
                    existing_message.updated_pg_id = row['updated_pg_id']
                    existing_message.version = int(row['version'])
                    
                    session.add(existing_message)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    message = MstMessages(
                        id=int(row['id']),
                        message_code=row['message_code'],
                        message_type=row['message_type'],
                        message_text=row['message_text'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(message)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_mst_organizations_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルから組織情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_org = get_mst_organizations_by_id(session, int(row['id']))
                
                if existing_org:
                    # 既存のレコードを更新
                    existing_org.organization_code = row['organization_code']
                    existing_org.organization_name = row['organization_name']
                    existing_org.organization_type = row['organization_type']
                    existing_org.created_at = created_at
                    existing_org.created_by = row['created_by']
                    existing_org.created_pg_id = row['created_pg_id']
                    existing_org.updated_at = updated_at
                    existing_org.updated_by = row['updated_by']
                    existing_org.updated_pg_id = row['updated_pg_id']
                    existing_org.version = int(row['version'])
                    
                    session.add(existing_org)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    org = MstOrganizations(
                        id=int(row['id']),
                        organization_code=row['organization_code'],
                        organization_name=row['organization_name'],
                        organization_type=row['organization_type'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(org)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_mst_service_plans_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルからサービスプラン情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_plan = get_mst_service_plans_by_id(session, int(row['id']))
                
                if existing_plan:
                    # 既存のレコードを更新
                    existing_plan.service_plan_code = row['service_plan_code']
                    existing_plan.service_plan_name = row['service_plan_name']
                    existing_plan.service_id = int(row['service_id'])
                    existing_plan.created_at = created_at
                    existing_plan.created_by = row['created_by']
                    existing_plan.created_pg_id = row['created_pg_id']
                    existing_plan.updated_at = updated_at
                    existing_plan.updated_by = row['updated_by']
                    existing_plan.updated_pg_id = row['updated_pg_id']
                    existing_plan.version = int(row['version'])
                    
                    session.add(existing_plan)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    plan = MstServicePlans(
                        id=int(row['id']),
                        service_plan_code=row['service_plan_code'],
                        service_plan_name=row['service_plan_name'],
                        service_id=int(row['service_id']),
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(plan)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_mst_services_from_csv(session: Session, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    CSVファイルからサービス情報をインポートする
    
    Args:
        session: データベースセッション
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル {csv_file_path} が見つかりません")
        return 0
    
    processed_count = 0
    updated_count = 0
    inserted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                processed_count += 1
                
                # 日付文字列をdatetimeオブジェクトに変換
                created_at = parse_date(row['created_at'])
                updated_at = parse_date(row['updated_at'])
                
                # 既存のレコードを検索
                existing_service = get_mst_services_by_id(session, int(row['id']))
                
                if existing_service:
                    # 既存のレコードを更新
                    existing_service.service_code = row['service_code']
                    existing_service.service_name = row['service_name']
                    existing_service.service_type = row['service_type']
                    existing_service.created_at = created_at
                    existing_service.created_by = row['created_by']
                    existing_service.created_pg_id = row['created_pg_id']
                    existing_service.updated_at = updated_at
                    existing_service.updated_by = row['updated_by']
                    existing_service.updated_pg_id = row['updated_pg_id']
                    existing_service.version = int(row['version'])
                    
                    session.add(existing_service)
                    updated_count += 1
                else:
                    # 新しいレコードを作成
                    service = MstServices(
                        id=int(row['id']),
                        service_code=row['service_code'],
                        service_name=row['service_name'],
                        service_type=row['service_type'],
                        created_at=created_at,
                        created_by=row['created_by'],
                        created_pg_id=row['created_pg_id'],
                        updated_at=updated_at,
                        updated_by=row['updated_by'],
                        updated_pg_id=row['updated_pg_id'],
                        version=int(row['version'])
                    )
                    session.add(service)
                    inserted_count += 1
                
                # 指定された間隔でコミット
                if processed_count % commit_interval == 0:
                    session.commit()
                    print(f"処理済み: {processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        
        # 残りのレコードをコミット
        session.commit()
        print(f"処理完了: 合計{processed_count}件 (挿入: {inserted_count}件, 更新: {updated_count}件)")
        return processed_count
    
    except Exception as e:
        session.rollback()
        print(f"インポート中にエラーが発生しました: {str(e)}")
        return 0


def import_data(session: Session, model_type: str, csv_file_path: str, commit_interval: int = 1000) -> int:
    """
    指定されたモデルタイプに基づいてCSVファイルからデータをインポートする
    
    Args:
        session: データベースセッション
        model_type: モデルタイプ
        csv_file_path: CSVファイルのパス
        commit_interval: コミット間隔（レコード数）
        
    Returns:
        処理したレコード数
    """
    if model_type == "ContractUsbDeviceRegistration":
        return import_usb_devices_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "ContractBasicInformation":
        return import_contract_basic_info_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "ContractGrantPrivilege":
        return import_contract_grant_privilege_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "ContractInformationManagers":
        return import_contract_information_managers_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "ContractInformationUsers":
        return import_contract_information_users_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "MstMessages":
        return import_mst_messages_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "MstOrganizations":
        return import_mst_organizations_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "MstServicePlans":
        return import_mst_service_plans_from_csv(session, csv_file_path, commit_interval)
    elif model_type == "MstServices":
        return import_mst_services_from_csv(session, csv_file_path, commit_interval)
    else:
        print(f"エラー: サポートされていないモデルタイプです: {model_type}")
        return 0


def main() -> int:    
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='CSVファイルからデータをインポートする')
    parser.add_argument('--model', type=str, required=True, help='インポートするモデルタイプ (例: ContractUsbDeviceRegistration, ContractBasicInformation, ContractGrantPrivilege, ContractInformationManagers, ContractInformationUsers, MstMessages, MstOrganizations, MstServicePlans, MstServices)')
    parser.add_argument('--csv', type=str, required=True, help='インポートするCSVファイルのパス')
    parser.add_argument('--commit-interval', type=int, default=1000, help='コミット間隔（レコード数、デフォルト: 1000）')
    args = parser.parse_args()
    
    try:
        # テスト数据库连接
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("数据库连接成功!")
            print(f"连接URI: {settings.DATABASE_DEV_URI}")

        # 创建数据库会话
        session = Session(engine)
        
        # 指定されたモデルタイプとCSVファイルからデータをインポート
        processed_count = import_data(session, args.model, args.csv, args.commit_interval)
        
        if processed_count > 0:
            print(f"CSVファイルから{processed_count}件のデータをインポートしました")
        else:
            print("CSVファイルからのインポートに失敗しました")

        return 0
    except Exception as e:
        print(f"操作失败: {str(e)}")
        return 1
    finally:
        session.close()


if __name__ == "__main__":
    main()
    sys.exit(0)