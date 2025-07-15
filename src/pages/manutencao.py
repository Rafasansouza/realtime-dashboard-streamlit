# pages/plantao.py
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from db.connection import get_connection

# Atualiza a página automaticamente a cada 10 segundos
st_autorefresh(interval=10_000, limit=None, key="refresh")

st.set_page_config(page_title="Plantão", layout="wide")

# def carregar_dados():
#     with get_connection() as conn:
#         query = "SELECT * FROM public.produto;"
#         df = pd.read_sql(query, conn)
#     return df

# df = carregar_dados()

# st.dataframe(df, use_container_width=True)

# Dados fictícios
dados = pd.DataFrame({
    "placa": [f"ABC{n:03d}" for n in range(1, 11)],
    "tipo_servico": ["Preventiva", "Corretiva", "Corretiva", "Preventiva", "Preventiva", 
                     "Corretiva", "Preventiva", "Preventiva", "Preventiva", "Corretiva"],
    "turno": ["Manhã", "Tarde", "Manhã", "Noite", "Manhã", 
              "Tarde", "Noite", "Manhã", "Tarde", "Noite"],
    "status": ["Programado", "Realizado", "Programado", "Realizado", "Realizado", 
               "Programado", "Programado", "Realizado", "Realizado", "Programado"],
    "equipe": ["A", "B", "A", "C", "A", "B", "C", "A", "C", "B"],
    "tempo_execucao": [None, 45, None, 50, 30, None, None, 25, 40, None]
})

# Separar programados e realizados
df_programado = dados[dados["status"] == "Programado"]
df_realizado = dados[dados["status"] == "Realizado"]

# KPIs
total_programado = len(df_programado)
total_realizado = len(df_realizado)
total_prog_preventiva = len(df_programado[df_programado["tipo_servico"] == "Preventiva"])
total_prog_corretiva =  len(df_programado[df_programado["tipo_servico"] == "Corretiva"])
total_real_preventiva = len(df_realizado[df_realizado["tipo_servico"] == "Preventiva"])
total_real_corretiva =  len(df_realizado[df_realizado["tipo_servico"] == "Corretiva"])
percentual = (total_realizado / (total_programado + total_realizado)) * 100 if (total_programado + total_realizado) > 0 else 0
tempo_medio = df_realizado["tempo_execucao"].mean()

# Configuração da página
st.set_page_config(page_title="Manutenção - Programado x Realizado", layout="wide")
st.title("🛠️ Dashboard de Manutenção - Programado x Realizado")


st.markdown("**% de Cumprimento da Programação**")
st.progress(min(int(percentual), 100))  # barra visual de 0 a 100
st.markdown(f"<p style='text-align:center;font-size:18px;'>{percentual:.1f}%</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# 🔧 COLUNA 1: PROGRAMADO
with col1:
    st.subheader("🔧 Programado")

    st.markdown(
        f"""
        <div style="display: flex; gap: 20px;">  
            <div style="padding: 20px; border-radius: 10px; background-color: white; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;">
                <h4 style="margin-bottom: 5px;">Preventivas Programadas</h4>
                <h2 style="color: #3366cc;">{total_prog_preventiva}</h2>
            </div>
            <div style="padding: 20px; border-radius: 10px; background-color: white; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;">
                <h4 style="margin-bottom: 5px;">Corretivas Programadas</h4>
                <h2 style="color: #3366cc;">{total_prog_corretiva}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("**Programados por Tipo de Serviço**")
    st.bar_chart(df_programado["tipo_servico"].value_counts())

    st.markdown("**Programados por Turno**")
    st.bar_chart(df_programado["turno"].value_counts())

    st.markdown("**Top Serviços Programados**")
    st.dataframe(df_programado[["placa", "tipo_servico", "turno", "equipe"]])

# ✅ COLUNA 2: REALIZADO
with col2:
    st.subheader("✅ Realizado")

    st.markdown(
        f"""
        <div style="display: flex; gap: 20px;">  
            <div style="padding: 20px; border-radius: 10px; background-color: white; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;">
                <h4 style="margin-bottom: 5px;">Preventivas Realizadas</h4>
                <h2 style="color: #3366cc;">{total_real_preventiva}</h2>
            </div>
            <div style="padding: 20px; border-radius: 10px; background-color: white; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;">
                <h4 style="margin-bottom: 5px;">Corretivas Realizadas</h4>
                <h2 style="color: #3366cc;">{total_real_corretiva}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("**Realizados por Equipe**")
    st.bar_chart(df_realizado["equipe"].value_counts())

    st.markdown("**Tempo Médio de Execução (min)**")
    if tempo_medio:
        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; background-color: white; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;">
                <h4 style="margin-bottom: 5px;">Tempo Médio</h4>
                <h2 style="color: #555;">{tempo_medio:.1f} min</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Sem dados de tempo disponíveis.")

    st.markdown("**Serviços Finalizados**")
    st.dataframe(df_realizado[["placa", "tipo_servico", "turno", "equipe", "tempo_execucao"]])