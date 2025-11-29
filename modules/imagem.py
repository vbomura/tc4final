import streamlit as st
import os

def app():
    st.title("Análise de Dados")
    #st.write("Conteúdo da página de análise...")
    st.image("assets/Grafico.png", caption="Minha imagem")

    st.subheader("Relações entre Hábitos e Obesidade")

    st.markdown("""
    ### Antes de analisar os gráficos...
    Os hábitos diários exercem influência direta no risco de obesidade.  
    A seguir, avaliamos três comportamentos principais:

    1. **Atividade física**
    2. **Consumo de alimentos calóricos**
    3. **Tempo de exposição à tecnologia**

    Essas análises ajudam a entender os padrões comportamentais que contribuem para diferentes níveis de obesidade, como por exemplo, a falta de atividade física + o alto consumo calórico, 
    aceleram as chances da pessoa ter obesidade.
                
    """)