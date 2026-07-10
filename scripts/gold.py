from dotenv import load_dotenv
from sqlalchemy import create_engine
import polars as pl
import os

load_dotenv()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df_vendas = pl.read_parquet(os.path.join(base_dir, "data", "silver", "vendas.parquet"))
df_clientes = pl.read_parquet(os.path.join(base_dir, "data", "silver", "clientes.parquet"))
df_produtos = pl.read_parquet(os.path.join(base_dir, "data", "silver", "produtos.parquet"))


def conectar_banco():
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    return engine


def faturamento_total():
    return df_vendas.select(
        pl.sum("valor_total").round(2).alias("faturamento_total")
    )

def faturamento_por_mes():
    return df_vendas.group_by(
        pl.col("data_venda").dt.year().alias("ano"),
        pl.col("data_venda").dt.month().alias("mes")
    ).agg(
        pl.sum("valor_total").round(2).alias("faturamento_total")
    ).sort("ano", "mes")

def top_10_clientes():
    return df_vendas.group_by(
        pl.col("id_cliente")
    ).agg(
        pl.sum("valor_total").round(2).alias("total_gasto")
    ).join(
        df_clientes, on="id_cliente", how="left"
    ).select(
        "nome", "total_gasto"
    ).sort(
        "total_gasto", descending=True
    ).head(10)

def top_10_produtos():
    return df_vendas.group_by(
        pl.col("id_produto")
    ).agg(
        pl.sum("valor_total").round(2).alias("total_vendido")
    ).join(
        df_produtos, on="id_produto", how="left"
    ).select(
        "nome_produto", "total_vendido"
    ).sort(
        "total_vendido", descending=True
    ).head(10)

def ticket_medio():
    return df_vendas.select(
        pl.count("id_venda").alias("total_vendas"),
        pl.sum("valor_total").round(2).alias("faturamento_total"),
        pl.mean("valor_total").round(2).alias("ticket_medio")
    )



def main():
    print("=" * 50)
    print("CAMADA GOLD - Métricas de negócio")
    print("=" * 50)

    print("Conectando ao PostgreSQL...")
    engine = conectar_banco()

    print("Calculando faturamento total...")
    faturamento_total().write_database("faturamento_total", connection=engine, if_table_exists="replace")

    print("Calculando faturamento por mês...")
    faturamento_por_mes().write_database("faturamento_mensal", connection=engine, if_table_exists="replace")

    print("Calculando top 10 clientes...")
    top_10_clientes().write_database("top_clientes", connection=engine, if_table_exists="replace")

    print("Calculando top 10 produtos...")
    top_10_produtos().write_database("top_produtos", connection=engine, if_table_exists="replace")

    print("Calculando ticket médio...")
    ticket_medio().write_database("ticket_medio", connection=engine, if_table_exists="replace")

    engine.dispose()
    print("\nCamada Gold finalizada com sucesso!")


if __name__ == "__main__":
    main()