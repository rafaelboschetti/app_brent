import os
import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Explicação do Modelo", layout="wide")

st.title("Análise e Previsão do Preço do Petróleo Brent")

# Definir caminho das imagens dinamicamente
caminho_imagens = os.path.join(os.getcwd(), "imagens")

# Função auxiliar para carregar imagens com segurança
def carregar_imagem(nome_arquivo, legenda):
    caminho_arquivo = os.path.join(caminho_imagens, nome_arquivo)
    if os.path.exists(caminho_arquivo):  # Verifica se o arquivo existe
        st.image(caminho_arquivo, caption=legenda, use_container_width=True)
    else:
        st.warning(f"⚠️ Imagem não encontrada: {nome_arquivo}")

# Introdução detalhada
st.header("Introdução ao Projeto")
st.markdown("""
O preço do petróleo Brent é um dos principais indicadores econômicos globais, sendo influenciado por fatores como crises geopolíticas, demanda por energia, políticas governamentais e flutuações de oferta. Este estudo tem como objetivo analisar a variação histórica do preço do Brent e utilizar modelos de aprendizado de máquina para prever suas cotações futuras.

A abordagem adotada combina técnicas de **análise de séries temporais** e **aprendizado de máquina**, permitindo identificar padrões sazonais, tendências de longo prazo e possíveis anomalias. Além disso, o modelo preditivo foi treinado com dados históricos para fornecer previsões diárias do preço do petróleo para os próximos 30 dias.
""")

# Decomposição da Série Temporal
st.header("Decomposição da Série Temporal")
st.markdown("""
Para compreender melhor os componentes que influenciam a variação do preço do petróleo, realizamos uma decomposição da série temporal. A decomposição divide a série em três componentes principais:

- **Tendência:** Representa a evolução de longo prazo do preço do petróleo, capturando aumentos e quedas graduais ao longo dos anos.
- **Sazonalidade:** Indica padrões que se repetem em intervalos regulares, como variações anuais ou mensais que podem estar relacionadas a fatores sazonais da economia global.
- **Resíduo:** Representa a parte aleatória da série, ou seja, as variações que não podem ser explicadas pelos componentes de tendência e sazonalidade.

Essa análise auxilia na identificação de fatores estruturais que influenciam o comportamento do mercado, permitindo uma modelagem mais precisa para a previsão futura.
""")
carregar_imagem("decomposicao.png", "Decomposição da Série Temporal")

# Análise de Autocorrelação
st.header("Análise de Autocorrelação")
st.markdown("""
A autocorrelação mede o grau de dependência entre os valores passados e futuros de uma série temporal. Para avaliar essa relação no preço do petróleo, utilizamos os gráficos de:

- **Autocorrelação (ACF):** Indica a correlação entre a série e seus valores defasados ao longo do tempo.
- **Autocorrelação Parcial (PACF):** Mostra a correlação direta entre um ponto no tempo e seus lags, eliminando o efeito de intermediários.

Esses gráficos ajudam na identificação da quantidade de defasagens (lags) que devem ser incluídas no modelo preditivo, garantindo que ele capture as relações temporais relevantes da série.
""")
carregar_imagem("autocorrelacao.png", "Gráficos de Autocorrelação (ACF e PACF)")

# Construção do Modelo Preditivo
st.header("Construção do Modelo Preditivo")
st.markdown("""
Para a previsão do preço do petróleo Brent, utilizamos o algoritmo **XGBoost**, uma técnica baseada em árvores de decisão que é altamente eficiente para tarefas de séries temporais.

### **Etapas do processo de modelagem:**
1. **Criação de Features Temporais:** Foram geradas novas variáveis a partir da série original, como:
   - **Lags temporais:** Utilizados para capturar padrões passados e prever valores futuros.
   - **Médias móveis:** Permitem suavizar as oscilações da série e identificar tendências mais estáveis.

2. **Divisão dos Dados:** A base foi dividida em:
   - **Treinamento (80%)**: Para treinar o modelo com dados históricos.
   - **Teste (20%)**: Para validar as previsões do modelo.

3. **Treinamento do Modelo:** O **XGBoost** foi ajustado utilizando técnicas de otimização para obter um melhor desempenho preditivo. Ele leva em consideração padrões de curto e longo prazo, além de lidar bem com dados ruidosos.

4. **Avaliação do Modelo:** Utilizamos métricas como **Erro Médio Absoluto (MAE)**, **Raiz do Erro Quadrático Médio (RMSE)** e **Coeficiente de Determinação (R²)** para medir a precisão das previsões.
""")

# Comparação entre Valores Reais e Previstos
st.header("Comparação entre Valores Reais e Previstos")
st.markdown("""
Após o treinamento, o modelo foi testado utilizando dados históricos recentes para verificar sua capacidade de previsão. O gráfico abaixo mostra a comparação entre os valores reais do preço do petróleo e as previsões geradas pelo modelo:

- **Linha Azul:** Representa o preço real do petróleo Brent ao longo do tempo.
- **Linha Vermelha:** Representa as previsões feitas pelo modelo XGBoost.

A proximidade das duas curvas indica a precisão do modelo, demonstrando que ele consegue captar bem as tendências e flutuações do mercado.
""")
carregar_imagem("comparacao_real_previsto.png", "Comparação de Previsões - XGBoost")

# Distribuição dos Erros do Modelo
st.header("Distribuição dos Erros do Modelo")
st.markdown("""
Para entender melhor a precisão do modelo, analisamos a distribuição dos erros das previsões. O erro é calculado como a diferença entre o valor real e o valor previsto.

- Se os erros forem próximos de zero e distribuídos de maneira simétrica, significa que o modelo não apresenta viés significativo.
- Se houver desvios para um lado, pode indicar que o modelo está superestimando ou subestimando sistematicamente os valores.

A análise da distribuição dos resíduos nos ajuda a validar se o modelo é adequado para previsão ou se necessita ajustes.
""")
carregar_imagem("distribuicao_erros.png", "Distribuição dos Erros do Modelo")

# Previsão para os Próximos 30 Dias
st.header("Previsão para os Próximos 30 Dias")
st.markdown("""
Por fim, o modelo foi utilizado para gerar previsões diárias do preço do petróleo para os próximos 30 dias. Essas previsões foram ajustadas considerando a tendência observada nos últimos meses.

Os resultados fornecem um indicativo do comportamento esperado do preço do petróleo Brent no curto prazo, auxiliando na tomada de decisões estratégicas por parte de investidores e empresas do setor de energia.
""")

st.success("""
Este estudo demonstra como a combinação de **técnicas de séries temporais** e **aprendizado de máquina** pode ser utilizada para prever o preço do petróleo. A análise detalhada dos dados históricos, junto com a modelagem preditiva, permite obter insights valiosos para a tomada de decisão em mercados financeiros e setores relacionados à energia.
""")
