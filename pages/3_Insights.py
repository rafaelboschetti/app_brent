import streamlit as st
import pandas as pd
import plotly.express as px
import utils

# Configuração da página
st.set_page_config(page_title="Insights Históricos", layout="wide")

# Carregar dados históricos
df = utils.get_brent_data()

# Criar interface
st.title("Insights sobre a Cotação do Petróleo Brent")

# Criar gráfico idêntico ao da primeira página
fig_insights = px.line(df, x=df.index, y="valor", title="Histórico de preços do Brent")

# 📍 Lista de eventos históricos
eventos = [
    {"data": "2014-06-20", "descricao": "Boom do Xisto nos EUA"},
    {"data": "2016-01-20", "descricao": "Excesso de Oferta e Queda Recorde"},
    {"data": "2020-03-20", "descricao": "Colapso devido à Pandemia da COVID-19"},
    {"data": "2022-03-08", "descricao": "Alta Recorde pela Guerra na Ucrânia"},
]

# Adicionar marcadores ao gráfico
for evento in eventos:
    if evento["data"] in df.index:
        valor = df.loc[evento["data"], "valor"]

        # Adicionar marcador vermelho nos eventos
        fig_insights.add_scatter(
            x=[evento["data"]],
            y=[valor],
            mode="markers+text",
            marker=dict(color="red", size=10, symbol="circle"),
            text=["📍"],  # Símbolo de marcador
            textposition="top center",
            showlegend=False  # Remover legenda para não poluir o gráfico
        )

# Configuração do eixo X para mostrar apenas anos
fig_insights.update_xaxes(
    tickformat="%Y",  # Mostrar apenas o ano (ex: 2014, 2015, ...)
    dtick="M12"  # Define os ticks a cada 12 meses (1 ano)
)

# Configuração do eixo Y
fig_insights.update_yaxes(title="Preço (USD)")

# Exibir gráfico no Streamlit
st.plotly_chart(fig_insights, use_container_width=True)

# 📌 Exibir análise detalhada dos insights
st.markdown("## Análise Histórica Detalhada dos Principais Eventos")

insights = [
    {
        "ano": "2014",
        "titulo": "Boom do Xisto nos EUA e Queda dos Preços",
        "descricao": """
        O petróleo de xisto revolucionou a indústria energética nos Estados Unidos. Novas tecnologias de fraturamento hidráulico (fracking) permitiram um aumento massivo 
        da produção de petróleo, reduzindo a dependência dos EUA do petróleo importado. Como consequência, a oferta global cresceu rapidamente, 
        levando a OPEP a manter sua produção elevada para não perder participação de mercado.

        🔹 **Efeito no mercado:**  
        - Os preços começaram a cair rapidamente a partir de **junho de 2014**, saindo de valores acima **de \$110 por barril** para menos **de $50** no final do ano.  
        - Países exportadores, como **Venezuela, Rússia e Arábia Saudita**, enfrentaram crises fiscais severas.  
        """
    },
    {
        "ano": "2016",
        "titulo": "Excesso de Oferta e Colapso do Petróleo",
        "descricao": """
        O mercado global entrou em uma crise prolongada devido à superprodução da OPEP e a dificuldades na demanda global. A Arábia Saudita e seus aliados 
        mantiveram altas taxas de produção, esperando forçar pequenos produtores de xisto nos EUA a saírem do mercado.

        🔹 **Efeito no mercado:**  
        - O preço do petróleo Brent caiu para **menos de $30 por barril** em **janeiro de 2016**, sendo um dos menores valores da década.  
        - Empresas petrolíferas reduziram investimentos e algumas chegaram à falência.  
        - A recuperação do mercado começou após cortes de produção pela OPEP e aliados, formando a aliança conhecida como **OPEP+**.  
        """
    },
    {
        "ano": "2020",
        "titulo": "Colapso Histórico Durante a Pandemia da COVID-19",
        "descricao": """
        A pandemia da COVID-19 levou a um colapso sem precedentes no consumo de petróleo. Com as restrições de mobilidade, fechamento de fronteiras e queda da atividade econômica, 
        a demanda por combustíveis caiu drasticamente.

        🔹 **Efeito no mercado:**  
        - Em **março de 2020**, os preços do Brent desabaram para **menos de $20 por barril**.  
        - Pela primeira vez na história, o petróleo WTI (referência nos EUA) chegou a ser negociado a preços **negativos** em abril de 2020.  
        - Governos ao redor do mundo intervieram com pacotes de estímulo para evitar uma recessão global ainda maior.  
        """
    },
    {
        "ano": "2022",
        "titulo": "Guerra na Ucrânia e o Disparo dos Preços do Petróleo",
        "descricao": """
        A invasão da Ucrânia pela Rússia, em **fevereiro de 2022**, desencadeou uma das maiores crises energéticas das últimas décadas.  
        Sanções contra a Rússia limitaram a exportação de petróleo e gás, reduzindo a oferta global em um momento de recuperação pós-pandemia.

        🔹 **Efeito no mercado:**  
        - O petróleo Brent ultrapassou **$120 por barril** em **março de 2022**, atingindo o maior valor desde 2008.  
        - A inflação energética impactou consumidores e empresas ao redor do mundo, levando a medidas de racionamento e subsídios governamentais.  
        - Grandes importadores, como **China e Índia**, aumentaram compras de petróleo russo com desconto, mudando a dinâmica do comércio global de petróleo.  
        """
    }
]

# Exibir insights detalhados
for insight in insights:
    st.markdown(f"### {insight['ano']} - {insight['titulo']}")
    st.write(insight["descricao"])
