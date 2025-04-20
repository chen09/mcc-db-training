-- public.view_contract_usb_device_registration source

CREATE OR REPLACE VIEW public.view_contract_usb_device_registration
AS SELECT vabasicinfo.contract_number,
    vabasicinfo.contract_status,
    vabasicinfo.service_id,
    vabasicinfo.usage_start_date,
    vabasicinfo.usage_end_date,
    vabasicinfo.desired_start_date,
    vabasicinfo.scheduled_end_date,
    vabasicinfo.latest_apply_number,
    vabasicinfo.bill_to_company_code,
    vabasicinfo.bill_to_company_name,
    vabasicinfo.invoice_address_company_code,
    vabasicinfo.invoice_address_company_name,
    vabasicinfo.cost_center_code,
    vabasicinfo.cost_center_name,
    vabasicinfo.remarks,
    vabasicinfo.versatile_remarks1,
    vabasicinfo.versatile_remarks2,
    vabasicinfo.versatile_remarks3,
    vabasicinfo.versatile_remarks4,
    vabasicinfo.versatile_remarks5,
    vabasicinfo.created_at,
    vabasicinfo.created_by,
    vabasicinfo.created_pg_id,
    vabasicinfo.updated_at,
    vabasicinfo.updated_by,
    vabasicinfo.updated_pg_id,
    vabasicinfo.version,
    vabasicinfo.service_caption_id,
    vabasicinfo.apply_component_key,
    vabasicinfo.service_name,
    vabasicinfo.language,
    vabasicinfo.user_oa_number,
    vabasicinfo.user_name,
    vabasicinfo.user_name_roma,
    vabasicinfo.user_mailaddress,
    vabasicinfo.user_company_code,
    vabasicinfo.user_company_name,
    vabasicinfo.user_company_name_en,
    vabasicinfo.user_organization_code,
    vabasicinfo.user_organization_name,
    vabasicinfo.user_organization_name_en,
    vabasicinfo.manager_oa_number,
    vabasicinfo.manager_name,
    vabasicinfo.manager_name_roma,
    vabasicinfo.manager_mailaddress,
    vabasicinfo.manager_company_code,
    vabasicinfo.manager_company_name,
    vabasicinfo.manager_company_name_en,
    vabasicinfo.manager_organization_code,
    vabasicinfo.manager_organization_name,
    vabasicinfo.manager_organization_name_en,
    vabasicinfo.dl_user_oa_number,
    vabasicinfo.dl_manager_oa_number,
    vabasicinfo.plan_name,
    vabasicinfo.unit_price,
    vabasicinfo.provided_cost_center_code,
    vabasicinfo.provided_cost_center_name,
    vabasicinfo.expense_details_code,
    vabasicinfo.expense_details_name,
    usb_device_usage_type_candidate_row.master_value AS usb_device_usage_type,
    usb_device_usage_reason_candidate_row.master_value AS usb_device_usage_reason,
    device_type_candidate_row.master_value AS device_type,
    maker_name_candidate_row.master_value AS maker_name,
    ta_usb_device_registration.maker_name_manual_input,
    model_name_candidate_row.master_value AS model_name,
    ta_usb_device_registration.model_name_manual_input,
    ta_usb_device_registration.usb_serial_number,
    ta_usb_device_registration.work_name,
    ta_usb_device_registration.handling_data_content,
    ta_usb_device_registration.external_storage_device_required_reason,
    ta_usb_device_registration.usb_device_usage_type_master_id,
    ta_usb_device_registration.usb_device_usage_type_column_id,
    ta_usb_device_registration.usb_device_usage_type_id,
    ta_usb_device_registration.usb_device_usage_reason_master_id,
    ta_usb_device_registration.usb_device_usage_reason_column_id,
    ta_usb_device_registration.usb_device_usage_reason_id,
    ta_usb_device_registration.device_type_master_id,
    ta_usb_device_registration.device_type_column_id,
    ta_usb_device_registration.device_type_id,
    ta_usb_device_registration.maker_name_master_id,
    ta_usb_device_registration.maker_name_column_id,
    ta_usb_device_registration.maker_name_id,
    ta_usb_device_registration.model_name_master_id,
    ta_usb_device_registration.model_name_column_id,
    ta_usb_device_registration.model_name_id
   FROM view_contract_basic_information vabasicinfo
     JOIN trn_contract_usb_device_registration ta_usb_device_registration ON ta_usb_device_registration.contract_number::text = vabasicinfo.contract_number::text
     JOIN mst_service_individual_temporary_master_rows usb_device_usage_type_candidate_row ON usb_device_usage_type_candidate_row.service_individual_temporary_master_id = ta_usb_device_registration.usb_device_usage_type_master_id AND usb_device_usage_type_candidate_row.master_column_id = ta_usb_device_registration.usb_device_usage_type_column_id AND usb_device_usage_type_candidate_row.id = ta_usb_device_registration.usb_device_usage_type_id AND usb_device_usage_type_candidate_row.row_language = vabasicinfo.language
     JOIN mst_service_individual_temporary_master_rows usb_device_usage_reason_candidate_row ON usb_device_usage_reason_candidate_row.service_individual_temporary_master_id = ta_usb_device_registration.usb_device_usage_reason_master_id AND usb_device_usage_reason_candidate_row.master_column_id = ta_usb_device_registration.usb_device_usage_reason_column_id AND usb_device_usage_reason_candidate_row.id = ta_usb_device_registration.usb_device_usage_reason_id AND usb_device_usage_reason_candidate_row.row_language = vabasicinfo.language
     JOIN mst_service_individual_temporary_master_rows device_type_candidate_row ON device_type_candidate_row.service_individual_temporary_master_id = ta_usb_device_registration.device_type_master_id AND device_type_candidate_row.master_column_id = ta_usb_device_registration.device_type_column_id AND device_type_candidate_row.id = ta_usb_device_registration.device_type_id AND device_type_candidate_row.row_language = vabasicinfo.language
     JOIN mst_service_individual_temporary_master_rows maker_name_candidate_row ON maker_name_candidate_row.service_individual_temporary_master_id = ta_usb_device_registration.maker_name_master_id AND maker_name_candidate_row.master_column_id = ta_usb_device_registration.maker_name_column_id AND maker_name_candidate_row.id = ta_usb_device_registration.maker_name_id AND maker_name_candidate_row.row_language = vabasicinfo.language
     JOIN mst_service_individual_temporary_master_rows model_name_candidate_row ON model_name_candidate_row.service_individual_temporary_master_id = ta_usb_device_registration.model_name_master_id AND model_name_candidate_row.master_column_id = ta_usb_device_registration.model_name_column_id AND model_name_candidate_row.id = ta_usb_device_registration.model_name_id AND model_name_candidate_row.row_language = vabasicinfo.language
  WHERE vabasicinfo.service_id = 76
  ORDER BY vabasicinfo.contract_number, vabasicinfo.language;
  
  
view_contract_usb_device_registration
OK view_contract_basic_information
OK trn_contract_usb_device_registration
OK mst_service_individual_temporary_master_rows
    

