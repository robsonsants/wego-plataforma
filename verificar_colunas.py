import os
import pandas as pd

PASTA_CSV = "C:/Users/allis/Downloads/wego/csv"

for nome_arquivo in os.listdir(PASTA_CSV):
    if nome_arquivo.endswith(".csv"):
        caminho = os.path.join(PASTA_CSV, nome_arquivo)
        try:
            df = pd.read_csv(caminho)
            print(f"\n🗂️ Arquivo: {nome_arquivo}")
            print("🔑 Colunas:", list(df.columns))
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")
