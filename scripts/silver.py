import polars as pl
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bronze_path = os.path.join(base_dir, "data", "bronze")
silver_path = os.path.join(base_dir, "data", "silver")


def tratar_clientes():
    file = "clientes.parquet"
    print(f"Tratando {file}...")

    df = pl.read_parquet(bronze_path + "/" + file)
    registros_antes = df.shape[0]

    df = df.with_columns(
        pl.col("email").fill_null("NAO INFORMADO")
    )
    df = df.with_columns(
        pl.col("cidade").fill_null("NAO INFORMADO")
    )
    df = df.filter(
        pl.col("nome").is_not_null()
    )
    df = df.unique(subset=["nome", "email", "cidade", "estado"])
    df = df.with_columns(
        pl.col("nome", "cidade", "estado").str.to_uppercase(),
        pl.col("email").str.to_lowercase()
    )

    parquet_file_path = os.path.join(silver_path, file)
    df.write_parquet(parquet_file_path)
    print(f"  -> {registros_antes} registros -> {df.shape[0]} registros ({registros_antes - df.shape[0]} removidos)")


def tratar_produtos():
    file = "produtos.parquet"
    print(f"Tratando {file}...")

    df = pl.read_parquet(bronze_path + "/" + file)
    registros_antes = df.shape[0]

    df = df.with_columns(
        pl.col("preco").fill_null(0)
    )
    df = df.unique(subset=["nome_produto", "categoria"])
    df = df.with_columns(
        pl.col("nome_produto", "categoria").str.to_uppercase()
    )
    df = df.with_columns(
        pl.col("preco").cast(pl.Float64)
    )

    parquet_file_path = os.path.join(silver_path, file)
    df.write_parquet(parquet_file_path)
    print(f"  -> {registros_antes} registros -> {df.shape[0]} registros ({registros_antes - df.shape[0]} removidos)")


def tratar_vendas():
    file = "vendas.parquet"
    file2 = "clientes.parquet"
    print(f"Tratando {file}...")

    df = pl.read_parquet(bronze_path + "/" + file)
    registros_antes = df.shape[0]

    df = df.filter(pl.col("quantidade").is_not_null())
    df = df.unique(subset=["id_cliente", "id_produto", "quantidade", "preco_unitario", "data_venda"])
    df = df.with_columns(
        pl.col("data_venda").str.to_date(),
    )
    df = df.join(
        pl.read_parquet(silver_path + "/" + file2).select("id_cliente"),
        on="id_cliente",
        how="inner"
    )

    df = df.with_columns(
        (pl.col("quantidade") * pl.col("preco_unitario")).round(2).alias("valor_total")
    )

    parquet_file_path = os.path.join(silver_path, file)
    df.write_parquet(parquet_file_path)
    print(f"  -> {registros_antes} registros -> {df.shape[0]} registros ({registros_antes - df.shape[0]} removidos)")


if __name__ == "__main__":
    print("=" * 50)
    print("CAMADA SILVER - Limpeza e padronização")
    print("=" * 50)

    tratar_clientes()
    tratar_produtos()
    tratar_vendas()

    print("\nCamada Silver finalizada com sucesso!")