# 📊 Pipeline de Análise de Faturamento de Clubes

Sistema completo de ETL e análise de dados de faturamento de clubes brasileiros, com geração de KPIs e armazenamento em PostgreSQL.

## 🎯 Visão Geral

Este projeto processa dados de faturamento de clubes, gera indicadores-chave de performance (KPIs) e armazena os resultados em um banco de dados PostgreSQL para análise.

## 📁 Estrutura do Projeto

```
.
├── limpeza.py                    # Limpeza inicial dos dados
├── padronizacao.py               # Padronização de colunas e valores
├── Gerando_KPIs.py              # Geração dos KPIs principais
├── Import_CSV_PostgreSQL.py     # Upload do CSV completo para PostgreSQL
├── Import_KPIs_PostgreSQL.py    # Upload dos KPIs para PostgreSQL
├── teste_conexao.py             # Teste de conexão com o banco
├── POSTGRESQL.sql               # Queries SQL para análise
└── .env                         # Variáveis de ambiente (não versionado)
```

## 🚀 Funcionalidades

### 1️⃣ Limpeza de Dados (`limpeza.py`)
- Conversão de tipos de dados
- Padronização de valores de faturamento
- Ordenação por ano e faturamento

### 2️⃣ Padronização (`padronizacao.py`)
- Remoção de acentos e caracteres especiais
- Normalização de nomes de colunas
- Conversão de valores monetários

### 3️⃣ Geração de KPIs (`Gerando_KPIs.py`)
Gera os seguintes indicadores:

- **Total por Clube**: Faturamento acumulado de cada clube
- **Total por Estado**: Faturamento agregado por estado
- **Média Anual**: Média de faturamento anual por clube
- **YoY (Year over Year)**: Crescimento percentual ano a ano
- **CAGR**: Taxa de crescimento anual composta

### 4️⃣ Importação para PostgreSQL
- Upload de dados brutos (`Import_CSV_PostgreSQL.py`)
- Upload de KPIs calculados (`Import_KPIs_PostgreSQL.py`)

## ⚙️ Configuração

### Pré-requisitos

```bash
Python 3.8+
PostgreSQL 12+
```

### Instalação de Dependências

```bash
pip install pandas psycopg2-binary sqlalchemy python-dotenv
```

### Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações de Input/Output
INPUT_CSV=./data/faturamento_padronizado.csv
OUTPUT_DIR=./data/kpis
CSV_PATH=./data/faturamento_padronizado.csv

# Configurações do PostgreSQL
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nome_do_banco

# Aliases para compatibilidade
PG_USER=seu_usuario
PG_PASSWORD=sua_senha
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=nome_do_banco
TABLE_NAME=faturamento_total
```

## 📋 Como Usar

### Passo 1: Preparar os Dados

```bash
# 1. Limpar dados brutos
python limpeza.py

# 2. Padronizar o arquivo limpo
python padronizacao.py
```

### Passo 2: Gerar KPIs

```bash
python Gerando_KPIs.py
```

Arquivos gerados em `./data/kpis/`:
- `kpi_total_clube.csv`
- `kpi_total_estado.csv`
- `kpi_media_anual.csv`
- `kpi_yoy.csv`
- `kpi_cagr.csv`

### Passo 3: Configurar Banco de Dados

Execute o script SQL para criar as tabelas:

```bash
psql -U seu_usuario -d nome_do_banco -f POSTGRESQL.sql
```

### Passo 4: Testar Conexão

```bash
python teste_conexao.py
```

### Passo 5: Importar Dados

```bash
# Importar dados brutos
python Import_CSV_PostgreSQL.py

# Importar KPIs
python Import_KPIs_PostgreSQL.py
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Criadas

- `faturamento_total`: Dados brutos de faturamento
- `kpi_total_clube`: Total por clube
- `kpi_total_estado`: Total por estado
- `kpi_media_anual`: Média anual por clube
- `kpi_cagr`: Taxa de crescimento composta
- `kpi_yoy`: Crescimento ano a ano

## 📊 Análises Disponíveis (SQL)

O arquivo `POSTGRESQL.sql` contém queries prontas para:

- ✅ Ranking de clubes por faturamento
- ✅ Participação percentual de cada clube
- ✅ Comparação com média geral
- ✅ Categorização por faixa de faturamento
- ✅ Clubes com alto crescimento
- ✅ Análise de CAGR
- ✅ Formatação de valores em R$

## 🔍 Exemplos de Queries

```sql
-- Top 10 clubes por faturamento
SELECT 
    clube,
    to_char(total_faturamento, 'L999G999G999G990D00') AS faturamento
FROM kpi_total_clube
ORDER BY total_faturamento DESC
LIMIT 10;

-- Clubes com maior crescimento
SELECT
    clube,
    REPLACE(TO_CHAR(cagr * 100, 'FM990D99'), '.', ',') || '%' AS crescimento
FROM kpi_cagr
WHERE cagr IS NOT NULL
ORDER BY cagr DESC
LIMIT 10;
```

## 🛠️ Tratamento de Erros

O sistema inclui:
- Validação de variáveis de ambiente obrigatórias
- Tratamento de erros de conexão
- Mensagens claras de erro
- Verificação de existência de arquivos

## 📝 Notas Importantes

- Configure TODOS os caminhos nos arquivos antes de executar
- O arquivo `.env` NÃO deve ser versionado (adicione ao `.gitignore`)
- Certifique-se de ter permissões adequadas no PostgreSQL
- O script `Import_CSV_PostgreSQL.py` usa `if_exists="replace"` (sobrescreve dados)



## 📄 Licença

Este projeto está sob licença MIT.
