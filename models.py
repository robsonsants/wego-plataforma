class Evento:
    def __init__(self, titulo, data, local, imagem_base64, categoria):
        self.titulo = titulo
        self.data = data
        self.local = local
        self.imagem_base64 = imagem_base64
        self.categoria = categoria
        self.avaliacoes = []

    def adicionar_avaliacao(self, nota):
        if 1 <= nota <= 5:
            self.avaliacoes.append(nota)

    def media_avaliacoes(self):
        if not self.avaliacoes:
            return 0
        return sum(self.avaliacoes) / len(self.avaliacoes)


class Usuario:
    def __init__(self):
        self.eventos_participados = set()

    def participar(self, evento):
        self.eventos_participados.add(evento.titulo)

    def participou_do_evento(self, evento):
        return evento.titulo in self.eventos_participados
