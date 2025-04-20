-- public.view_manager_info source

CREATE MATERIALIZED VIEW public.view_manager_info
TABLESPACE pg_default
AS SELECT tcinfomanagers.contract_number,
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
WITH DATA;

-- View indexes:
CREATE INDEX idx_view_manager_info_contract ON public.view_manager_info USING btree (contract_number);