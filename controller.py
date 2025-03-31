import json
from models import Evento

class SistemaWEGo:
    def __init__(self):
        self.eventos = []

    def carregar_eventos(self, caminho_json="csv/eventos_categorizados.json"):
        self.eventos = []
        try:
            with open(caminho_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for ev in dados:
                    evento = Evento(
                        titulo=ev.get("title", "Sem título"),
                        data=ev.get("date", "Data não informada"),
                        local=ev.get("location", "Local não informado"),
                        imagem_base64=ev.get("image_base64", ""),
                        categoria=ev.get("category", "Geral")
                    )
                    self.eventos.append(evento)
        except Exception as e:
            print(f"Erro ao carregar eventos: {e}")

    def listar_eventos(self):
        return self.eventos

    def listar_por_categoria(self):
        categorias = {}
        for evento in self.eventos:
            categorias.setdefault(evento.categoria, []).append(evento)
        return categorias

    def encontrar_evento_por_titulo(self, titulo):
        for evento in self.eventos:
            if evento.titulo == titulo:
                return evento
        return None
