-- public.mst_messages definition

-- Drop table

-- DROP TABLE public.mst_messages;

CREATE TABLE public.mst_messages (
	id serial4 NOT NULL,
	"language" int4 NOT NULL,
	message varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT mst_messages_pkey PRIMARY KEY (id,"language")
);