from notion_client import Client
import os

# === CONFIGURAÇÃO DO NOTION ===
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# === BASES DE DADOS ===
ENTRADAS_BD = "23cfdc291a7281fc8b9dc4cbbf617ed0"
SAIDAS_BD = "23cfdc291a7281be8c7ed8b65b76da7e"
PAGAR_CARTAO_CREDITO = "23efdc291a72800b909be988f864ee14"

# === IDs DAS CONTAS ===
CARTAO_SANTANDER = "23efdc29-1a72-80f8-b21d-c3ea5e52d2b4"

# === IDs DAS CATEGORIAS ===
REEMBOLSO_CATEGORIA = "263fdc29-1a72-808e-90ed-e608f1fe02e0"

# === CLIENTE NOTION ===
notion = Client(auth=NOTION_TOKEN)

# === OBTER VALORES DAS ENTRADAS ===
config_page = notion.pages.retrieve(PAGAR_CARTAO_CREDITO)

inicio = config_page["properties"]["Início"]["date"]["start"]
fim = config_page["properties"]["Fim"]["date"]["start"]

# Entradas
results = notion.databases.query(
    **{
        "database_id": ENTRADAS_BD,
        "filter": {
            "and": [
                {
                    "property": "Conta",
                    "relation": {
                        "contains": CARTAO_SANTANDER
                    }
                },
                {
                    "property": "Data",
                    "date": {
                        "on_or_after": inicio
                    }
                },
                {
                    "property": "Data",
                    "date": {
                        "on_or_before": fim
                    }
                },
                {
                    "property": "Saiu",
                    "checkbox": {
                        "equals": False
                    }
                }
            ]
        }
    }
)

valor = 0
for page in results["results"]:
    valor = valor + page["properties"]["Valor"]["number"]

# Saídas
results = notion.databases.query(
    **{
        "database_id": SAIDAS_BD,
        "filter": {
            "and": [
                {
                    "property": "Conta",
                    "relation": {
                        "contains": CARTAO_SANTANDER
                    }
                },
                {
                    "property": "Data",
                    "date": {
                        "on_or_after": inicio
                    }
                },
                {
                    "property": "Data",
                    "date": {
                        "on_or_before": fim
                    }
                },
                {
                    "property": "Categoria",
                    "relation": {
                        "contains": REEMBOLSO_CATEGORIA
                    }
                },
            ]
        }
    }
)

saidas = 0
for page in results["results"]:
    saidas = saidas + page["properties"]["Valor"]["number"]

valor = valor - saidas

notion.pages.update(
    PAGAR_CARTAO_CREDITO,
    properties={
        "Valor": {
            "number": valor
        }
    }
)