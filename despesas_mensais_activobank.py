from notion_client import Client
from datetime import datetime, timezone
import os

# === CONFIGURAÇÃO DO NOTION ===
#NOTION_TOKEN = os.environ["NOTION_TOKEN"]

NOTION_TOKEN = "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"

# === BASES DE DADOS ===
DESPESAS_MENSAIS_BD = "273fdc291a72802d805cf87e978f92e1"
ENTRADAS_BD = "25bfdc291a72815f9078c3ad680f9120"
SAIDAS_BD = "25bfdc291a7281b3b2a9fa664bae649f"

# === IDs DAS CATEGORIAS ===
DESPESAS_MENSAIS_CATEGORIA = "25bfdc291a728152be87dde686dbb338"

# === IDs DAS CONTAS ===
SALDO_REAL = "25bfdc291a728124a964ff3170e4e50f"
DESPESAS_MENSAIS = "25bfdc291a72810fbee3de79fbf3667b"

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

# Seguro Vida
despesa = results[0]["properties"][P_DESPESA]["title"][0]["text"]["content"]
despesa_mensal = results[0]["properties"][P_VALOR]["number"]


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


criar_pagina(ENTRADAS_BD, despesa, DESPESAS_MENSAIS_CATEGORIA, DESPESAS_MENSAIS, despesa_mensal)
criar_pagina(SAIDAS_BD, despesa, DESPESAS_MENSAIS_CATEGORIA, SALDO_REAL, despesa_mensal)

