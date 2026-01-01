import streamlit as st
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- SENHAS PADRÃO ----------------
if "senha_master" not in st.session_state:
    st.session_state.senha_master = "MASTER2026"

if "senha_operacional" not in st.session_state:
    st.session_state.senha_operacional = "LPA2026"

# ---------------- STATUS DO SITE ----------------
if "status_site" not in st.session_state:
    st.session_state.status_site = "FECHADO"

# ---------------- HISTÓRICO ----------------
if "historico" not in st.session_state:
    st.session_state.historico = []

def registrar_acao(perfil, acao):
    st.session_state.historico.append({
        "data": datetime.now().strftime("%d/%m/%Y"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "perfil": perfil,
        "acao": acao
    })

# ---------------- CABEÇALHO ----------------
st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")
st.divider()

# ---------------- SIDEBAR ADMIN ----------------
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    perfil = None

    if senha == st.session_state.senha_master:
        perfil = "MASTER"
        st.success("Acesso MASTER")

    elif senha == st.session_state.senha_operacional:
        perfil = "OPERACIONAL"
        st.success("Acesso OPERACIONAL")

    elif senha:
        st.error("Senha incorreta")

    # -------- OPERACIONAL --------
    if perfil == "OPERACIONAL":
        st.markdown("### ⚙️ Controle da Consulta")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔓 ABRIR CONSULTA"):
                st.session_state.status_site = "ABERTO"
                registrar_acao("OPERACIONAL", "ABRIU CONSULTA")
                st.success("Consulta ABERTA")

        with col2:
            if st.button("🔒 FECHAR CONSULTA"):
                st.session_state.status_site = "FECHADO"
                registrar_acao("OPERACIONAL", "FECHOU CONSULTA")
                st.warning("Consulta FECHADA")

    # -------- MASTER --------
    if perfil == "MASTER":
        st.markdown("### ⚙️ Controle da Consulta")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔓 ABRIR CONSULTA"):
                st.session_state.status_site = "ABERTO"
                registrar_acao("MASTER", "ABRIU CONSULTA")
                st.success("Consulta ABERTA")

        with col2:
            if st.button("🔒 FECHAR CONSULTA"):
                st.session_state.status_site = "FECHADO"
                registrar_acao("MASTER", "FECHOU CONSULTA")
                st.warning("Consulta FECHADA")

        st.markdown("### 🔑 Alterar Senhas")

        nova_master = st.text_input("Nova senha MASTER", type="password")
        nova_operacional = st.text_input("Nova senha OPERACIONAL", type="password")

        if st.button("Salvar Senhas"):
            if nova_master:
                st.session_state.senha_master = nova_master
                registrar_acao("MASTER", "ALTEROU SENHA MASTER")

            if nova_operacional:
                st.session_state.senha_operacional = nova_operacional
                registrar_acao("MASTER", "ALTEROU SENHA OPERACIONAL")

            st.success("Senhas atualizadas")

        st.markdown("### 📜 Histórico de Ações")
        st.dataframe(st.session_state.historico, use_container_width=True)

# ---------------- STATUS ATUAL ----------------
st.markdown(f"### 📌 Status atual: **{st.session_state.status_site}**")

# ---------------- BLOQUEIO ----------------
if st.session_state.status_site == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ---------------- CONSULTA ----------------
st.markdown("### 🔍 Consulta")
nome = st.text_input("Digite o nome do motorista")

if nome:
    st.info("⚠️ Base de dados ainda não conectada.")
