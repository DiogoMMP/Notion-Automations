from notion_client import Client
import os

# === CONFIGURAÇÃO DO NOTION ===
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# === CLIENTE NOTION ===
notion = Client(auth=NOTION_TOKEN)

# === BASE DE DADOS DAS CATEGORIAS ===
db_categorias = "23cfdc291a7281c0aa27e00a630903f6"

# 1. Fazer query ao Notion para buscar todas as categorias
response = notion.databases.query(database_id=db_categorias)

# 2. Mapear Nome -> ID
categorias = {}
for page in response["results"]:
    nome = page["properties"]["Categorias"]["title"][0]["text"]["content"]
    categorias[nome] = page["id"]

# 3. Escrever
for categoria in categorias:
    print(categoria, " -> " , categorias[categoria])