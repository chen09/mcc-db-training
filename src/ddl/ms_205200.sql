-- public.ms_205200 definition

-- Drop table

-- DROP TABLE public.ms_205200;

CREATE TABLE public.ms_205200 (
	kaisha_code varchar NOT NULL,
	cost_center_c varchar NOT NULL,
	start_date varchar NOT NULL,
	end_date varchar NOT NULL,
	cost_center_name varchar NOT NULL,
	business_area_c varchar NOT NULL,
	cost_center_type varchar NOT NULL,
	profit_center_c varchar NOT NULL,
	nozeiti_c varchar NULL,
	tanpo_kbn varchar NULL,
	object_version int4 NOT NULL,
	delete_flg varchar NOT NULL,
	update_ymd timestamp NOT NULL,
	CONSTRAINT ms_205200_pkey PRIMARY KEY (kaisha_code, cost_center_c, start_date)
);