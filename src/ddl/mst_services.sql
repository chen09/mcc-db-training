-- public.mst_services definition

-- Drop table

-- DROP TABLE public.mst_services;

CREATE TABLE public.mst_services (
	id serial4 NOT NULL,
	"type" int4 NOT NULL,
	message_caption_id int4 NOT NULL,
	message_description_id int4 NOT NULL,
	message_attached_file_id int4 NULL,
	tag varchar NULL,
	target_link varchar NULL,
	attached_file_url varchar NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	apply_component_key varchar NULL,
	is_contract_excluded int4 NULL,
	usage_start_date timestamptz NULL,
	usage_end_date timestamptz NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	is_show_apply_for_end_of_use_button int4 DEFAULT 1 NOT NULL,
	is_workflow int4 DEFAULT 0 NOT NULL,
	workflow_application_name varchar NULL,
	is_work_management int4 DEFAULT 0 NOT NULL,
	lead_time_new int4 NULL,
	lead_time_change int4 NULL,
	lead_time_end_of_use int4 NULL,
	is_show_apply_for_change_button int4 DEFAULT 1 NOT NULL,
	is_servicenow int4 DEFAULT 0 NOT NULL,
	servicenow_url_new varchar NULL,
	servicenow_url_change varchar NULL,
	servicenow_url_end_of_use varchar NULL,
	provided_cost_center_code varchar NULL,
	provided_cost_center_name varchar NULL,
	expense_details_code varchar NULL,
	expense_details_name varchar NULL,
	message_new_mail_id int4 NULL,
	message_modify_mail_id int4 NULL,
	message_cancel_mail_id int4 NULL,
	CONSTRAINT mst_services_pkey PRIMARY KEY (id)
);