-- public.trn_contract_usb_device_registration definition

-- Drop table

-- DROP TABLE public.trn_contract_usb_device_registration;

CREATE TABLE public.trn_contract_usb_device_registration (
	contract_number varchar NOT NULL,
	usb_device_usage_type_master_id int4 NOT NULL,
	usb_device_usage_type_column_id int4 NOT NULL,
	usb_device_usage_type_id int4 NOT NULL,
	usb_device_usage_reason_master_id int4 NOT NULL,
	usb_device_usage_reason_column_id int4 NOT NULL,
	usb_device_usage_reason_id int4 NOT NULL,
	device_type_master_id int4 NOT NULL,
	device_type_column_id int4 NOT NULL,
	device_type_id int4 NOT NULL,
	maker_name_master_id int4 NOT NULL,
	maker_name_column_id int4 NOT NULL,
	maker_name_id int4 NOT NULL,
	maker_name_manual_input varchar NULL,
	model_name_master_id int4 NOT NULL,
	model_name_column_id int4 NOT NULL,
	model_name_id int4 NOT NULL,
	model_name_manual_input varchar NULL,
	usb_serial_number varchar NOT NULL,
	created_at timestamptz NOT NULL,
	created_by varchar NOT NULL,
	created_pg_id varchar NOT NULL,
	updated_at timestamptz NOT NULL,
	updated_by varchar NOT NULL,
	updated_pg_id varchar NOT NULL,
	"version" int4 NOT NULL,
	handling_data_content varchar NOT NULL,
	external_storage_device_required_reason varchar NOT NULL,
	work_name varchar NOT NULL
);


-- public.trn_contract_usb_device_registration foreign keys