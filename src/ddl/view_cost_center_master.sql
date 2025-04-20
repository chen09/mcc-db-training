CREATE MATERIALIZED VIEW view_cost_center_master AS
SELECT 
    id,
    row_language,
    service_individual_temporary_master_id,
    MAX(CASE WHEN master_column_id = 36 THEN master_value END) AS bill_to_company_code,
    MAX(CASE WHEN master_column_id = 37 THEN master_value END) AS company_name,
    MAX(CASE WHEN master_column_id = 38 THEN master_value END) AS kaisha_code
FROM 
    mst_service_individual_temporary_master_rows
WHERE 
    service_individual_temporary_master_id = 21
GROUP BY 
    id,
    row_language,
    service_individual_temporary_master_id
WITH DATA;

-- インデックスの作成
CREATE UNIQUE INDEX idx_view_cost_center_master_id 
ON view_cost_center_master(id);

CREATE INDEX idx_view_cost_center_master_bill_code 
ON view_cost_center_master(bill_to_company_code);

CREATE INDEX idx_view_cost_center_master_kaisha_code 
ON view_cost_center_master(kaisha_code);

-- コメントの追加
COMMENT ON MATERIALIZED VIEW view_cost_center_master IS '原価センタマスタマテリアライズドビュー';
COMMENT ON COLUMN view_cost_center_master.bill_to_company_code IS '請求先会社コード';
COMMENT ON COLUMN view_cost_center_master.company_name IS '会社名';
COMMENT ON COLUMN view_cost_center_master.kaisha_code IS '会計会社コード';

-- リフレッシュ用の関数
CREATE OR REPLACE FUNCTION refresh_view_cost_center_master()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY view_cost_center_master;
END;
$$ LANGUAGE plpgsql; 