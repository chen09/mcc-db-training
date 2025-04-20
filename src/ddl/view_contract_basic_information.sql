-- public.view_contract_basic_information source

CREATE OR REPLACE VIEW public.view_contract_basic_information
AS SELECT tcbasicinfo.contract_number,
    tcbasicinfo.contract_status,
    tcbasicinfo.service_id,
    tcbasicinfo.usage_start_date,
    tcbasicinfo.usage_end_date,
    tcbasicinfo.desired_start_date,
    tcbasicinfo.scheduled_end_date,
    tcbasicinfo.latest_apply_number,
    tcbasicinfo.bill_to_company_code,
    bill_organizations.organization_shortened_name AS bill_to_company_name,
    viac.invoice_address_company_code,
    viac.invoice_address_company_name,
    tcbasicinfo.cost_center_code,
    cci.cost_center_name,
    tcbasicinfo.remarks,
    tcbasicinfo.versatile_remarks1,
    tcbasicinfo.versatile_remarks2,
    tcbasicinfo.versatile_remarks3,
    tcbasicinfo.versatile_remarks4,
    tcbasicinfo.versatile_remarks5,
    tcbasicinfo.created_at,
    tcbasicinfo.created_by,
    tcbasicinfo.created_pg_id,
    tcbasicinfo.updated_at,
    tcbasicinfo.updated_by,
    tcbasicinfo.updated_pg_id,
    tcbasicinfo.version,
    services.message_caption_id AS service_caption_id,
    services.apply_component_key,
    messages.message AS service_name,
    messages.language,
    ui.user_oa_number,
    ui.user_name,
    ui.user_name_roma,
    ui.user_mailaddress,
    ui.user_company_code,
    ui.user_company_name,
    ui.user_company_name_en,
    ui.user_organization_code,
    ui.user_organization_name,
    ui.user_organization_name_en,
    mi.manager_oa_number,
    mi.manager_name,
    mi.manager_name_roma,
    mi.manager_mailaddress,
    mi.manager_company_code,
    mi.manager_company_name,
    mi.manager_company_name_en,
    mi.manager_organization_code,
    mi.manager_organization_name,
    mi.manager_organization_name_en,
    ui.dl_user_oa_number,
    mi.dl_manager_oa_number,
    plan_message.message AS plan_name,
    service_plans.unit_price,
    services.provided_cost_center_code,
    services.provided_cost_center_name,
    services.expense_details_code,
    services.expense_details_name
   FROM trn_contract_basic_information tcbasicinfo
     LEFT JOIN mst_services services ON tcbasicinfo.service_id = services.id
     LEFT JOIN mst_service_plans service_plans ON tcbasicinfo.service_plan_id = service_plans.id
     LEFT JOIN mst_messages messages ON services.message_caption_id = messages.id
     LEFT JOIN mst_messages plan_message ON service_plans.message_plan_name_id = plan_message.id AND plan_message.language = messages.language
     LEFT JOIN view_user_info ui ON tcbasicinfo.contract_number::text = ui.contract_number::text
     LEFT JOIN view_manager_info mi ON tcbasicinfo.contract_number::text = mi.contract_number::text
     LEFT JOIN mst_organizations bill_organizations ON tcbasicinfo.bill_to_company_code::text = bill_organizations.organization_code::text AND bill_organizations.organization_level::text = '1'::text
     LEFT JOIN view_invoice_address_company_info viac ON tcbasicinfo.invoice_address_company_code_id = viac.id
     LEFT JOIN view_cost_center_master ccm ON ccm.bill_to_company_code::text = tcbasicinfo.bill_to_company_code::text
     LEFT JOIN view_cost_center_info cci ON cci.kaisha_code::text = ccm.kaisha_code::text AND cci.cost_center_c::text = tcbasicinfo.cost_center_code::text AND cci.row_number = 1
  ORDER BY tcbasicinfo.contract_number, messages.language;


OK - trn_contract_basic_information (tcbasicinfo)
OK - trn_contract_information_users (tcinfousers)
OK - trn_contract_information_managers (tcinfomanagers)
- mst_users (users, managers)
- mst_users_detail (usersdetail, managersdetail)
- mst_services (services)
- mst_service_plans (service_plans)
- mst_messages (messages, plan_message)
- mst_organizations (bill_organizations)
OK - view_invoice_address_company_info (viac)
OK - ms_205200 (コストセンター情報)

