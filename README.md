# WEGO - Plataforma Eventos Centralizados

**WEGo** é uma aplicação web desenvolvida com foco na centralização e curadoria de eventos reais. Com uma interface amigável, busca facilitar a descoberta de eventos autênticos por usuários e permitir que organizadores ganhem visibilidade com confiança.

---

## 📄 Descrição do Projeto

WEGo coleta dados reais da web, organiza por categoria e disponibiliza uma interface que permite:

- Visualizar eventos por categoria
- Buscar eventos por nome
- Participar de eventos
- Avaliar eventos (após participar)
- Visualizar eventos em destaque

---

## 🔹 Tecnologias Utilizadas

- Python 3.12+
- Flask
- HTML, CSS (Minimalista), JS (para interação)
- Jinja2 (renderização dinâmica)
- Selenium + WebScraping (para coleta dos eventos)
- Redis (para versão alternativa de cache)

---

## 🔍 Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/robsonsants/wego-plataforma
cd wego-eventos
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python app.py
```

Acesse via navegador: [http://localhost:5000](http://localhost:5000)

---

## 📅 Estrutura de Pastas

```
wego-eventos/
├── app.py               # Roteador principal (Flask)
├── controller.py        # Lógica de negócio (camada intermediária)
├── models.py            # Classes principais: Evento e Usuario
├── eventos_categorizados.json # Dados dos eventos organizados por categoria
├── gerar_eventos_json.py # Script de conversão CSV → JSON
├── templates/
│   └── index.html      
├── static/
│   └── style.css        
└── csv/                 # Arquivos CSV gerados via scraping
```

---

## 📂 Documentação Técnica

### `app.py`

- Arquivo principal que roda a aplicação Flask
- Define as rotas (`/`, `/categoria/<nome>`, `/participar`, `/avaliar`)
- Realiza o carregamento inicial dos eventos a partir do arquivo JSON

### `models.py`

- Define as classes `Evento` e `Usuario`
- `Evento` contém atributos como título, data, local, imagem, categoria e avaliações
- `Usuario` guarda os eventos participados e valida se o usuário pode avaliar

### `controller.py`

- Classe `SistemaWEGo` que atua como "repositório"
- Métodos para listar, filtrar, buscar eventos, e carregar o JSON

### `index.html`

- Interface principal usando Jinja2
- Permite navegar entre eventos, categorias, buscar, participar e avaliar eventos
- Layout responsivo com destaque para eventos bem avaliados

### `style.css`

- Estilo visual com foco em minimalismo e cores modernas (laranja como cor principal)

### `eventos_categorizados.json`

- Arquivo gerado pela conversão de diversos CSVs, agrupando eventos por categoria
- Usado diretamente pelo backend

### `gerar_eventos_json.py`

- Script que:
  - Lê todos os arquivos CSV dentro da pasta `csv/`
  - Extrai os campos "Nome do Evento", "Data", "Localização", "Imagem"
  - Organiza os dados em uma estrutura por categoria
  - Salva no arquivo `eventos_categorizados.json`

### `select_all_category.py` (Scraping com Selenium)

- Script para webscraping dos eventos da plataforma Sympla
- Automatiza o clique nas categorias, coleta os dados de cada evento (inclusive imagem)
- Armazena localmente em arquivos CSV por categoria
- *Versão anterior* convertia imagens diretamente para base64
- *Nesta versão*, o link da imagem é armazenado no CSV e usado dinamicamente no frontend

---

## 📂 Base de Dados

- Origem: Sympla (eventos reais)
- Transformação:
  - Extração por Selenium → CSVs por categoria
  - Conversão por script Python → JSON estruturado
  - Utilização dinâmica no sistema web via Flask

---

## ✨ Funcionalidades

- Eventos organizados por categoria
- Participar de evento com 1 clique
- Avaliação entre 1 e 5 estrelas
- Busca por nome de evento
- Eventos com maior nota ganham destaque
- Mensagem de feedback para o usuário

---

## 🎓 Projeto Acadêmico

Este projeto foi desenvolvido como parte da disciplina **"Introdução à Programação"**.

---