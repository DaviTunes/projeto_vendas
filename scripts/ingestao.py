import polars as pl
import os


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw")
    bronze_path = os.path.join(base_dir, "data", "bronze")

    for file in os.listdir(raw_path):
        if file.endswith(".csv"):
            df = pl.read_csv(os.path.join(raw_path, file))
            parquet_file_path = os.path.join(bronze_path, file.replace(".csv", ".parquet"))
            df.write_parquet(parquet_file_path)


if __name__ == "__main__":
    main()