--- CRIANDO TABELAS ----

DROP TABLE IF EXISTS kpi_yoy;
DROP TABLE IF EXISTS kpi_cagr;
DROP TABLE IF EXISTS kpi_media_anual;
DROP TABLE IF EXISTS kpi_total_estado;
DROP TABLE IF EXISTS kpi_total_clube;


CREATE TABLE kpi_total_clube (
    id SERIAL PRIMARY KEY,
    clube VARCHAR(100),
    faturamento NUMERIC
);

CREATE TABLE kpi_total_estado (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(50),
    faturamento NUMERIC
);

CREATE TABLE kpi_media_anual (
    id SERIAL PRIMARY KEY,
    clube VARCHAR(100),
    faturamento NUMERIC
);

CREATE TABLE kpi_cagr (
    id SERIAL PRIMARY KEY,
    clube VARCHAR(100),
    cagr NUMERIC
);

CREATE TABLE kpi_yoy (
    id SERIAL PRIMARY KEY,
    clube VARCHAR(100),
    estado VARCHAR(50),
    ano INTEGER,
    faturamento NUMERIC,
    yoy NUMERIC
);


DROP TABLE IF EXISTS kpi_total_clube;


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'kpi_total_clube';



--- VERIFICANDO SE A TABELA FOI CRIADA
SELECT *
FROM information_schema.tables
WHERE table_name = 'faturamento_total';


--- CONTEUDO DA TABELA
SELECT *
FROM faturamento_total
LIMIT 20;


--- QUANTAS LINHAS FORAM INSERIDAS
SELECT COUNT(*) AS total_registros
FROM faturamento_total;


-- CADA TIPO DE CADA COLUNA (IMPORTANTE)
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'faturamento_total';

---- FATURAMENTOS EM R$ (ESPECIFICO PQ O FATURAMENTO ESTA EM DOUBLE PRECISION)
SELECT 
    clube AS time,
    'R$ ' || TO_CHAR(faturamento::numeric, 'FM999G999G999G990D00') AS faturamento
FROM faturamento_total;

---- #### KPIs #### ----


