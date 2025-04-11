-- public.mst_users definition

-- Drop table

-- DROP TABLE public.mst_users;

CREATE TABLE public.mst_users (
	oa_number varchar NOT NULL,
	mailaddress varchar NULL,
	user_name varchar NOT NULL,
	user_name_roma varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT mst_users_pkey PRIMARY KEY (oa_number)
);
CREATE INDEX ix_mst_users_user_name ON public.mst_users USING btree (user_name);
CREATE INDEX ix_mst_users_user_name_roma ON public.mst_users USING btree (user_name_roma);