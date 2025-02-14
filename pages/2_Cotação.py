import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import utils  

# Configuração inicial
st.set_page_config(page_title="Análise do Petróleo Brent", layout="wide")

# Carregar modelo treinado
model = joblib.load("xgboost.joblib")

# Carregar dados históricos
df = utils.get_brent_data()

# Criar features
df = utils.create_features(df)

# Separar dados para previsão
X = df.drop(columns=['valor'])
y = df['valor']

# Criar interface no Streamlit
st.title("Análise da Cotação do Petróleo Brent")
st.write("Este aplicativo prevê o preço do petróleo Brent para os próximos 30 dias.")

# 📈 Gráfico histórico do petróleo Brent
with st.container():
    st.subheader("Evolução do preço do Petróleo Brent")
    fig_historico = px.line(df, x=df.index, y="valor", title="Histórico de preços do Brent")

    fig_historico.update_xaxes(tickformat="%Y", dtick="M12")
    fig_historico.update_yaxes(title="Preço (USD)")

    st.plotly_chart(fig_historico, use_container_width=True)

# 🔹 Organizar os dados recentes e previsões lado a lado
with st.container():
    col1, col2 = st.columns(2)

    # 📌 Exibir tabela de dados recentes formatados corretamente
    with col1:
        st.subheader("Dados mais recentes")
        df_exibicao = df[['valor']].reset_index()
        df_exibicao.columns = ['Data', 'Valor']  
        df_exibicao['Data_str'] = df_exibicao['Data'].dt.strftime("%d/%m/%Y")

        # 🔹 Formatando os valores para exibição correta
        df_exibicao['Valor'] = df_exibicao['Valor'].apply(lambda x: f"${x:,.2f}")

        st.dataframe(df_exibicao[['Data_str', 'Valor']].tail(10).rename(columns={'Data_str': 'Data'}), hide_index=True)

    # 🔮 Exibir previsão futura
    with col2:
        st.subheader("Previsão para os próximos 30 dias")
        future_df = utils.forecast_future(model, df, [1, 5, 10, 20], [5, 10, 20], days=30)

        future_df = future_df.reset_index()
        future_df.columns = ["Data", "Valor"]
        future_df["Data_str"] = future_df["Data"].dt.strftime("%d/%m/%Y")

        # 🔹 Formatando os valores para exibição correta
        future_df['Valor'] = future_df['Valor'].apply(lambda x: f"${x:,.2f}")

        st.dataframe(future_df[['Data_str', 'Valor']].rename(columns={'Data_str': 'Data'}), hide_index=True)

# 📊 Gráfico de previsão futura
with st.container():
    st.subheader("Projeção dos próximos 30 dias")
    
    fig_previsao = px.line(title="Previsão dos próximos 30 dias")
    fig_previsao.add_scatter(x=df.index[-100:], y=df["valor"].iloc[-100:], mode='lines', name='Histórico', line=dict(color="lightblue"))
    fig_previsao.add_scatter(x=future_df["Data"], y=future_df["Valor"], mode='lines', name='Previsão', line=dict(color="red"))

    fig_previsao.update_xaxes(tickformat="%m-%Y", dtick="M2")
    fig_previsao.update_yaxes(title="Preço (USD)")

    st.plotly_chart(fig_previsao, use_container_width=True)

# 🔹 Exibir fonte de dados no final da página
st.markdown("<br>", unsafe_allow_html=True)
st.write("📌 **Fonte dos dados:** Yahoo Finance")
