-- public.trn_contract_basic_information definition

-- Drop table

-- DROP TABLE public.trn_contract_basic_information;

CREATE TABLE public.trn_contract_basic_information (
	contract_number varchar NOT NULL,
	contract_status int4 NOT NULL,
	latest_apply_number varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	service_id int4 NULL,
	versatile_remarks1 varchar NULL,
	versatile_remarks2 varchar NULL,
	versatile_remarks3 varchar NULL,
	versatile_remarks4 varchar NULL,
	versatile_remarks5 varchar NULL,
	remarks varchar NULL,
	usage_start_date timestamptz NULL,
	usage_end_date timestamptz NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	desired_start_date timestamptz NULL,
	scheduled_end_date timestamptz NULL,
	bill_to_company_code varchar NULL,
	cost_center_code varchar NULL,
	invoice_address_company_code_master_id int4 NULL,
	invoice_address_company_code_column_id int4 NULL,
	invoice_address_company_code_id int4 NULL,
	service_plan_id int4 NULL,
	CONSTRAINT trn_contract_basic_information_pkey PRIMARY KEY (contract_number)
);
CREATE INDEX ix_trn_contract_basic_information_latest_apply_number ON public.trn_contract_basic_information USING btree (latest_apply_number);