# Notion-Automations

Este repositório contém um conjunto de **automações em Python** para integração com o [Notion](https://www.notion.so/).  
O objetivo é atualizar automaticamente bases de dados e propriedades específicas em intervalos definidos, utilizando **GitHub Actions**.  

---

## 📂 Estrutura do projeto

- `cartao_credito.py`  
  Automatiza o "pagamento" registado na base de dados **Pagar Cartão de Crédito**:  
  - Retira o valor da conta *Cartão de Crédito Santander*.  
  - Marca como concluídas (`checkbox "Saiu"`) as despesas dentro da janela de datas.  
  - ⚙️ Corre a cada **5 minutos** nos dias **6, 7 e 8** de cada mês.

- `categorias.py`  
  Exporta todos os **IDs das páginas** da base de dados **Categorias**.

- `contas.py`  
  Exporta todos os **IDs das páginas** da base de dados **Contas**.

- `despesas_mensais.py`  
  - Lê a base de dados **Valores das Despesas Mensais**.  
  - Cria entradas na conta *Despesas Mensais* e saídas na conta *Saldo Real*.  
  - ⚙️ Corre automaticamente à **meia-noite do dia 1 de cada mês**.

- `despesas_mensais_activobank.py`  
  Versão simplificada do script anterior, mas aplicada a outro banco e apenas com uma despesa.

- `valor_cartao_credito.py`  
  - Soma todas as despesas registadas no cartão de crédito dentro de uma janela de datas.  
  - Desconta reembolsos, mantendo o valor atualizado.  
  - ⚙️ Corre a cada **5 minutos**.

---

## ⚙️ Workflows (GitHub Actions)

Existem **3 workflows configurados** no GitHub Actions:

1. **Cartão de Crédito**  
   Executa o script `cartao_credito.py` conforme agendamento (5 em 5 minutos nos dias 6, 7 e 8).

2. **Despesas Mensais**  
   Executa `despesas_mensais.py` no dia 1 de cada mês, à meia-noite.

3. **Valor Cartão de Crédito**  
   Mantém o valor atualizado, correndo `valor_cartao_credito.py` de 5 em 5 minutos.

---

## 📦 Dependências

Todas as bibliotecas necessárias encontram-se listadas no ficheiro:

```
requirements.txt
```

Instalação local:

```bash
pip install -r requirements.txt
````

---

## 🔑 Integração com o Notion

Para funcionar corretamente:

1. Criar uma [integração interna no Notion](https://developers.notion.com/docs/getting-started).
2. Copiar o **token secreto** gerado.
3. Partilhar as bases de dados/páginas relevantes com a integração.
4. Guardar o token no GitHub como um **Secret** chamado `NOTION_TOKEN`.

No código, o token é acedido através da variável de ambiente:

```python
import os
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
```

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**.
Consulta o ficheiro `LICENSE` para mais detalhes.
