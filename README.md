# Projeto Vendas — Pipeline Medalhão

Pipeline de dados com arquitetura medalhão (Bronze → Silver → Gold) usando dados simulados de vendas de uma empresa fictícia de varejo. O objetivo é transformar arquivos CSV brutos em métricas de negócio prontas para consumo, passando por etapas de ingestão, limpeza e agregação.

## Tecnologias

- Python 3.12
- Polars — transformações de dados nas camadas Bronze e Silver
- PostgreSQL — armazenamento da camada Gold
- Docker — container para o banco de dados
- SQLAlchemy — conexão Python ↔ PostgreSQL
- Parquet — formato intermediário entre camadas

## Arquitetura

```
CSV (raw) → [ingestao.py] → Parquet (bronze) → [silver.py] → Parquet (silver) → [gold.py] → PostgreSQL (gold)
```

**Bronze:** dados brutos sem nenhuma transformação, apenas convertidos de CSV para Parquet.

**Silver:** dados limpos e padronizados — remoção de duplicatas, tratamento de nulos, padronização de texto, conversão de tipos e criação da coluna `valor_total`.

**Gold:** métricas de negócio agregadas — faturamento total, faturamento por mês, top 10 clientes, top 10 produtos e ticket médio.

## Estrutura do Projeto

```
projeto_vendas/
├── data/
│   ├── raw/            ← CSVs originais (entrada)
│   │   ├── clientes.csv
│   │   ├── produtos.csv
│   │   └── vendas.csv
│   ├── bronze/         ← Parquet bruto (saída do ingestao.py)
│   ├── silver/         ← Parquet limpo (saída do silver.py)
│   └── gold/           ← Reservado para exports futuros
├── scripts/
│   ├── ingestao.py     ← Camada Bronze
│   ├── silver.py       ← Camada Silver
│   └── gold.py         ← Camada Gold
├── run_pipeline.py     ← Executa todo o pipeline em ordem
├── .env                ← Credenciais do banco (não versionado)
├── .gitignore
├── README.md
└── requirements.txt
```

## Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- Docker instalado e rodando

### 1. Clonar e configurar o ambiente

```bash
git clone https://github.com/seu-usuario/projeto_vendas.git
cd projeto_vendas
python -m venv venv
```

Ativar o ambiente virtual:

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (cmd)
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

### 2. Subir o banco de dados

```bash
docker run --name db_projeto_vendas_medalion -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=projeto_vendas -p 5432:5432 -d postgres
```

### 3. Configurar as credenciais

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=projeto_vendas
DB_USER=postgres
DB_PASSWORD=1234
```

### 4. Executar o pipeline

Para rodar todo o pipeline de uma vez:

```bash
python run_pipeline.py
```

Ou executar cada camada individualmente:

```bash
# 1. Camada Bronze — ingestão dos CSVs para Parquet
python scripts/ingestao.py

# 2. Camada Silver — limpeza e padronização
python scripts/silver.py

# 3. Camada Gold — geração de métricas no PostgreSQL
python scripts/gold.py
```

## Dados de Entrada

Os CSVs em `data/raw/` possuem problemas de qualidade propositais para exercitar a camada Silver:

| Problema | Onde aparece |
|---|---|
| Linhas duplicadas | clientes, produtos, vendas |
| Valores nulos | emails, cidades, preços, quantidades |
| Texto com caixa inconsistente | nomes de clientes, categorias de produtos |

## Tratamentos Aplicados (Camada Silver)

| Tabela | Tratamento |
|---|---|
| clientes | Nulos preenchidos (email, cidade), duplicatas removidas, texto em maiúsculo |
| produtos | Nulos preenchidos (preço), duplicatas removidas, texto em maiúsculo |
| vendas | Nulos removidos (quantidade), duplicatas removidas, data convertida, `valor_total` criado |

## Métricas Geradas (Camada Gold)

| Tabela no PostgreSQL | Descrição |
|---|---|
| faturamento_total | Soma de todas as vendas |
| faturamento_mensal | Faturamento agrupado por ano e mês |
| top_clientes | Top 10 clientes por valor gasto |
| top_produtos | Top 10 produtos por valor vendido |
| ticket_medio | Total de vendas, faturamento e ticket médio |

## Autor

Davi Monsalves Tunes