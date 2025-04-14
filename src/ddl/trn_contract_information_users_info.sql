CREATE TABLE public.trn_contract_information_users_info (
    contract_number VARCHAR(50) NOT NULL,
    user_oa_number VARCHAR(50) NOT NULL,
    user_detail_id INTEGER NOT NULL,
    user_name VARCHAR(100),
    user_name_roma VARCHAR(100),
    mailaddress VARCHAR(255),
    company_code VARCHAR(20),
    company_name VARCHAR(100),
    company_name_en VARCHAR(100),
    organization_code VARCHAR(20),
    organization_name VARCHAR(100),
    organization_name_en VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    created_pg_id VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL,
    updated_pg_id VARCHAR(50) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT pk_contract_users_info PRIMARY KEY (contract_number, user_oa_number, user_detail_id)
);

-- インデックスの作成
CREATE INDEX idx_contract_users_info_oa_number ON public.trn_contract_information_users_info(user_oa_number);
CREATE INDEX idx_contract_users_info_company_code ON public.trn_contract_information_users_info(company_code);
CREATE INDEX idx_contract_users_info_org_code ON public.trn_contract_information_users_info(organization_code);

-- コメントの追加
COMMENT ON TABLE public.trn_contract_information_users_info IS '契約ユーザー情報テーブル';
COMMENT ON COLUMN public.trn_contract_information_users_info.contract_number IS '契約番号';
COMMENT ON COLUMN public.trn_contract_information_users_info.user_oa_number IS 'ユーザーOA番号';
COMMENT ON COLUMN public.trn_contract_information_users_info.user_detail_id IS 'ユーザー詳細ID';
COMMENT ON COLUMN public.trn_contract_information_users_info.user_name IS 'ユーザー名';
COMMENT ON COLUMN public.trn_contract_information_users_info.user_name_roma IS 'ユーザー名（ローマ字）';
COMMENT ON COLUMN public.trn_contract_information_users_info.mailaddress IS 'メールアドレス';
COMMENT ON COLUMN public.trn_contract_information_users_info.company_code IS '会社コード';
COMMENT ON COLUMN public.trn_contract_information_users_info.company_name IS '会社名';
COMMENT ON COLUMN public.trn_contract_information_users_info.company_name_en IS '会社名（英語）';
COMMENT ON COLUMN public.trn_contract_information_users_info.organization_code IS '組織コード';
COMMENT ON COLUMN public.trn_contract_information_users_info.organization_name IS '組織名';
COMMENT ON COLUMN public.trn_contract_information_users_info.organization_name_en IS '組織名（英語）'; 