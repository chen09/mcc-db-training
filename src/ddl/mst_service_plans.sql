-- public.mst_service_plans definition

-- Drop table

-- DROP TABLE public.mst_service_plans;

CREATE TABLE public.mst_service_plans (
	id serial4 NOT NULL,
	service_id int4 NOT NULL,
	unit_price int4 NOT NULL,
	created_at timestamptz NOT NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_at timestamptz NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	message_plan_name_id int4 NOT NULL,
	display_order int4 NULL,
	is_active bool NOT NULL,
	CONSTRAINT mst_service_plans_pkey PRIMARY KEY (id)
);


-- public.mst_service_plans foreign keys

ALTER TABLE public.mst_service_plans ADD CONSTRAINT mst_service_plans_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.mst_services(id);