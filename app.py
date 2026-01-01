import streamlit as st

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- INICIALIZAÇÃO DE ESTADO ----------------
if "master_password" not in st.secrets:
    st.secrets["master_password"] = ""
if "oper_password" not in st.secrets:
    st.secrets["oper_password"] = ""
if "status" not in st.secrets:
    st.secrets["status"] = "FECHADO"

# ---------------- CONFIGURAÇÃO INICIAL ----------------
if st.secrets["master_password"] == "" or st.secrets["oper_password"] == "":
    st.title("🔐 Configuração Inicial")

    master = st.text_input("Defina a senha MASTER", type="password")
    oper = st.text_input("Defina a senha OPERACIONAL", type="password")

    if st.button("Salvar senhas"):
        if master and oper:
            st.secrets["master_password"] = master
            st.secrets["oper_password"] = oper
            st.success("✅ Senhas configuradas com sucesso!")
            st.rerun()
        else:
            st.error("Preencha ambas as senhas.")
    st.stop()

# ---------------- LOGIN ----------------
st.title("🚚 SPX | Consulta de Rotas")
senha = st.text_input("Digite sua senha", type="password")

if senha == st.secrets["master_password"]:
    perfil = "MASTER"
elif senha == st.secrets["oper_password"]:
    perfil = "OPERACIONAL"
else:
    perfil = None

if not perfil:
    st.warning("🔒 Acesso restrito")
    st.stop()

st.success(f"Acesso autorizado ({perfil})")

# ---------------- ÁREA ADMINISTRATIVA ----------------
st.divider()
st.subheader("⚙️ Área Administrativa")

st.info(f"Status atual: **{st.secrets['status']}**")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 ABRIR"):
        st.secrets["status"] = "ABERTO"
        st.success("Status alterado para ABERTO")
        st.rerun()

with col2:
    if st.button("🔴 FECHAR"):
        st.secrets["status"] = "FECHADO"
        st.warning("Status alterado para FECHADO")
        st.rerun()

# ---------------- ÁREA DE CONSULTA ----------------
st.divider()
st.subheader("📄 Consulta")

if st.secrets["status"] == "FECHADO":
    st.error("🚫 Consulta fechada no momento.")
else:
    st.success("✅ Consulta aberta.")
    st.write("Aqui entra a lógica de consulta de rotas.")
