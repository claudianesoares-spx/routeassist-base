import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title="RouteAssist | Apoio Operacional",
    page_icon="🧭",
    layout="centered"
)

# ================= CACHE (SOMENTE ADMIN | 60s) =================
@st.cache_data(ttl=60, show_spinner=False)
def carregar_rotas_admin(url):
    df = pd.read_excel(url)
    df["ID"] = df["ID"].astype(str).str.strip()
    return df

# ================= ARQUIVO DE PERSISTÊNCIA =================
CONFIG_FILE = "config.json"

# ================= CONFIG PADRÃO =================
DEFAULT_CONFIG = {
    "status_site": "FECHADO",
    "senha_master": "MASTER2026",
    "historico": []
}

# ================= LOAD / SAVE =================
def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

config = load_config()

# ================= FUNÇÃO LOG =================
def registrar_acao(usuario, acao):
    config["historico"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "usuario": usuario,
        "acao": acao
    })
    save_config(config)

# ================= REGRA DE HORÁRIO (10:05) =================
agora = datetime.now()
liberar_dobra = (
    agora.hour > 10 or
    (agora.hour == 10 and agora.minute >= 5)
)

# ================= ESTILO =================
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-left: 6px solid #ff7a00;
    margin-bottom: 16px;
}
.card h4 {
    margin-bottom: 12px;
}
.card p {
    margin: 4px 0;
    font-size: 15px;
}
.card a {
    display: inline-block;
    margin-top: 10px;
    color: #ff7a00;
    font-weight: bold;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ================= CABEÇALHO =================
st.title("🧭 RouteAssist")
st.markdown(
    "Ferramenta de **apoio operacional** para alocação e redistribuição de rotas, "
    "atuando de forma complementar ao sistema oficial **SPX**."
)
st.divider()

# ================= SIDEBAR / ADMIN =================
nivel = None

with st.sidebar:
    with st.expander("🔒 Área Administrativa", expanded=False):

        senha = st.text_input("Senha", type="password")

        if senha == config["senha_master"]:
            nivel = "MASTER"
            st.success("Acesso MASTER liberado")
        elif senha == "LPA2026":
            nivel = "ADMIN"
            st.success("Acesso ADMIN liberado")
        elif senha:
            st.error("Senha incorreta")

        if nivel in ["ADMIN", "MASTER"]:
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔓 ABRIR"):
                    config["status_site"] = "ABERTO"
                    registrar_acao(nivel, "ABRIU CONSULTA")
                    st.success("Consulta ABERTA")

            with col2:
                if st.button("🔒 FECHAR"):
                    config["status_site"] = "FECHADO"
                    registrar_acao(nivel, "FECHOU CONSULTA")
                    st.warning("Consulta FECHADA")

# ================= STATUS ATUAL =================
st.markdown(f"### 📌 Status atual: **{config['status_site']}**")
st.divider()

# ================= PAINEL OPERACIONAL (ADMIN ONLY) =================
if nivel in ["ADMIN", "MASTER"]:

    url_rotas = "https://docs.google.com/spreadsheets/d/1F8HC2D8UxRc5R_QBdd-zWu7y6Twqyk3r0NTPN0HCWUI/export?format=xlsx"
    df_admin = carregar_rotas_admin(url_rotas)

    rotas_disponiveis_admin = df_admin[
        df_admin["ID"].isna() |
        (df_admin["ID"] == "") |
        (df_admin["ID"].str.lower() == "nan") |
        (df_admin["ID"] == "-")
    ]

    st.markdown("## 📊 Painel Operacional")

    st.info(f"""
📌 **Status do sistema:** {config['status_site']}  
🕒 **Horário atual:** {agora.strftime('%H:%M')}  
📦 **Dobra liberada:** {"SIM" if liberar_dobra else "NÃO"}
""")

    c1, c2, c3 = st.columns(3)
    c1.metric("🚚 Total de rotas", len(df_admin))
    c2.metric("✅ Atribuídas", len(df_admin) - len(rotas_disponiveis_admin))
    c3.metric("📦 Disponíveis", len(rotas_disponiveis_admin))

    if not rotas_disponiveis_admin.empty:
        st.dataframe(
            rotas_disponiveis_admin[
                ["Rota", "Cidade", "Bairro", "Tipo Veiculo"]
            ].sort_values(by=["Cidade", "Bairro"]),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

# ================= BLOQUEIO PARA DRIVERS =================
if config["status_site"] == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ================= CONSULTA DRIVER (ORIGINAL / SEM CACHE) =================
st.markdown("### 🔍 Consulta Operacional de Rotas")
id_motorista = st.text_input("Digite seu ID de motorista")

# 🔒 A PARTIR DAQUI: É EXATAMENTE O SEU CÓDIGO ORIGINAL
# (sem cache, sem painel, sem alteração)
