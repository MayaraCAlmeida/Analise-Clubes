-- criando tabelas

DROP TABLE IF EXISTS kpi_yoy, kpi_cagr, kpi_media_anual, kpi_total_estado, kpi_total_clube;

CREATE TABLE kpi_total_clube  (id SERIAL PRIMARY KEY, clube VARCHAR(100), faturamento NUMERIC);
CREATE TABLE kpi_total_estado (id SERIAL PRIMARY KEY, estado VARCHAR(50),  faturamento NUMERIC);
CREATE TABLE kpi_media_anual  (id SERIAL PRIMARY KEY, clube VARCHAR(100), faturamento NUMERIC);
CREATE TABLE kpi_cagr         (id SERIAL PRIMARY KEY, clube VARCHAR(100), cagr NUMERIC);
CREATE TABLE kpi_yoy          (id SERIAL PRIMARY KEY, clube VARCHAR(100), estado VARCHAR(50), ano INTEGER, faturamento NUMERIC, yoy NUMERIC);


-- verificações gerais

SELECT * FROM information_schema.tables WHERE table_name = 'faturamento_total';
SELECT * FROM faturamento_total LIMIT 20;
SELECT COUNT(*) FROM faturamento_total;
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'faturamento_total';

SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'kpi_total_clube';

-- faturamento formatado em R$
SELECT clube AS time,
    'R$ ' || TO_CHAR(faturamento::numeric, 'FM999G999G999G990D00') AS faturamento
FROM faturamento_total;


-- kpi 1: total por clube
SELECT clube, to_char(total_faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_clube ORDER BY total_faturamento DESC LIMIT 5;

-- kpi 2: total por estado
SELECT estado, to_char(faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_estado ORDER BY faturamento DESC LIMIT 5;

-- kpi 3: média anual por clube
SELECT clube, to_char(faturamento, 'L999G999G999G990D00') AS media_anual
FROM kpi_media_anual ORDER BY faturamento DESC LIMIT 5;

-- kpi 4: cagr
SELECT clube, to_char(cagr, 'FM999G999G990D00%') AS percentual_crescimento
FROM kpi_cagr WHERE cagr IS NOT NULL ORDER BY cagr ASC LIMIT 10;

-- cálculo manual do cagr
WITH base AS (
    SELECT clube, MIN(ano) AS ano_inicial, MAX(ano) AS ano_final
    FROM faturamento_total GROUP BY clube
),
valores AS (
    SELECT f.clube,
        'R$ ' || TO_CHAR(f.faturamento::numeric,  'FM999G999G999G990D00') AS valor_inicial,
        'R$ ' || TO_CHAR(f2.faturamento::numeric, 'FM999G999G999G990D00') AS valor_final,
        (b.ano_final - b.ano_inicial) AS anos
    FROM base b
    JOIN faturamento_total f  ON f.clube  = b.clube AND f.ano  = b.ano_inicial
    JOIN faturamento_total f2 ON f2.clube = b.clube AND f2.ano = b.ano_final
)
SELECT * FROM valores;


-- kpi 5: ranking geral
SELECT clube,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999G999G999G990D00') AS faturamento,
    RANK() OVER (ORDER BY total_faturamento DESC) AS ranking
FROM kpi_total_clube;

-- participação percentual
SELECT clube,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999G999G999G990D00') AS faturamento,
    TO_CHAR(ROUND(total_faturamento / SUM(total_faturamento) OVER() * 100, 2), 'FM999G990D00"%"') AS participacao
FROM kpi_total_clube ORDER BY total_faturamento DESC;

-- clube vs média geral
SELECT clube,
    TO_CHAR(total_faturamento, 'L999G999G999G990D00') AS faturamento,
    TO_CHAR((SELECT AVG(total_faturamento) FROM kpi_total_clube), 'L999G999G999G990D00') AS media_geral,
    TO_CHAR(total_faturamento - (SELECT AVG(total_faturamento) FROM kpi_total_clube), 'L999G999G999G990D00') AS diferenca
FROM kpi_total_clube ORDER BY total_faturamento DESC;

-- faixa de faturamento
SELECT clube,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999,999,999,999.00') AS total_faturamento,
    CASE
        WHEN total_faturamento >= 200000000 THEN 'A - Muito Alto'
        WHEN total_faturamento >= 100000000 THEN 'B - Alto'
        WHEN total_faturamento >= 50000000  THEN 'C - Médio'
        ELSE 'D - Baixo'
    END AS categoria
FROM kpi_total_clube ORDER BY total_faturamento DESC;

-- clubes que faturam pouco mas crescem rápido
SELECT k.clube,
    'R$ ' || TO_CHAR(k.total_faturamento, 'FM999G999G999G990D00') AS faturamento,
    TO_CHAR(c.cagr * 100, 'FM990D99') || '%' AS cagr,
    RANK() OVER (ORDER BY c.cagr DESC) AS rank
FROM kpi_total_clube k
JOIN kpi_cagr c USING(clube)
WHERE c.cagr IS NOT NULL ORDER BY c.cagr DESC;

-- clubes sem cagr calculável
SELECT * FROM kpi_cagr        WHERE clube IN ('Chapecoense', 'Atlético Goianiense');
SELECT * FROM kpi_total_clube WHERE clube IN ('Chapecoense', 'Atlético Goianiense');

-- anos de faturamento por clube
SELECT clube, COUNT(*) AS anos_registrados
FROM faturamento_total GROUP BY clube ORDER BY anos_registrados;
