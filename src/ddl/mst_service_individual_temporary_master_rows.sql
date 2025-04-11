-- public.mst_service_individual_temporary_master_rows definition

-- Drop table

-- DROP TABLE public.mst_service_individual_temporary_master_rows;

CREATE TABLE public.mst_service_individual_temporary_master_rows (
	id int4 NOT NULL,
	row_language int4 NOT NULL,
	service_individual_temporary_master_id int4 NOT NULL,
	master_column_id int4 NOT NULL,
	master_value varchar NULL,
	usage_start_date timestamptz NULL,
	usage_end_date timestamptz NULL,
	display_order int4 NULL,
	created_at timestamptz NOT NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_at timestamptz NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	CONSTRAINT mst_service_individual_temporary_master_rows_pkey PRIMARY KEY (id, row_language, service_individual_temporary_master_id, master_column_id)
);


-- public.mst_service_individual_temporary_master_rows foreign keys

ALTER TABLE public.mst_service_individual_temporary_master_rows ADD CONSTRAINT mst_service_individual_tempo_service_individual_temporary_fkey1 FOREIGN KEY (service_individual_temporary_master_id) REFERENCES public.mst_service_individual_temporary_masters(id);