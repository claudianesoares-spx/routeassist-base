import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- ARQUIVOS ----------------
CONFIG_FILE = "config.json"
LOG_FILE = "logs.csv"

# ---------------- CONFIG INICIAL ----------------
def carregar_config():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "senha_master": "MASTER2026",
            "senha_operacional": "LPA2026",
            "status_site": "ABERTO"
        }
        with open(CONFIG_FILE, "w") as f:
            import json
            json.dump(config, f)
    else:
        import json
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        config.setdefault("senha_master", "MASTER2026")
        config.setdefault("senha_operacional", "LPA2026")
        config.setdefault("status_site", "ABERTO")
    return config

def salvar_config(config):
    import json
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = carregar_config()

# ---------------- LOGS ----------------
def registrar_log(acao, nivel):
    linha = {
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Ação": acao,
        "Acesso": nivel
    }
    if not os.path.exists(LOG_FILE):
        pd.DataFrame([linha]).to_csv(LOG_FILE, index=False)
    else:
        pd.DataFrame([linha]).to_csv(LOG_FILE, mode="a", header=False, index=False)

# ---------------- LIMPEZA AUTOMÁTICA DE LOGS (3 DIAS) ----------------
def limpar_logs_3_dias():
    if not os.path.exists(LOG_FILE):
        return
    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty or 'Data' not in df.columns:
            return
        df['Data'] = pd.to_datetime(df['Data'], format="%d/%m/%Y", errors='coerce')
        df = df.dropna(subset=['Data'])
        limite = datetime.now() - timedelta(days=3)
        df_limpo = df[df['Data'] >= limite]
        df_limpo.to_csv(LOG_FILE, index=False)
    except Exception as e:
        st.warning(f"Não foi possível limpar os logs: {e}")

limpar_logs_3_dias()

# ---------------- ESTILO ----------------
st.markdown("""
<style>
.stApp { background-color: #f6f7f9; }
.header-card { background: white; padding: 24px; border-radius: 16px; border-left: 6px solid #ff7a00; margin-bottom: 30px; }
.header-title { font-size: 32px; font-weight: 700; color: #1f2937; }
.header-sub { font-size: 14px; color: #6b7280; margin-top: 4px; }
.result-card { background: white; padding: 20px; border-radius: 14px; border: 1px solid #e5e7eb; margin-bottom: 16px; }
.result-title { font-size: 20px; font-weight: 700; color: #ff7a00; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO ----------------
st.markdown("""
<div class="header-card">
    <div class="header-title">🚚 SPX | Consulta de Rotas</div>
    <div class="header-sub">Shopee Express • Operação Logística</div>
</div>
""", unsafe_allow_html=True)

# ---------------- URL PLANILHA ----------------
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1F8HC2D8UxRc5R_QBdd-zWu7y6Twqyk3r0NTPN0HCWUI/export?format=xlsx"

@st.cache_data(ttl=300)
def carregar_base():
    df = pd.read_excel(URL_PLANILHA)
    df.columns = df.columns.str.strip()
    return df.fillna("")

df = carregar_base()

# ---------------- LOGIN ----------------
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    nivel = None
    if senha == config["senha_master"]:
        nivel = "MASTER"
    elif senha == config["senha_operacional"]:
        nivel = "OPERACIONAL"

    if nivel:
        st.success(f"Acesso {nivel}")
        st.markdown(f"**🚦 Status:** `{config['status_site']}`")
        col1, col2 = st.columns(2)
        if col1.button("🟢 Abrir"):
            config["status_site"] = "ABERTO"
            salvar_config(config)
            registrar_log("Consulta ABERTA", nivel)
            st.experimental_rerun()
        if col2.button("🔴 Fechar"):
            config["status_site"] = "FECHADO"
            salvar_config(config)
            registrar_log("Consulta FECHADA", nivel)
            st.experimental_rerun()

        if nivel == "MASTER":
            st.markdown("---")
            st.markdown("### 🔑 Gerenciar Senhas")
            nova_op = st.text_input("Nova senha operacional")
            if st.button("Salvar senha operacional") and nova_op:
                config["senha_operacional"] = nova_op
                salvar_config(config)
                registrar_log("Senha operacional alterada", nivel)
                st.success("Senha operacional atualizada")
            nova_master = st.text_input("Nova senha master")
            if st.button("Salvar senha master") and nova_master:
                config["senha_master"] = nova_master
                salvar_config(config)
                registrar_log("Senha master alterada", nivel)
                st.success("Senha master atualizada")

            st.markdown("---")
            st.markdown("### 📜 Histórico")
            if os.path.exists(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)

    elif senha:
        st.error("Senha incorreta")

# ---------------- BLOQUEIO ----------------
if config["status_site"] == "FECHADO":
    st.warning("Consulta temporariamente indisponível.")
    st.stop()

# ---------------- BUSCA ----------------
nome_busca = st.text_input("Digite o **nome completo ou parcial** do motorista:")

if nome_busca:
    resultado = df[df["Nome"].str.contains(nome_busca, case=False, na=False)]
    if resultado.empty:
        st.warning("❌ Nenhuma rota atribuída.")
    else:
        for _, row in resultado.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">🚚 Rota {row['Rota']}</div>
                <strong>👤 Motorista:</strong> {row['Nome']}<br>
                <strong>🚗 Placa:</strong> {row['Placa']}<br>
                <strong>🏙️ Cidade:</strong> {row['Cidade']}<br>
                <strong>📍 Bairro:</strong> {row['Bairro']}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Digite um nome para consultar a rota.")
