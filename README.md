# Projeto Vendas — Pipeline Medalhão

Pipeline de dados com arquitetura medalhão (Bronze → Silver → Gold) usando dados simulados de vendas de uma empresa fictícia de varejo. O objetivo é transformar arquivos CSV brutos em métricas de negócio prontas para consumo, passando por etapas de ingestão, limpeza e agregação.

## Tecnologias

- Python 3.12
- Polars — transformações de dados nas camadas Bronze e Silver
- PostgreSQL — armazenamento da camada Gold
- Parquet — formato intermediário entre camadas

## Arquitetura

```
CSV (raw) → [ingestao.py] → Parquet (bronze) → [silver.py] → Parquet (silver) → [gold.py] → PostgreSQL (gold)
```

**Bronze:** dados brutos sem nenhuma transformação, apenas convertidos de CSV para Parquet.

**Silver:** dados limpos e padronizados — remoção de duplicatas, tratamento de nulos, padronização de texto e conversão de tipos.

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
├── README.md
└── requirements.txt
```

## Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL instalado e rodando (necessário apenas para a camada Gold)

### Instalação

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

### Executando o Pipeline

Os scripts devem ser executados nesta ordem, a partir da raiz do projeto:

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

## Métricas Geradas (Camada Gold)

- Faturamento total
- Faturamento por mês
- Top 10 clientes por valor comprado
- Top 10 produtos mais vendidos
- Ticket médio das vendas

## Autor

Davi Monsalves Tunes