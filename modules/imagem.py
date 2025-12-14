import streamlit as st
import os

def app():
    st.title("Informações sobre a Predição")

    st.markdown("""
        Para o nosso algoritmo de previsão de faixa de peso adotamos uma estratégia de avaliar o resultado de 3 modelos, Random Forest, Decision Tree e Regressão logística. Os modelos foram escolhidos pois o problema em si não é muito difícil e pelas capacidades de previsão.

        Para fazer a predição identificamos cinco variáveis que tem correlação forte com a categoria de peso (peso, idade, histórico familiar de obesidade, consumo entre refeições e consumo frequente de calorias). Para testar os modelos com as variáveis criamos um pipeline, nele pudemos parametrizar e validar cada um deles. 
                
        **Com 83% de precisão, Random Forest** foi o melhor modelo, seguido da Árvore de Decisão (81%) e Regressão Logística (52%). Os resultados são condizentes com as especialidades de cada algoritmo.

        Entrando em mais detalhes do melhor modelo, Random Forest apresentou uma precisão boa nos "extremos" da categoria (obesidade e peso insuficiente), a menor acurácia de precisão foi em relação a pessoas dentro do "peso normal", mas ainda assim a precisão ficou dentro da faixa de 75%. Vale destacar que, com base no recall, o algoritmo teve uma tendência a apontar falsos positivos para as pessoas dentro do peso adequado.

                                
    """)

    st.image("assets/Grafico2.png", caption="")