import os
import json
import pandas as pd

# Caminho para sua pasta de CSVs
PASTA_CSV = "C:/Users/allis/Downloads/wego/csv"

eventos = []

for nome_arquivo in os.listdir(PASTA_CSV):
    if nome_arquivo.endswith(".csv"):
        caminho_arquivo = os.path.join(PASTA_CSV, nome_arquivo)
        try:
            df = pd.read_csv(caminho_arquivo)

            categoria = nome_arquivo.replace("Sympla_", "").replace(".csv", "").strip()

            for _, row in df.iterrows():
                evento = {
                    "title": str(row.get("Nome do Evento", "Sem título")),
                    "date": str(row.get("Data", "Data não informada")),
                    "location": str(row.get("Localização", "Local não informado")),
                    "image_base64": str(row.get("Imagem", "")),
                    "category": categoria,
                    "avaliacoes": []
                }
                eventos.append(evento)

        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

# Salvar o JSON final
saida = os.path.join(PASTA_CSV, "eventos_categorizados.json")
with open(saida, "w", encoding="utf-8") as f:
    json.dump(eventos, f, ensure_ascii=False, indent=2)

print(f"\n✅ Arquivo gerado com sucesso: {saida}")
