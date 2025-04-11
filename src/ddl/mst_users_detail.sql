-- public.mst_users_detail definition

-- Drop table

-- DROP TABLE public.mst_users_detail;

CREATE TABLE public.mst_users_detail (
	id serial4 NOT NULL,
	oa_number varchar NOT NULL,
	business varchar NOT NULL,
	company_code varchar NOT NULL,
	company_name varchar NULL,
	organization_code varchar NOT NULL,
	organization_name varchar NULL,
	"member" varchar NULL,
	position_code varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	company_name_en varchar NULL,
	organization_name_en varchar NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT mst_users_detail_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_mst_users_detail_oa_number ON public.mst_users_detail USING btree (oa_number);