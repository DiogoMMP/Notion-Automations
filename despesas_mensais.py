from notion_client import Client
from datetime import datetime, timezone
import os

# === CONFIGURAÇÃO DO NOTION ===
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# === BASES DE DADOS ===
DESPESAS_MENSAIS_BD = "23efdc291a7280e9b9bed4bd2b316ab8"
ENTRADAS_BD = "23cfdc291a7281fc8b9dc4cbbf617ed0"
SAIDAS_BD = "23cfdc291a7281be8c7ed8b65b76da7e"

# === IDs DAS CATEGORIAS ===
DESPESAS_MENSAIS_CATEGORIA = "23efdc29-1a72-80e5-bb24-d9b646ddb21b"

# === IDs DAS CONTAS ===
SALDO_REAL = "23cfdc29-1a72-8151-b359-ee758733623a"
DESPESAS_MENSAIS = "23cfdc29-1a72-81e8-a3df-ef05e86b7254"

# === NOMES DAS PROPRIEDADES ===
P_NOME = "Nome"                 #Texto
P_CATEGORIA = "Categoria"       #Relação
P_CONTA = "Conta"               #Relação
P_DATA = "Data"                 #Data
P_VALOR = "Valor"               #Número
P_DESPESA = "Despesa"           #Texto

# === CLIENTE NOTION ===
notion = Client(auth=NOTION_TOKEN)

# === OBTER VALORES DAS DESPESAS MENSAIS ===
results = notion.databases.query(DESPESAS_MENSAIS_BD)["results"]

# Associação, Conta Poupança, NOS Pais, Seguro Vida, Prestação da Casa
despesas_mensais = {}

for result in results:
    despesa = result["properties"][P_DESPESA]["title"][0]["text"]["content"]
    despesas_mensais[despesa] = result["properties"][P_VALOR]["number"]

def criar_pagina(database_id, nome, categoria, conta, valor):
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            P_NOME: {
                "title": [
                    {"text": {"content": nome}}
                ]
            },
            P_CATEGORIA: {
                "relation": [
                    {"id": categoria}
                ]
            },
            P_CONTA: {
                "relation": [
                    {"id": conta}
                ]
            },
            P_DATA: {
                "date": {
                    "start": datetime.now(timezone.utc).date().isoformat()
                }
            },
            P_VALOR: {
                "number": valor
            }
        }
    )


for despesa_mensal in despesas_mensais:
    criar_pagina(ENTRADAS_BD, despesa_mensal, DESPESAS_MENSAIS_CATEGORIA, DESPESAS_MENSAIS, despesas_mensais[despesa_mensal])
    criar_pagina(SAIDAS_BD, despesa_mensal, DESPESAS_MENSAIS_CATEGORIA, SALDO_REAL, despesas_mensais[despesa_mensal])

