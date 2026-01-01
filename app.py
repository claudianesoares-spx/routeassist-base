import streamlit as st
from datetime import datetime

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ================= SENHAS PADRÃO =================
SENHA_ADMIN_PADRAO = "LPA2026"
SENHA_MASTER_PADRAO = "MASTER2026"

# ================= SESSION STATE =================
if "status_site" not in st.session_state:
    st.session_state.status_site = "FECHADO"

if "senha_master" not in st.session_state:
    st.session_state.senha_master = SENHA_MASTER_PADRAO

if "historico" not in st.session_state:
    st.session_state.historico = []

# ================= FUNÇÃO LOG =================
def registrar_acao(usuario, acao):
    st.session_state.historico.append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "usuario": usuario,
        "acao": acao
    })

# ================= CABEÇALHO =================
st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")
st.divider()

# ================= ÁREA ADMINISTRATIVA =================
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    nivel = None

    if senha == st.session_state.senha_master:
        nivel = "MASTER"
        st.success("Acesso MASTER liberado")

    elif senha == SENHA_ADMIN_PADRAO:
        nivel = "ADMIN"
        st.success("Acesso ADMIN liberado")

    elif senha:
        st.error("Senha incorreta")

    # ================= CONTROLES =================
    if nivel in ["ADMIN", "MASTER"]:
        st.markdown("---")
        st.markdown("### ⚙️ Controle da Consulta")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔓 ABRIR"):
                st.session_state.status_site = "ABERTO"
                registrar_acao(nivel, "ABRIU CONSULTA")
                st.success("Consulta ABERTA")

        with col2:
            if st.button("🔒 FECHAR"):
                st.session_state.status_site = "FECHADO"
                registrar_acao(nivel, "FECHOU CONSULTA")
                st.warning("Consulta FECHADA")

    # ================= MASTER ONLY =================
    if nivel == "MASTER":
        st.markdown("---")
        st.markdown("### 🔑 Trocar senha MASTER")

        nova_senha = st.text_input("Nova senha MASTER", type="password")

        if st.button("Salvar nova senha"):
            if nova_senha:
                st.session_state.senha_master = nova_senha
                registrar_acao("MASTER", "ALTEROU SENHA MASTER")
                st.success("Senha MASTER atualizada")
            else:
                st.error("Digite uma senha válida")

        st.markdown("---")
        st.markdown("### 📜 Histórico de ações")

        if st.session_state.historico:
            for h in reversed(st.session_state.historico):
                st.markdown(
                    f"- {h['data']} | **{h['usuario']}** | {h['acao']}"
                )
        else:
            st.info("Nenhuma ação registrada")

# ================= STATUS ATUAL =================
st.markdown(f"### 📌 Status atual: **{st.session_state.status_site}**")
st.divider()

# ================= BLOQUEIO =================
if st.session_state.status_site == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ================= CONSULTA (MANTIDA) =================
st.markdown("### 🔍 Consulta")

nome = st.text_input("Digite o nome do motorista")

if nome:
    st.info("⚠️ Base de dados ainda não conectada.")
