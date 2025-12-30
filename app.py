@st.cache_data(ttl=300)
def carregar_planilha():
    try:
        url = "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA_ROTAS/export?format=xlsx"

        df_rotas = pd.read_excel(url, sheet_name="rotas")
        df_controle = pd.read_excel(url, sheet_name="controle", header=None)

        status_site = str(df_controle.iloc[0, 0]).strip().upper()

        df_rotas.columns = df_rotas.columns.str.strip().str.lower()
        df_rotas["nome_normalizado"] = df_rotas["nome"].apply(normalizar_texto)

        return df_rotas, status_site

    except Exception as e:
        st.error(f"❌ Erro ao carregar a planilha: {e}")
        st.stop()
