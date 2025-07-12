# pages/1_🌙_Plantao.py
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from db.connection import get_connection

# Atualiza a página automaticamente a cada 10 segundos
st_autorefresh(interval=10_000, limit=None, key="refresh")

st.set_page_config(page_title="Plantão", layout="wide")
st.title("Dados do Plantão")

def carregar_dados():
    with get_connection() as conn:
        query = "SELECT * FROM public.produto;"
        df = pd.read_sql(query, conn)
    return df

df = carregar_dados()
st.dataframe(df, use_container_width=True)
