import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- LIMPEZA DE CACHE INICIAL ----------------
st.cache_data.clear()

# ---------------- ESTILO (CSS) ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f6f7f9;
}
.header-card {
    background: white;
    padding: 24px 28px;
    border-radius: 16px;
    border-left: 6px solid #ff7a00;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
.header-title {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
}
.header-sub {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
}
.header-info {
    margin-top: 14px;
    font-size: 15px;
    color: #374151;
}
.result-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 16px;
}
.result-title {
    font-size: 20px;
    font-weight: 700;
    color: #ff7a00;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO ----------------
st.markdown("""
<div class="header-card">
    <div class="header-title">🚚 SPX | Consulta de Rotas</div>
    <div class="header-sub">Shopee Express • Operação Logística</div>
    <div class="header-info">
        Consulta disponível <strong>somente após a alocação das rotas</strong>.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- URL DA PLANILHA ----------------
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"

# ---------------- CONTROLE (ABERTO / FECHADO) ----------------
@st.cache_data(ttl=300)
def carregar_controle():
    df_controle = pd.read_excel(URL_PLANILHA, sheet_name="controle")
    df_controle.columns = df_controle.columns.str.strip().str.lower()

    if "status_consulta" not in df_controle.columns:
        return "ABERTO"

    return str(df_controle.iloc[0]["status_consulta"]).strip().upper()

status_site = carregar_controle()

if status_site == "FECHADO":
    st.warning("🚫 Consulta temporariamente indisponível. Aguarde a liberação das rotas.")
    st.stop()

# ---------------- BASE PRINCIPAL + TIMESTAMP ----------------
@st.cache_data(ttl=300)
def carregar_base():
    df = pd.read_excel(URL_PLANILHA)
    df.columns = df.columns.str.strip()
    df = df.fillna("")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return df, timestamp

df, ultima_atualizacao = carregar_base()

# ---------------- SIDEBAR ADMIN ----------------
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    st.markdown("---")

    senha = st.text_input("Senha ADMIN", type="password")

    if senha == "LPA2026":
        st.success("Acesso liberado")

        st.markdown(f"**🔄 Status da consulta:** `{status_site}`")
        st.markdown(f"**🕒 Última atualização:** `{ultima_atualizacao}`")

        if st.button("🔁 Atualizar agora"):
            st.cache_data.clear()
            st.success("Atualizando base…")
            st.rerun()

        st.markdown("---")
        st.markdown("📊 **Base completa**")
        st.dataframe(df, use_container_width=True)

    elif senha:
        st.error("Senha incorreta")

# ---------------- CONFERÊNCIA DAS COLUNAS ----------------
colunas_necessarias = ["Placa", "Nome", "Bairro", "Rota", "Cidade"]

for col in colunas_necessarias:
    if col not in df.columns:
        st.error(f"Coluna obrigatória não encontrada: {col}")
        st.stop()

# ---------------- CAMPO DE BUSCA ----------------
nome_busca = st.text_input(
    "Digite o **nome completo ou parcial** do motorista:",
    placeholder="Ex: Luan de Oliveira"
)

# ---------------- RESULTADO (INALTERADO) ----------------
if nome_busca:
    resultado = df[df["Nome"].str.contains(nome_busca, case=False, na=False)]

    if resultado.empty:
        st.warning("❌ Nenhuma rota atribuída para este motorista.")
    else:
        st.success(f"🚚 {len(resultado)} rota(s) encontrada(s)")

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
