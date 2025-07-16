# pages/plantao.py
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from db.connection import get_connection
import altair as alt
from datetime import datetime

# Atualiza a página automaticamente a cada 10 segundos
st_autorefresh(interval=10_000, limit=None, key="refresh")

st.set_page_config(page_title="Manutenção", layout="wide")

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
    "status": ["Realizado", "Aberto", "Realizado", "Realizado", "Realizado", 
               "Realizado", "Realizado", "Realizado", "Aberto", "Aberto"],
    "equipe": ["A", "B", "A", "C", "A", "B", "C", "A", "C", "B"],
    "tempo_execucao": [None, 45, None, 50, 30, None, None, 25, 40, None]
})

# Separar realizados
df_realizado = dados[dados["status"] == "Realizado"]

# KPIs
total_programado = len(dados)
total_realizado = len(df_realizado)
total_prog_preventiva = len(dados[dados["tipo_servico"] == "Preventiva"])
total_prog_corretiva =  len(dados[dados["tipo_servico"] == "Corretiva"])
total_real_preventiva = len(df_realizado[df_realizado["tipo_servico"] == "Preventiva"])
total_real_corretiva =  len(df_realizado[df_realizado["tipo_servico"] == "Corretiva"])
percentual = (total_realizado / total_programado) * 100 if (total_realizado) > 0 else 0
graus = (percentual / 100) * 180
date_now = datetime.now().strftime("%d/%m/%Y")

# Configuração da página
# Configuração inicial da página
st.set_page_config(page_title="Manutenção - Programado x Realizado", layout="wide")

# CSS personalizado para reduzir espaçamento superior
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
        }
        [data-testid="stHeader"] {
            z-index: -999;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do dashboard
st.title("🛠️ Dashboard de Manutenção - Programado x Realizado")

barra_html = f"""
<div style="margin-top: 20px;">
    <div style="margin-bottom: 8px; color: #ccc; font-size: 16px;">Progresso do dia {date_now}</div>
    <div style="width: 100%; background-color: #1e2a38; border-radius: 10px; height: 36px; overflow: hidden;">
        <div style="
            height: 100%;
            width: {percentual}%;
            background-color: #16C60C;
            border-radius: 10px 0 0 10px;
            text-align: right;
            padding-right: 12px;
            color: white;
            font-weight: bold;
            line-height: 36px;
            font-size: 16px;">
            {percentual:.1f}%
        </div>
    </div>
</div>
"""
st.markdown(barra_html, unsafe_allow_html=True)

# Adicionando espaçamento de 50px
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# PROGRAMADO
with col1:
    st.subheader("🔧 Programado")

    st.markdown(
        f"""
        <div style="display: flex; gap: 20px;">  
            <div style="padding: 20px; border-radius: 10px; background-color: #1E2A38; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;
                        width: 350px; margin: 0 auto;">
                <h4 style="margin-bottom: 5px;">Total de Preventivas</h4>
                <h2 style="color: #3366cc;">{total_prog_preventiva}</h2>
            </div>
            <div style="padding: 20px; border-radius: 10px; background-color: #1E2A38; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;
                        width: 350px; margin: 0 auto;">
                <h4 style="margin-bottom: 5px;">Total de Corretivas</h4>
                <h2 style="color: #3366cc;">{total_prog_corretiva}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

    T_equipe_counts = dados["equipe"].value_counts().reset_index()
    T_equipe_counts.columns = ["equipe", "quantidade"]

    chart = alt.Chart(T_equipe_counts).mark_bar(color="#83C9FF").encode(
    y=alt.Y("equipe", title="Setor", sort="-x"),
    x=alt.X("quantidade", title="Quantidade",
            axis=alt.Axis(
                values=list(range(0, int(max(T_equipe_counts['quantidade'])) + 1)),  # Valores inteiros
                tickCount=int(max(T_equipe_counts['quantidade'])) + 1,  # Número de ticks
                format='d'  # Formato decimal sem casas
            )),
    tooltip=["equipe", "quantidade"]
    ).properties(
        width=500,
        height=300
    )

    st.markdown("#### **Total de Serviços por Setor**")
    st.altair_chart(chart, use_container_width=True)

# REALIZADO
with col2:
    st.subheader("✅ Realizado")

    st.markdown(
        f"""
        <div style="display: flex; gap: 20px;">  
            <div style="padding: 20px; border-radius: 10px; background-color: #1E2A38; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;
                        width: 350px; margin: 0 auto;">
                <h4 style="margin-bottom: 5px;">Preventivas Realizadas</h4>
                <h2 style="color: #3366cc;">{total_real_preventiva}</h2>
            </div>
            <div style="padding: 20px; border-radius: 10px; background-color: #1E2A38; 
                        border: 1px solid #ccc; text-align: center; margin-bottom: 20px;
                        width: 350px; margin: 0 auto;">
                <h4 style="margin-bottom: 5px;">Corretivas Realizadas</h4>
                <h2 style="color: #3366cc;">{total_real_corretiva}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

    equipe_counts = df_realizado["equipe"].value_counts().reset_index()
    equipe_counts.columns = ["equipe", "quantidade"]

    chart = alt.Chart(equipe_counts).mark_bar(color="#83C9FF").encode(
    y=alt.Y("equipe", title="Setor", sort="-x"),
    x=alt.X("quantidade", title="Quantidade",
            axis=alt.Axis(
                values=list(range(0, int(max(equipe_counts['quantidade'])) + 1)),  # Valores inteiros
                tickCount=int(max(equipe_counts['quantidade'])) + 1,  # Número de ticks
                format='d'  # Formato decimal sem casas
            )),
    tooltip=["equipe", "quantidade"]
    ).properties(
        width=500,
        height=300
    )

    st.markdown("#### **Total de Serviços Realizados por Setor**")
    st.altair_chart(chart, use_container_width=True)