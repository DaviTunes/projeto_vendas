import polars as pl
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bronze_path = os.path.join(base_dir, "data", "bronze")
silver_path = os.path.join(base_dir, "data", "silver")


def tratar_clientes():
    file = "clientes.parquet"

    df = pl.read_parquet(bronze_path + "/" + file)

    # tratar emails nulos
    df = df.with_columns(
        pl.col("email").fill_null("NAO INFORMADO")
    )

    # tratar cidades nulas
    df = df.with_columns(
        pl.col("cidade").fill_null("NAO INFORMADO")
    )

    # valores repetidos
    df = df.unique(subset=["nome", "email", "cidade", "estado"])

    # padronização de texto
    df = df.with_columns(
        pl.col("nome", "cidade", "estado").str.to_uppercase(),
        pl.col("email").str.to_lowercase()
    )

    # salvando parquet
    parquet_file_path = os.path.join(silver_path, file)
    df.write_parquet(parquet_file_path)

def tratar_produtos():
    file = "produtos.parquet"

    df = pl.read_parquet(bronze_path + "/" + file)

    # tratar preços nulos
    df = df.with_columns(
        pl.col("preco").fill_null(0)
    )

    # valores repetidos
    df = df.unique(subset=["nome_produto", "categoria"])

    # padronização de texto
    df = df.with_columns(
        pl.col("nome_produto", "categoria").str.to_uppercase()
    )

    # convertendo tipos
    df = df.with_columns(
        pl.col("preco").cast(pl.Float64)
    )

    # salvando parquet
    parquet_file_path = os.path.join(silver_path, file)
    df.write_parquet(parquet_file_path)

def tratar_vendas():
    file = "vendas.parquet"

    df = pl.read_parquet(bronze_path + "/" + file)

    # tratar valores nulos
    df = df.filter(
        pl.col("quantidade").is_not_null()
    )

    # valores repetidos
    df = df.unique(subset=["id_cliente", "id_produto", "quantidade", "preco_unitario", "data_venda"])


    # convertendo tipos
    df = df.with_columns(
        pl.col("data_venda").str.to_date(),
    )

    # criando coluna valor total
    df = df.with_columns(
        (pl.col("quantidade") * pl.col("preco_unitario")).round(2).alias("valor_total")
    )

    parquet_file_path = os.path.join(silver_path, file)
    df.write_parquet(parquet_file_path)


if __name__ == "__main__":
    tratar_clientes()
    tratar_produtos()
    tratar_vendas()

    

