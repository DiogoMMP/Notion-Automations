from notion_client import Client
from datetime import datetime, timezone
import os

# === CONFIGURAÇÃO DO NOTION ===
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# === BASES DE DADOS ===
ENTRADAS_BD = "23cfdc291a7281fc8b9dc4cbbf617ed0"
SAIDAS_BD = "23cfdc291a7281be8c7ed8b65b76da7e"
PAGAR_CARTAO_CREDITO = "285fdc291a7280fc9f1fcc0c0f7b157f"

# === IDs DAS CONTAS ===
CARTAO_UNIVERSO = "244fdc291a7280cb88bfc5c6c1c00382"

# === IDs DAS CATEGORIAS ===
DESPESAS_MENSAIS_CATEGORIA = "23efdc29-1a72-80e5-bb24-d9b646ddb21b"

# === NOMES DAS PROPRIEDADES ===
P_NOME = "Nome"                 #Texto
P_CATEGORIA = "Categoria"       #Relação
P_CONTA = "Conta"               #Relação
P_DATA = "Data"                 #Data
P_VALOR = "Valor"               #Número

# === CLIENTE NOTION ===
notion = Client(auth=NOTION_TOKEN)

# === OBTER VALORES DAS ENTRADAS ===
config_page = notion.pages.retrieve(PAGAR_CARTAO_CREDITO)

inicio = config_page["properties"]["Início"]["date"]["start"]
fim = config_page["properties"]["Fim"]["date"]["start"]
pago = config_page["properties"]["Pago"]["checkbox"]
valor = config_page["properties"]["Valor"]["number"]

if pago is True:
    # Entradas
    results = notion.databases.query(
        **{
            "database_id": ENTRADAS_BD,
            "filter": {
                "and": [
                    {
                        "property": "Conta",
                        "relation": {
                            "contains": CARTAO_UNIVERSO
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
                            "before": fim
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
    )["results"]

    for result in results:
        page_id = result["id"]
        notion.pages.update(
            page_id,
            properties={
                "Saiu": {"checkbox": True}
            }
        )

    hoje = datetime.now(timezone.utc)

    notion.pages.create(
        parent={"database_id": SAIDAS_BD},
        properties={
            P_NOME: {
                "title": [
                    {"text": {"content": "Pagamento do Cartão de Crédito Universo"}}
                ]
            },
            P_CATEGORIA: {
                "relation": [
                    {"id": DESPESAS_MENSAIS_CATEGORIA}
                ]
            },
            P_CONTA: {
                "relation": [
                    {"id": CARTAO_UNIVERSO}
                ]
            },
            P_DATA: {
                "date": {
                    "start": hoje.isoformat()
                }
            },
            P_VALOR: {
                "number": valor
            }
        }
    )

    data_15 = hoje.replace(day=15)

    notion.pages.update(
        PAGAR_CARTAO_CREDITO,
        properties={
            "Valor": {
                "number": 0
            },
            "Pago":{
                "checkbox": False
            },
            "Início":{
                "date": {
                    "start": fim.split("T")[0]
                }
            },
            "Fim":{
                "date": {
                    "start": data_15.date().isoformat()
                }
            }
        }
    )