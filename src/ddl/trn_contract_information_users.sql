-- public.trn_contract_information_users definition

-- Drop table

-- DROP TABLE public.trn_contract_information_users;

CREATE TABLE public.trn_contract_information_users (
	contract_number varchar NOT NULL,
	user_oa_number varchar NOT NULL,
	user_department varchar NULL,
	user_phone varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT trn_contract_information_users_pkey PRIMARY KEY (contract_number, user_oa_number)
);
CREATE INDEX idx_contract_information_users_01 ON public.trn_contract_information_users USING btree (user_oa_number);