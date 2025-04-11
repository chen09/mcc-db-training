-- public.trn_contract_information_managers definition

-- Drop table

-- DROP TABLE public.trn_contract_information_managers;

CREATE TABLE public.trn_contract_information_managers (
	contract_number varchar NOT NULL,
	manager_oa_number varchar NOT NULL,
	manager_department varchar NULL,
	manager_phone varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT trn_contract_information_managers_pkey PRIMARY KEY (contract_number, manager_oa_number)
);
CREATE INDEX idx_contract_information_managers_01 ON public.trn_contract_information_managers USING btree (manager_oa_number);