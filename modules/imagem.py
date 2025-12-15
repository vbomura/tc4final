import streamlit as st
import os

def app():
    st.title("Informações sobre a Predição")

    st.markdown("""
        Para o nosso algoritmo de previsão de faixa de peso adotamos uma estratégia de avaliar o resultado de 3 modelos, Random Forest, Decision Tree e Regressão logística. Os modelos foram escolhidos pois o problema em si não é muito difícil e pelas capacidades de previsão.

        Para fazer a predição identificamos seis variáveis que tem correlação forte com a categoria de peso (peso, altura, idade, histórico familiar de obesidade, consumo entre refeições e consumo frequente de calorias). Para testar os modelos com as variáveis criamos um pipeline, nele pudemos parametrizar e validar cada um deles. 
                
        **Com 94%% de precisão, Decision Tree** foi o melhor modelo, seguido de Random Forest (mesmo resultado de 94%) e Regressão Logística (52%). O resultado igual de Random Forest e Decision Tree é condizente considerando que o primeiro se trata de fazer o segundo várias vezes. Dito isso, para uso menor de recursos optamos pelo Decision Tree.

        Entrando em mais detalhes do melhor modelo, Decion Tree apresentou uma precisão muito boa em todos as faixas de peso, se mantendo acima 90% em todas. Sua taxa de recall, ou seja, falsos positivos, também foi muito baixa, mostrando que o algoritmo consegue classificar bem as faixas de peso
    
                
    """)

    st.image("assets/Grafico2.png", caption="")