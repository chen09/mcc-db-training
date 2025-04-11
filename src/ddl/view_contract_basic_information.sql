
-- public.view_contract_basic_information source

CREATE OR REPLACE VIEW public.view_contract_basic_information
AS WITH user_info AS (
         SELECT tcinfousers.contract_number,
            string_agg(COALESCE(users.oa_number, tcinfousers.user_oa_number, ''::character varying)::text, ','::text) AS user_oa_number,
            string_agg(COALESCE(users.user_name, ''::character varying)::text, ','::text) AS user_name,
            string_agg(COALESCE(users.user_name_roma, ''::character varying)::text, ','::text) AS user_name_roma,
            string_agg(COALESCE(users.mailaddress, ''::character varying)::text, ','::text) AS user_mailaddress,
            string_agg(COALESCE(usersdetail.company_code, ''::character varying)::text, ','::text) AS user_company_code,
            string_agg(COALESCE(usersdetail.company_name, ''::character varying)::text, ','::text) AS user_company_name,
            string_agg(COALESCE(usersdetail.company_name_en, ''::character varying)::text, ','::text) AS user_company_name_en,
            string_agg(COALESCE(usersdetail.organization_code, ''::character varying)::text, ','::text) AS user_organization_code,
            string_agg(COALESCE(usersdetail.organization_name, ''::character varying)::text, ','::text) AS user_organization_name,
            string_agg(COALESCE(usersdetail.organization_name_en, ''::character varying)::text, ','::text) AS user_organization_name_en,
            string_agg(DISTINCT COALESCE(tcinfousers.user_oa_number, ''::character varying)::text, ','::text) AS dl_user_oa_number
           FROM trn_contract_information_users tcinfousers
             LEFT JOIN mst_users users ON tcinfousers.user_oa_number::text = users.oa_number::text
             LEFT JOIN mst_users_detail usersdetail ON tcinfousers.user_oa_number::text = usersdetail.oa_number::text
          GROUP BY tcinfousers.contract_number
        ), manager_info AS (
         SELECT tcinfomanagers.contract_number,
            string_agg(COALESCE(managers.oa_number, tcinfomanagers.manager_oa_number, ''::character varying)::text, ','::text) AS manager_oa_number,
            string_agg(COALESCE(managers.user_name, ''::character varying)::text, ','::text) AS manager_name,
            string_agg(COALESCE(managers.user_name_roma, ''::character varying)::text, ','::text) AS manager_name_roma,
            string_agg(COALESCE(managers.mailaddress, ''::character varying)::text, ','::text) AS manager_mailaddress,
            string_agg(COALESCE(managersdetail.company_code, ''::character varying)::text, ','::text) AS manager_company_code,
            string_agg(COALESCE(managersdetail.company_name, ''::character varying)::text, ','::text) AS manager_company_name,
            string_agg(COALESCE(managersdetail.company_name_en, ''::character varying)::text, ','::text) AS manager_company_name_en,
            string_agg(COALESCE(managersdetail.organization_code, ''::character varying)::text, ','::text) AS manager_organization_code,
            string_agg(COALESCE(managersdetail.organization_name, ''::character varying)::text, ','::text) AS manager_organization_name,
            string_agg(COALESCE(managersdetail.organization_name_en, ''::character varying)::text, ','::text) AS manager_organization_name_en,
            string_agg(DISTINCT COALESCE(tcinfomanagers.manager_oa_number, ''::character varying)::text, ','::text) AS dl_manager_oa_number
           FROM trn_contract_information_managers tcinfomanagers
             LEFT JOIN mst_users managers ON tcinfomanagers.manager_oa_number::text = managers.oa_number::text
             LEFT JOIN mst_users_detail managersdetail ON tcinfomanagers.manager_oa_number::text = managersdetail.oa_number::text
          GROUP BY tcinfomanagers.contract_number
        ), cost_center_info AS (
         SELECT ms_205200.kaisha_code,
            ms_205200.cost_center_c,
            ms_205200.cost_center_name,
            row_number() OVER (PARTITION BY ms_205200.kaisha_code, ms_205200.cost_center_c ORDER BY ms_205200.start_date DESC) AS row_number
           FROM ms_205200
          WHERE ms_205200.start_date::text <= to_char(now(), 'YYYYMMDD'::text) AND ms_205200.end_date::text >= to_char(now(), 'YYYYMMDD'::text)
        )
 SELECT tcbasicinfo.contract_number,
    tcbasicinfo.contract_status,
    tcbasicinfo.service_id,
    tcbasicinfo.usage_start_date,
    tcbasicinfo.usage_end_date,
    tcbasicinfo.desired_start_date,
    tcbasicinfo.scheduled_end_date,
    tcbasicinfo.latest_apply_number,
    tcbasicinfo.bill_to_company_code,
    bill_organizations.organization_shortened_name AS bill_to_company_name,
    mrow.master_value AS invoice_address_company_code,
    mrow2.master_value AS invoice_address_company_name,
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
     LEFT JOIN user_info ui ON tcbasicinfo.contract_number::text = ui.contract_number::text
     LEFT JOIN manager_info mi ON tcbasicinfo.contract_number::text = mi.contract_number::text
     LEFT JOIN mst_organizations bill_organizations ON tcbasicinfo.bill_to_company_code::text = bill_organizations.organization_code::text AND bill_organizations.organization_level::text = '1'::text
     LEFT JOIN mst_service_individual_temporary_master_rows mrow ON tcbasicinfo.invoice_address_company_code_master_id = mrow.service_individual_temporary_master_id AND tcbasicinfo.invoice_address_company_code_column_id = mrow.master_column_id AND tcbasicinfo.invoice_address_company_code_id = mrow.id
     LEFT JOIN mst_service_individual_temporary_master_rows mrow2 ON tcbasicinfo.invoice_address_company_code_master_id = mrow2.service_individual_temporary_master_id AND tcbasicinfo.invoice_address_company_code_id = mrow2.id AND mrow2.master_column_id = 35
     LEFT JOIN mst_service_individual_temporary_master_rows mrow3 ON mrow3.service_individual_temporary_master_id = 21 AND mrow3.master_value::text = tcbasicinfo.bill_to_company_code::text AND mrow3.master_column_id = 36
     LEFT JOIN mst_service_individual_temporary_master_rows mrow4 ON mrow4.service_individual_temporary_master_id = 21 AND mrow4.master_column_id = 38 AND mrow4.id = mrow3.id
     LEFT JOIN cost_center_info cci ON cci.kaisha_code::text = mrow4.master_value::text AND cci.cost_center_c::text = tcbasicinfo.cost_center_code::text AND cci.row_number = 1
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
OK - mst_service_individual_temporary_master_rows (mrow, mrow2, mrow3, mrow4)
OK - ms_205200 (コストセンター情報)

