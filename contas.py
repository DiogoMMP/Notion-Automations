from notion_client import Client
import os

# === CONFIGURAÇÃO DO NOTION ===
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# === CLIENTE NOTION ===
notion = Client(auth=NOTION_TOKEN)

# === BASE DE DADOS DAS CONTAS ===
db_contas = "23cfdc291a728143b501ec3f411e0901"

# 1. Fazer query ao Notion para buscar todas as contas
response = notion.databases.query(database_id=db_contas)

# 2. Mapear Conta -> ID
contas = {}
for page in response["results"]:
    conta = page["properties"]["Conta"]["title"][0]["text"]["content"]
    contas[conta] = page["id"]

# 3. Escrever
for conta in contas:
    print(conta, " -> " , contas[conta])