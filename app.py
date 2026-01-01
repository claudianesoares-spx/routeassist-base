import streamlit as st

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- SENHAS ----------------
SENHA_MASTER = "MASTER2026"
SENHA_OPERACIONAL = "OPER2026"

# ---------------- ESTADO ----------------
if "perfil" not in st.session_state:
    st.session_state.perfil = None

if "status_site" not in st.session_state:
    st.session_state.status_site = "FECHADO"

# ---------------- CABEÇALHO ----------------
st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")

st.divider()

# ===================== ÁREA DO USUÁRIO (SEMPRE VISÍVEL) =====================
st.subheader("🔍 Consulta")

if st.session_state.status_site == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
else:
    nome = st.text_input("Digite o nome do motorista")
    if nome:
        st.info("⚠️ Base ainda não conectada.")

# ===================== SIDEBAR ADMINISTRATIVA =====================
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")

    senha = st.text_input("Senha administrativa", type="password")

    if senha == SENHA_MASTER:
        st.session_state.perfil = "MASTER"
        st.success("Acesso MASTER")

    elif senha == SENHA_OPERACIONAL:
        st.session_state.perfil = "OPERACIONAL"
        st.success("Acesso OPERACIONAL")

    elif senha:
        st.error("Senha incorreta")

    # -------- PAINEL MASTER --------
    if st.session_state.perfil == "MASTER":
        st.markdown("---")
        st.markdown("### ⚙️ Controles")

        novo_status = st.radio(
            "Status da Consulta",
            ["ABERTO", "FECHADO"],
            index=0 if st.session_state.status_site == "ABERTO" else 1
        )

        if st.button("Salvar Status"):
            st.session_state.status_site = novo_status
            st.success("Status atualizado")

        if st.button("Sair"):
            st.session_state.perfil = None
            st.rerun()

    # -------- PAINEL OPERACIONAL --------
    if st.session_state.perfil == "OPERACIONAL":
        st.markdown("---")
        st.info("Perfil operacional não possui controles administrativos.")

        if st.button("Sair"):
            st.session_state.perfil = None
            st.rerun()
