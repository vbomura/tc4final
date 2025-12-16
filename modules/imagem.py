import streamlit as st
import os

def app():
    st.title("Informações sobre a Predição")

    st.markdown("""
        Para o nosso algoritmo de previsão de faixa de peso adotamos uma estratégia de avaliar o resultado de 3 modelos, Random Forest, Decision Tree e Regressão logística. Os modelos foram escolhidos pois o problema em si não é muito difícil e pelas capacidades de previsão.

        Para fazer a predição identificamos seis variáveis que tem correlação forte com a categoria de peso (peso, altura, idade, histórico familiar de obesidade, consumo entre refeições e consumo frequente de calorias). Para testar os modelos com as variáveis criamos um pipeline, nele pudemos parametrizar e validar cada um deles. 
                
        **Com 94% de precisão, Decision Tree** foi o melhor modelo, seguido de Random Forest (mesmo resultado de 94%) e Regressão Logística (52%). O resultado igual de Random Forest e Decision Tree é condizente considerando que o primeiro se trata de fazer o segundo várias vezes. Dito isso, para uso menor de recursos optamos pelo Decision Tree.

        Entrando em mais detalhes sobre o resultado, Decion Tree apresentou uma precisão muito boa em todos as faixas de peso, se mantendo acima 90% em todas as faixas. Sua taxa de recall, ou seja, falsos positivos, também foi muito boa, mostrando que o algoritmo consegue classificar com eficácia cada categoria.
        
        Embora o algoritmo tenha apresentado excelentes resultados é sempre bom relembrar que a avaliação de um profissional de saúde é essencial. Além disso, como mostrado no dashboard, outros fatores que não estão na pesquisa podem influenciar a faixa de peso de um paciente, recomenda-se analisar eles também.
    
                
    """)

    st.image("assets/Grafico2.png", caption="")
