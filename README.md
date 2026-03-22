# Pipeline de Faturamento de Clubes

ETL completo para processar dados de faturamento, gerar KPIs e armazenar no PostgreSQL.

## Estrutura
```
.
├── limpeza.py
├── padronizacao.py
├── Gerando_KPIs.py
├── Import_CSV_PostgreSQL.py
├── Import_KPIs_PostgreSQL.py
├── teste_conexao.py
├── POSTGRESQL.sql
└── .env
```

## Dependências
```bash
pip install pandas psycopg2-binary sqlalchemy python-dotenv
```

Python 3.8+ e PostgreSQL 12+.

## Configuração

Crie o `.env` na raiz:
```env
INPUT_CSV=./data/faturamento_padronizado.csv
OUTPUT_DIR=./data/kpis
CSV_PATH=./data/faturamento_padronizado.csv

POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nome_do_banco

PG_USER=seu_usuario
PG_PASSWORD=sua_senha
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=nome_do_banco
TABLE_NAME=faturamento_total
```

## Como rodar

**1. Preparar os dados**
```bash
python limpeza.py
python padronizacao.py
```

**2. Gerar KPIs**
```bash
python Gerando_KPIs.py
```

Gera em `./data/kpis/`: `kpi_total_clube.csv`, `kpi_total_estado.csv`, `kpi_media_anual.csv`, `kpi_yoy.csv`, `kpi_cagr.csv`.

**3. Criar tabelas no banco**
```bash
psql -U seu_usuario -d nome_do_banco -f POSTGRESQL.sql
```

**4. Testar conexão**
```bash
python teste_conexao.py
```

**5. Importar dados**
```bash
python Import_CSV_PostgreSQL.py
python Import_KPIs_PostgreSQL.py
```

## Tabelas

- `faturamento_total` — dados brutos
- `kpi_total_clube` — total por clube
- `kpi_total_estado` — total por estado
- `kpi_media_anual` — média anual por clube
- `kpi_cagr` — crescimento anual composto
- `kpi_yoy` — crescimento ano a ano

## Queries úteis
```sql
-- top 10 por faturamento
SELECT clube, to_char(total_faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_clube ORDER BY total_faturamento DESC LIMIT 10;

-- maior crescimento
SELECT clube, REPLACE(TO_CHAR(cagr * 100, 'FM990D99'), '.', ',') || '%' AS crescimento
FROM kpi_cagr WHERE cagr IS NOT NULL ORDER BY cagr DESC LIMIT 10;
```

O `POSTGRESQL.sql` tem queries prontas pra ranking, participação percentual, comparação com média, faixas de faturamento e análise de CAGR.

## Observações

- `Import_CSV_PostgreSQL.py` usa `if_exists="replace"` — sobrescreve os dados a cada execução
- O `.env` não é versionado, não sobe pro GitHub
