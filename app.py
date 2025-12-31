import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- ESTILO SPX (LARANJA) ----------------
st.markdown("""
<style>
.main {
    background-color: #fffaf5;
}

h1, h2, h3 {
    color: #111827;
    font-weight: 800;
}

input {
    border-radius: 12px !important;
    border: 2px solid #fb923c !important;
}

.stButton > button {
    background-color: #f97316;
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
}

.stAlert-success {
    background-color: #fff7ed;
    border-left: 6px solid #f97316;
}

.stAlert-warning {
    background-color: #fff1f2;
    border-left: 6px solid #ef4444;
}

.stAlert-info {
    background-color: #ffedd5;
    border-left: 6px solid #fb923c;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1f2937);
}

section[data-testid="stSidebar"] * {
    color: white;
}

.card {
    background-color: white;
    border-radius: 16px;
    padding: 18px;
    margin-top: 16px;
    border: 1px solid #fed7aa;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #ea580c;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ADMIN ----------------
with st.sidebar:
    st.markdown("### 🔐 Área Administrativa")
    senha = st.text_input("Senha admin", type="password")

    if senha == "LPA2026":
        st.success("Acesso liberado")
    elif senha:
        st.error("Senha incorreta")

# ---------------- TÍTULO ----------------
st.markdown("# 🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")

# ---------------- BASE ----------------
URL = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"

@st.cache_data
def carregar_base():
    df = pd.read_excel(
        URL,
        sheet_name="CONSULTA ROTAS",
        dtype=str
    )

    df.columns = df.columns.str.strip()

    for col in ["Placa", "Nome", "Bairro", "Rota", "Cidade"]:
        df[col] = df[col].fillna("").astype(str)

    return df

df = carregar_base()

# ---------------- BUSCA ----------------
nome_busca = st.text_input(
    "Digite o nome completo ou parcial do motorista:",
    placeholder="Ex: Adriana Cardoso"
)

# ---------------- RESULTADO ----------------
if nome_busca:
    resultado = (
        df[df["Nome"].str.contains(nome_busca, case=False, na=False)]
        .reset_index(drop=True)
    )

    if resultado.empty:
        st.warning("❌ Nenhuma rota encontrada para este nome.")
    else:
        st.success(f"🚚 {len(resultado)} rota(s) encontrada(s)")

        for _, row in resultado.iterrows():
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🚚 Rota {row['Rota']}</div>
                <p><strong>👤 Motorista:</strong> {row['Nome']}</p>
                <p><strong>🚘 Placa:</strong> {row['Placa']}</p>
                <p><strong>📍 Bairro:</strong> {row['Bairro']}</p>
                <p><strong>🏙️ Cidade:</strong> {row['Cidade']}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Digite um nome para consultar a rota.")
