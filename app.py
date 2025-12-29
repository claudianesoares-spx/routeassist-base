import unicodedata
import re

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"\s+", " ", texto)  # remove espaços extras
    
    return texto

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="📦",
    layout="centered"
)

# ---------------- ESTILO SPX ----------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        max-width: 520px;
    }

    h1 {
        color: #ee4d2d;
        text-align: center;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .card {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        margin-top: 1rem;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- TÍTULO ----------------
st.markdown("<h1>SPX | Consulta de Rotas</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Ferramenta interna de apoio à operação</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='subtitle'>📅 Base atualizada em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>",
    unsafe_allow_html=True
)

# ---------------- CARREGAR BASE ----------------
try:
    df = pd.read_excel("rotas.xlsx")
    df.columns = df.columns.str.strip().str.lower()

    # normalizar coluna nome
    df["nome_normalizado"] = df["nome"].apply(normalizar_texto)

except Exception:
    st.error("Erro ao carregar a base de dados.")
    st.stop()

# ---------------- BUSCA ----------------
st.markdown("### 🔎 Buscar rota")
nome = st.text_input("Nome completo do motorista")

if nome:
    nome_busca = normalizar_texto(nome)

    resultado = df[
        df["nome_normalizado"] == nome_busca
    ]

    if not resultado.empty:
        rota = resultado.iloc[0]["rota"]
        bairro = resultado.iloc[0]["bairro"]

        st.markdown(f"""
        <div class="card">
            <h4>✅ Rota</h4>
            <strong>{rota}</strong>
            <hr>
            <h4>📍 Bairro</h4>
            <strong>{bairro}</strong>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning(
            "❌ Motorista não encontrado.\n\n"
            "✔️ Verifique se digitou o nome completo conforme cadastro."
        )
else:
    st.info("Digite o nome completo do motorista para consultar a rota.")

# ---------------- RODAPÉ ----------------
st.markdown("""
<div class="footer">
    SPX | Shopee Express<br>
    Base atualizada diariamente após alocação
</div>
""", unsafe_allow_html=True)


