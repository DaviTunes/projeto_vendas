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
    df_faturamento_total = df_vendas.select(pl.sum("valor_total").alias("faturamento_total"))
    return df_faturamento_total

def faturamento_por_mes():
    df_faturamento_mes = df_vendas.group_by(
        pl.col("data_venda").dt.year().alias("ano"),
        pl.col("data_venda").dt.month().alias("mes")
    ).agg(
        pl.sum("valor_total").alias("faturamento_total")
    ).sort("ano", "mes")
    return df_faturamento_mes

def top_10_clientes():
    df_top_clientes = df_vendas.group_by(
        pl.col("id_cliente")
    ).agg(
        pl.sum("valor_total").alias("total_gasto")
    ).join(
        df_clientes, on="id_cliente", how="left"
    ).select(
        "nome", "total_gasto"
    ).sort(
        "total_gasto",descending=True
    ).head(10)
    return df_top_clientes

def top_10_produtos():
    df_top_produtos = df_vendas.group_by(
        pl.col("id_produto")
    ).agg(
        pl.sum("valor_total").alias("total_vendido")
    ).join(
        df_produtos, on="id_produto", how="left"
    ).select(
        "nome_produto", "total_vendido"
    ).sort(
        "total_vendido", descending=True
    ).head(10)
    return df_top_produtos

def ticket_medio():
    df_ticket_medio = df_vendas.select(
        pl.count("id_venda").alias("total_vendas"),
        pl.sum("valor_total").alias("faturamento_total"),
        pl.mean("valor_total").alias("ticket_medio")
    )
    return df_ticket_medio


def main():
    engine = conectar_banco()
    
    df_fat_total = faturamento_total()
    df_fat_total.write_database("faturamento_total", connection=engine, if_table_exists="replace")

    df_fat_mensal = faturamento_por_mes()
    df_fat_mensal.write_database("faturamento_mensal", connection=engine, if_table_exists="replace")

    df_top_clientes = top_10_clientes()
    df_top_clientes.write_database("top_clientes", connection=engine, if_table_exists="replace")

    df_top_produtos = top_10_produtos()
    df_top_produtos.write_database("top_produtos", connection=engine, if_table_exists="replace")

    df_ticket_med = ticket_medio()
    df_ticket_med.write_database("ticket_medio", connection=engine, if_table_exists="replace")

    engine.dispose()

if __name__ == "__main__":
    main()

