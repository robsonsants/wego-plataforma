from flask import Flask, render_template, request, redirect, jsonify
from controller import SistemaWEGo
from models import Usuario
import random

app = Flask(__name__)
sistema = SistemaWEGo()
usuario = Usuario()
sistema.carregar_eventos()

@app.route("/")
def index():
    eventos = sistema.listar_eventos()
    eventos_ordenados = sorted(eventos, key=lambda e: e.media_avaliacoes(), reverse=True)
    categorias = list(sistema.listar_por_categoria().keys())
    return render_template("index.html", eventos=eventos_ordenados, categorias=categorias, usuario=usuario)


@app.route("/ver_categoria/<nome>")
def ver_categoria(nome):
    eventos_categoria = sistema.listar_por_categoria().get(nome, [])
    return render_template("index.html", eventos=eventos_categoria, categorias=list(sistema.listar_por_categoria().keys()), usuario=usuario, mensagem=f"Categoria: {nome}")

@app.route("/categoria/<nome>")
def categoria(nome):
    eventos_categoria = sistema.listar_por_categoria().get(nome, [])
    return jsonify([{
        "titulo": e.titulo,
        "data": e.data,
        "local": e.local,
        "imagem_base64": e.imagem_base64,
        "media": e.media_avaliacoes(),
        "participado": usuario.participou_do_evento(e)
    } for e in eventos_categoria])

@app.route("/participar", methods=["POST"])
def participar():
    titulo = request.form.get("titulo")
    evento = sistema.encontrar_evento_por_titulo(titulo)
    if evento:
        usuario.participar(evento)
        return render_template("index.html", eventos=[evento], categorias=list(sistema.listar_por_categoria().keys()), usuario=usuario)
    return redirect("/")

@app.route("/avaliar", methods=["POST"])
def avaliar():
    titulo = request.form.get("titulo")
    nota = int(request.form.get("nota"))
    evento = sistema.encontrar_evento_por_titulo(titulo)
    if evento and usuario.participou_do_evento(evento):
        evento.adicionar_avaliacao(nota)
        mensagem = "✅ Obrigado por avaliar o evento! Volte sempre 😊"
        return render_template("index.html", eventos=[evento], categorias=list(sistema.listar_por_categoria().keys()), usuario=usuario, mensagem=mensagem)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
