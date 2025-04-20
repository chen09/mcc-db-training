
CREATE MATERIALIZED VIEW view_invoice_address_company_info AS
SELECT 
    id,
    row_language,
    service_individual_temporary_master_id,
    MAX(CASE WHEN master_column_id = 34 THEN master_value END) AS invoice_address_company_code,
    MAX(CASE WHEN master_column_id = 35 THEN master_value END) AS invoice_address_company_name
FROM 
    mst_service_individual_temporary_master_rows
WHERE 
    service_individual_temporary_master_id = 20
GROUP BY 
    id,
    row_language,
    service_individual_temporary_master_id
WITH DATA;

-- インデックスの作成
CREATE UNIQUE INDEX idx_view_invoice_address_company_info_id 
ON view_invoice_address_company_info(id);

-- コメントの追加
COMMENT ON MATERIALIZED VIEW view_invoice_address_company_info IS '請求先会社情報マテリアライズドビュー';
COMMENT ON COLUMN view_invoice_address_company_info.invoice_address_company_code IS '請求先会社コード';
COMMENT ON COLUMN view_invoice_address_company_info.invoice_address_company_name IS '請求先会社名';

-- リフレッシュ用の関数
CREATE OR REPLACE FUNCTION refresh_view_invoice_address_company_info()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY view_invoice_address_company_info;
END;
$$ LANGUAGE plpgsql; 