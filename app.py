import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- SENHA ADMIN ----------------
SENHA_ADMIN = "LPA2026"

# ---------------- LINK DA PLANILHA ----------------
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1F8HC2D8UxRc5R_QBdd-zWu7y6Twqyk3r0NTPN0HCWUI/export?format=xlsx"

# ---------------- ESTADO DO SITE ----------------
if "status_site" not in st.session_state:
    st.session_state.status_site = "FECHADO"

# ---------------- CABEÇALHO ----------------
st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")
st.divider()

# ---------------- ÁREA ADMIN ----------------
st.markdown("### 🔒 Área Administrativa")

senha = st.text_input("Senha administrativa", type="password")

if senha == SENHA_ADMIN:
    st.success("Acesso administrativo liberado")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔓 ABRIR CONSULTA"):
            st.session_state.status_site = "ABERTO"
            st.success("Consulta ABERTA")

    with col2:
        if st.button("🔒 FECHAR CONSULTA"):
            st.session_state.status_site = "FECHADO"
            st.warning("Consulta FECHADA")

elif senha:
    st.error("Senha incorreta")

st.divider()

# ---------------- STATUS ----------------
st.markdown(f"### 📌 Status atual: **{st.session_state.status_site}**")

# ---------------- BLOQUEIO ----------------
if st.session_state.status_site == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ---------------- CARREGAR BASE ----------------
@st.cache_data(ttl=300)
def carregar_base():
    df = pd.read_excel(URL_PLANILHA)
    df.columns = df.columns.str.strip()
    return df.fillna("")

try:
    df = carregar_base()
except Exception as e:
    st.error("Erro ao carregar a base de dados.")
    st.stop()

# ---------------- CONSULTA ----------------
st.markdown("### 🔍 Consulta")

nome = st.text_input("Digite o nome do motorista")

if nome:
    resultado = df[df["Nome"].str.contains(nome, case=False, na=False)]

    if resultado.empty:
        st.warning("❌ Nenhuma rota atribuída para este motorista.")
    else:
        for _, r in resultado.iterrows():
            st.success(f"🚚 Rota {r['Rota']} | {r['Nome']} | {r['Placa']}")
