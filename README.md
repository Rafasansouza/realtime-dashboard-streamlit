# 📊 Dashboard em Tempo Real com Streamlit

Este projeto é um **dashboard web em tempo real** desenvolvido com **Streamlit**. Ele se conecta a um banco de dados relacional (PostgreSQL por padrão) e exibe informações em tempo real divididas em três áreas principais:

- **Plantão**
- **Manutenção**
- **Almoxarifado**

A página é atualizada automaticamente a cada 10 segundos.

---

## 🚀 Funcionalidades

- Atualização automática a cada 10 segundos com `streamlit-autorefresh`
- Navegação entre páginas usando a sidebar do Streamlit
- Conexão com banco de dados via SQLAlchemy
- Exibição de dados dinâmicos em tabelas interativas
- Projeto organizado com gerenciador de pacotes `poetry`

---

## 🧱 Estrutura do Projeto

```
realtime-dashboard/
├── app.py
├── db/
│   └── connection.py
├── pages/
│   ├── 1_Plantao.py
│   ├── 2_Manutencao.py
│   └── 3_Almoxarifado.py
├── pyproject.toml
```

---

## ⚙️ Pré-requisitos

- Python 3.9 ou superior
- [Poetry](https://python-poetry.org/docs/#installation)
- Acesso a um banco de dados (ex: PostgreSQL)

---

## 🛠️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/Rafasansouza/realtime-dashboard-streamlit
cd realtime-dashboard-streamlit
```

### 2. Instale as dependências com Poetry

```bash
poetry install
```

### 3. Ative o ambiente virtual

```bash
poetry shell
```

### 4. Configure o banco de dados

Edite o arquivo `db/connection.py` e ajuste a string de conexão:

```python
from sqlalchemy import create_engine

def get_connection():
    engine = create_engine("postgresql://usuario:senha@localhost:5432/nomedobanco")
    return engine.connect()
```

> ⚠️ **Importante:** Certifique-se de que o banco está ativo, acessível e que os dados necessários já existem nas tabelas. Além disso, lembre-se de modificar a consulta ao banco deste projeto para a consulta ao seu banco de dados.

---

### 5. Execute o Streamlit

```bash
poetry run streamlit run app.py
```

---

## 📦 Principais Dependências

- `streamlit`
- `pandas`
- `sqlalchemy`
- `psycopg2-binary` (ou outro driver, dependendo do banco usado)
- `streamlit-autorefresh`

---

## 📌 Observações

- A estrutura está pronta para PostgreSQL, mas você pode adaptar facilmente para **MySQL**, **SQL Server** ou **SQLite**, modificando apenas a string de conexão.
- O projeto segue boas práticas de organização de código e gerenciamento de ambiente.
- Ideal para uso em operações, monitoramento e BI em tempo real.

---
