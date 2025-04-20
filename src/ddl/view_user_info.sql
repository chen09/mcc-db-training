-- public.view_user_info source

CREATE MATERIALIZED VIEW public.view_user_info
TABLESPACE pg_default
AS SELECT tcinfousers.contract_number,
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
WITH DATA;

-- View indexes:
CREATE INDEX idx_view_user_info_contract ON public.view_user_info USING btree (contract_number);