--- VALORES EM R$ 
SELECT 
    clube,
    to_char(total_faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_clube
ORDER BY total_faturamento DESC
LIMIT 5;




-- TABELA 2: KPI TOTAL POR ESTADO
--- OS ESTADOS QUE MAIS FATURARAM
SELECT estado, faturamento
FROM kpi_total_estado
ORDER BY faturamento DESC
LIMIT 5;
-- VALOR EM R$
SELECT 
    estado,
    to_char(faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_estado
ORDER BY faturamento DESC
LIMIT 5;




-- TABELA 3: KPI MÉDIA ANUAL POR CLUBE
--- OS 5 MAIORES DE MEDIA ANUAL
SELECT clube, faturamento
FROM kpi_media_anual
ORDER BY  faturamento DESC
LIMIT 5;
-- VALOR EM R$
SELECT 
    clube,
    to_char(faturamento, 'L999G999G999G990D00') AS media_anual
FROM kpi_media_anual
ORDER BY faturamento DESC
LIMIT 5;



-- TABELA 4: KPI CAGR POR CLUBE (TAXA DE CRESCIMENTO MÉDIO ANUAL)
--- OS 5 MAIORES CAGR 
SELECT clube, cagr
FROM kpi_cagr
WHERE cagr IS NOT NULL
ORDER BY cagr ASC
LIMIT 5;
--- CRESCIMENTO EM %
SELECT 
    clube,
    to_char(cagr, 'FM999G999G990D00%') AS percentual_crescimento
FROM kpi_cagr
WHERE cagr IS NOT NULL
ORDER BY cagr ASC
LIMIT 10;

---- CALCULO DE CAGR ---- 
WITH base AS (
    SELECT 
        clube,
        MIN(ano) AS ano_inicial,
        MAX(ano) AS ano_final
    FROM faturamento_total
    GROUP BY clube
),
valores AS (
    SELECT 
        f.clube,

-- Valor INICIAL FORMATADO EM R$
        'R$ ' || 
        REPLACE(
            REPLACE(
                TO_CHAR(f.faturamento::numeric, 'FM999G999G999G990D00'),
                '.', ','
            ),
            ',', '.'
        ) AS valor_inicial,

-- VALOR FINAL FORMATADO EM R$
        'R$ ' ||
        REPLACE(
            REPLACE(
                TO_CHAR(f2.faturamento::numeric, 'FM999G999G999G990D00'),
                '.', ','
            ),
            ',', '.'
        ) AS valor_final,

        (b.ano_final - b.ano_inicial) AS anos
    FROM base b
    JOIN faturamento_total f 
        ON f.clube = b.clube AND f.ano = b.ano_inicial
    JOIN faturamento_total f2
        ON f2.clube = b.clube AND f2.ano = b.ano_final
)
SELECT * FROM valores;



-- TABELA 5: FATURAMENTO TOTAL DOS TIMES
SELECT clube, total_faturamento
FROM kpi_total_clube
ORDER BY total_faturamento DESC;
---- OS 5 TIMES QUE MAIS FATURARAM
SELECT clube, total_faturamento
FROM kpi_total_clube
ORDER BY total_faturamento DESC
LIMIT 10;
--- VALOR EM R$
SELECT 
    clube,
    to_char(total_faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_clube
ORDER BY total_faturamento DESC
LIMIT 20;

---- VALOR TOTAL ARRECADADO EM R$
SELECT
    clube AS time,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999,999,999,999.00') AS valor_arrecadado
FROM kpi_total_clube;




----- RANKING FATURAMENTO
SELECT
    clube,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999G999G999G990D00') AS faturamento,
    RANK() OVER (ORDER BY total_faturamento DESC) AS ranking
FROM kpi_total_clube;


---- % DE PARTICIPAÇÃO (O QUANTO CADA CLUBE REPRESENTA DO FATURAMENTO TOTAL DE TODOS ELES)
SELECT
    clube,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999G999G999G990D00') AS faturamento,
    TO_CHAR(
        ROUND(total_faturamento / SUM(total_faturamento) OVER() * 100, 2),
        'FM999G990D00"%"'
    ) AS percentual_participacao
FROM kpi_total_clube
ORDER BY total_faturamento DESC;


---- CLUBE VS MEDIA GERAL (AVERIGUAR SE O CLUBE FATUROU MAIS OU MENOS QUE A MEDIA)
SELECT
    clube,
    TO_CHAR(total_faturamento, 'L999G999G999G990D00') AS faturamento,
    TO_CHAR((SELECT AVG(total_faturamento) FROM kpi_total_clube), 'L999G999G999G990D00') AS media_geral,
    TO_CHAR(
        total_faturamento - (SELECT AVG(total_faturamento) FROM kpi_total_clube),
        'L999G999G999G990D00'
    ) AS diferenca_da_media
FROM kpi_total_clube
ORDER BY total_faturamento DESC;



---- FAIXA DE FATURAMENTO
SELECT
    clube,
    'R$ ' || TO_CHAR(total_faturamento, 'FM999,999,999,999.00') AS total_faturamento,
    CASE
        WHEN total_faturamento >= 200000000 THEN 'A - Muito Alto'
        WHEN total_faturamento >= 100000000 THEN 'B - Alto'
        WHEN total_faturamento >= 50000000 THEN 'C - Médio'
        ELSE 'D - Baixo'
    END AS categoria_faturamento
FROM kpi_total_clube
ORDER BY total_faturamento DESC;



---- CLUBES QUE FATURAM POUCO MAS CRESCEM RÁPIDO
SELECT
    k.clube,
    'R$ ' || 
    REPLACE(
        REPLACE(TO_CHAR(k.total_faturamento, 'FM999G999G999G990D00'), '.', ','), 
        ',', '.'
    ) AS valor_faturamento,
    REPLACE(TO_CHAR(c.cagr * 100, 'FM990D99'), '.', ',') || '%' AS percentual,
    RANK() OVER (ORDER BY c.cagr DESC) AS rank
FROM kpi_total_clube k
JOIN kpi_cagr c USING(clube)
WHERE c.cagr IS NOT NULL
  AND c.cagr = c.cagr   
ORDER BY c.cagr DESC;

--- CLUBES COM "NAN%" --- NÃO É POSSIVEL CALCULAR O CAGR
SELECT *
FROM kpi_cagr
WHERE clube IN ('Chapecoense', 'Atlético Goianiense');

SELECT *
FROM kpi_total_clube
WHERE clube IN ('Chapecoense', 'Atlético Goianiense');

----- ANOS DE FATURAMENTO ---- 
SELECT clube, COUNT(*) AS anos_registrados
FROM faturamento_total
GROUP BY clube
ORDER BY anos_registrados;