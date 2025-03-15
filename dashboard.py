import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard de Vendas")

# URL da planilha publicada no Google Sheets (substitua pelo seu link)
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQoxoiVZ7UfM0vHtkieyby0zOQrtBl19D5R6j5wb8dKR62izmZjWuC3qeoAX9-wnO2AlVaSfqvK7pn7/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)  # Cache dos dados por 60 segundos
def load_data():
    return pd.read_csv(URL_SHEET)

df = load_data()

st.title("📊 Dashboard de Vendas")

# 🔹 Tratamento da coluna Data
if "Data" in df.columns:
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df = df.dropna(subset=["Data"])  # Remove linhas com datas inválidas
    df["Ano"] = df["Data"].dt.year
    df["Mês"] = df["Data"].dt.strftime('%Y-%m')  # Formato: "2024-01"
else:
    st.error("❌ Erro: A coluna 'Data' não foi encontrada no dataset!")

# Criando filtros
col1, col2, col3, col4 = st.columns(4)

with col1:
    regional_selecionada = st.selectbox("🌎 Escolha a Regional:", ["Todas"] + list(df["Regional"].unique()))
with col2:
    cidade_selecionada = st.selectbox("🏙️ Escolha a Cidade:", ["Todas"] + list(df["Cidade"].unique()))
with col3:
    produto_selecionado = st.selectbox("📦 Escolha o Produto:", ["Todos"] + list(df["Produto"].unique()))
with col4:
    vendedor_selecionado = st.selectbox("🧑‍💼 Escolha o Vendedor:", ["Todos"] + list(df["Vendedor"].unique()))

# 🔹 Filtro de Período (Mês e Ano)
col_periodo1, col_periodo2 = st.columns(2)

with col_periodo1:
    mes_inicial = st.selectbox("📆 Mês Inicial:", sorted(df["Mês"].unique()))
with col_periodo2:
    mes_final = st.selectbox("📆 Mês Final:", sorted(df["Mês"].unique()), index=len(df["Mês"].unique()) - 1)

# 🔹 Aplicando os filtros
df_filtrado = df.copy()

if regional_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Regional"] == regional_selecionada]
if cidade_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Cidade"] == cidade_selecionada]
if produto_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Produto"] == produto_selecionado]
if vendedor_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Vendedor"] == vendedor_selecionado]

# 🔹 Aplicando Filtro de Período
df_filtrado = df_filtrado[(df_filtrado["Mês"] >= mes_inicial) & (df_filtrado["Mês"] <= mes_final)]

# Criando gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Vendas por Produto")
    fig_produto = px.bar(df_filtrado, x="Produto", y="Valor", color="Produto", title="Vendas por Produto", text_auto=True)
    st.plotly_chart(fig_produto, use_container_width=True)

with col2:
    st.subheader("📊 Vendas por Vendedor")
    fig_vendedor = px.bar(df_filtrado, x="Vendedor", y="Valor", color="Vendedor", title="Vendas por Vendedor", text_auto=True)
    st.plotly_chart(fig_vendedor, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Vendas por Regional")
    fig_regional = px.pie(df_filtrado, names="Regional", values="Valor", title="Distribuição de Vendas por Regional")
    st.plotly_chart(fig_regional, use_container_width=True)

with col4:
    st.subheader("📈 Evolução das Vendas")
    
    if not df_filtrado.empty:
        fig_evolucao = px.line(df_filtrado.sort_values("Data"), x="Data", y="Valor", title="Evolução das Vendas")
        st.plotly_chart(fig_evolucao, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado disponível para o período selecionado!")

# Exibir tabela com os dados filtrados
st.subheader("📄 Dados Filtrados:")
st.dataframe(df_filtrado)

