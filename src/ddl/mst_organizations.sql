-- public.mst_organizations definition

-- Drop table

-- DROP TABLE public.mst_organizations;

CREATE TABLE public.mst_organizations (
	organization_code varchar NOT NULL,
	company_code varchar NULL,
	organization_level varchar NULL,
	upper_group_code varchar NULL,
	organization_name varchar NULL,
	organization_formal_name varchar NULL,
	organization_shortened_name varchar NULL,
	company_shortened_name varchar NULL,
	devision_shortened_name varchar NULL,
	department_shortened_name varchar NULL,
	section_shortened_name varchar NULL,
	office_shortened_name varchar NULL,
	team_shortened_name varchar NULL,
	company_abbreviated_name varchar NULL,
	organization_name_en varchar NULL,
	organization_formal_name_en varchar NULL,
	organization_shortened_name_en varchar NULL,
	company_shortened_name_en varchar NULL,
	devision_shortened_name_en varchar NULL,
	department_shortened_name_en varchar NULL,
	section_shortened_name_en varchar NULL,
	office_shortened_name_en varchar NULL,
	team_shortened_name_en varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	comsec_excluded_check bool NULL,
	CONSTRAINT mst_organizations_pkey PRIMARY KEY (organization_code)
);