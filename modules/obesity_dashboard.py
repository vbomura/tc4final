import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    # CONFIGURAÇÃO DO DASHBOARD
    st.set_page_config(
        page_title="Análise de Obesidade",
        layout="wide"
    )

    st.title("Dashboard de Indicadores de Obesidade")
    st.markdown("Análise exploratória com base em hábitos e características demográficas.")

    # CARREGAMENTO DA BASE
    @st.cache_data
    def carregar_base():
        # return pd.read_excel(r"C:\Users\Pedro\OneDrive\Área de Trabalho\TechChallenge\Fase 4\base_algoritmo.xlsx")
        return pd.read_excel(r"https://raw.githubusercontent.com/vbomura/TC4Final/main/arquivos/base_algoritmo.xlsx")

    base = carregar_base()

    # Dicionário de tradução geral
    traduzir_valores = {
        "yes": "Sim",
        "no": "Não",
        "male": "Masculino",
        "female": "Feminino",
        "Male": "Masculino",
        "Female": "Feminino",
        "Sometimes": "Às vezes",
        "Always": "Sempre",
        "Frequently": "Frequentemente",
        "no": "Não",
        "Yes": "Sim",
        "No": "Não",
        "Public_Transportation": "Transporte Público",
        "Automobile": "Automóvel",
        "Bike": "Bicicleta",
        "Motorbike": "Motocicleta",
        "Walking": "Caminhada",
        "Drinks sometimes": "Bebe às vezes",
        "Frequently": "Frequentemente",
        "Always": "Sempre",
        "no": "Não",
        "No": "Não",
        "Sometimes": "Às vezes",
        "Normal_Weight":"Peso Normal",
        "Overweight_Level_I": "Sobrepeso Nível 1",
        "Overweight_Level_II": "Sobrepeso Nível 2",
        "Obesity_Type_I": "Obesidade Nível 1",
        "Obesity_Type_II": "Obesidade Nível 2",
        "Obesity_Type_III": "Obesidade Nível 3",
        "Insufficient_Weight": "Peso Insuficiente"
    }

    # Aplicado a tradução apenas nas colunas de texto
    for col in base.select_dtypes(include="object").columns:
        base[col] = base[col].replace(traduzir_valores)

    # SEÇÃO DE FILTROS
    st.sidebar.header("Filtros")

    with st.sidebar.expander("Dados Demográficos", expanded=True):
        genero_sel = st.multiselect("Gênero", base["genero"].unique())
        idade_min, idade_max = st.slider(
            "Faixa de idade",
            min_value=int(base["idade"].min()),
            max_value=int(base["idade"].max()),
            value=(int(base["idade"].min()), int(base["idade"].max()))
        )

    with st.sidebar.expander("Condições de Saúde", expanded=True):
        nivel_sel = st.multiselect("Nível de Peso", base["nvl_obsidade"].unique())
        historico_familiar = st.multiselect("Histórico Familiar", base["historico_familiar"].unique())

    # Aplicação dos filtros
    df_filtrado = base.copy()

    # Filtros
    if genero_sel:
        df_filtrado = df_filtrado[df_filtrado["genero"].isin(genero_sel)]

    df_filtrado = df_filtrado[
        (df_filtrado["idade"] >= idade_min) &
        (df_filtrado["idade"] <= idade_max)
    ]

    if nivel_sel:
        df_filtrado = df_filtrado[df_filtrado["nvl_obsidade"].isin(nivel_sel)]

    if historico_familiar:
        df_filtrado = df_filtrado[df_filtrado["historico_familiar"].isin(historico_familiar)]  

    total_registros = base.shape[0]
    total_registros = f"{total_registros:,}".replace(",", ".")
    st.write(f"**Total de Registros Base:** {total_registros}")
    df_filtrado['nvl_obsidade'].value_counts()

    # VISÃO GERAL
    st.subheader("Visão Geral da Base")

    total_base = base.shape[0]
    filtrado = df_filtrado.shape[0]
    perc = (filtrado / total_base) * 100
    filtrado_fmt = f"{filtrado:,}".replace(",", ".")
    perc_fmt = f"{perc:.1f}%"
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros após filtros:", f"{df_filtrado.shape[0]:,}".replace(",", "."))
    col2.metric(
        "% Após o Filtro",
        f"{perc_fmt}"
    )

    st.dataframe(df_filtrado, use_container_width=True, height=420)  

    # GRÁFICOS EXPLORATÓRIOS
    st.subheader("Distribuições e Relações")

    tab1, = st.tabs(["Distribuição de Obesidade"])

    mapa = {
        "Peso Insuficiente": 1,
        "Peso Normal": 2,
        "Sobrepeso Nível 1": 3,
        "Sobrepeso Nível 2": 4,
        "Obesidade Nível 1": 5,
        "Obesidade Nível 2": 6,
        "Obesidade Nível 3": 7,
    }

    df_filtrado["classificacao"] = df_filtrado["nvl_obsidade"].map(mapa)

    # Gráfico 1 
    with tab1:
        fig1 = px.histogram(
            df_filtrado,
            x="nvl_obsidade",
            color="genero",
            barmode="group",
            title="Distribuição de Níveis de Obesidade por Gênero",
            color_discrete_sequence=["#F28482", "#A8DADC"] # azul claro e rosa claro
        )

        fig1.update_xaxes(
            categoryorder="array",
            categoryarray=[
                "Peso Insuficiente",
                "Peso Normal",
                "Sobrepeso Nível 1",
                "Sobrepeso Nível 2",
                "Obesidade Nível 1",
                "Obesidade Nível 2",
                "Obesidade Nível 3"
            ]
        )

        fig1.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            title_font=dict(size=18, family="Inter, sans-serif", color="#333"),
            legend_title_text="Gênero",
            font=dict(color="#333", size=12)
        )

        fig1.update_traces(
            texttemplate="%{y}", 
            textposition="outside"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # INDICADORES DE HÁBITOS E ESTILO DE VIDA
    st.subheader("Hábitos e Estilo de Vida")

    col1, col2, col3, col4 = st.columns(4)
    perc_fumantes = (df_filtrado[df_filtrado["fuma"] == "Sim"].shape[0] / df_filtrado.shape[0]) * 100
    perc_atividade = (df_filtrado[df_filtrado["frequencia_atividade"] > 2].shape[0] / df_filtrado.shape[0]) * 100
    perc_calorias = (df_filtrado[df_filtrado["calorias_frequente"] == "Sim"].shape[0] / df_filtrado.shape[0]) * 100
    calorias_frequente = df_filtrado[df_filtrado["calorias_frequente"] == "Sim"]
    perc_alcool = (df_filtrado[df_filtrado["frequencia_alcool"].isin(["Frequentemente", "Sempre"])].shape[0] / df_filtrado.shape[0]) * 100

    col1.metric("% Fumantes", f"{perc_fumantes:.1f}%")
    col2.metric("% Ativos Fisicamente", f"{perc_atividade:.1f}%")
    col3.metric("% Consumo Calórico Frequente", f"{perc_calorias:.1f}%")
    col4.metric("% Consumo de Álcool Frequente", f"{perc_alcool:.1f}%")

    # GRÁFICOS DE HÁBITOS
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

    tab2, tab3, tab4 = st.tabs(["Atividade Física", "Consumo Calórico", "Tempo de Tecnologia"])


    mapa = {
        "Peso Insuficiente": 1,
        "Peso Normal": 2,
        "Sobrepeso Nível 1": 3,
        "Sobrepeso Nível 2": 4,
        "Obesidade Nível 1": 5,
        "Obesidade Nível 2": 6,
        "Obesidade Nível 3": 7,
    }

    # Gráfico 2
    with tab2:
        fig4 = px.box(
            df_filtrado,
            x="nvl_obsidade",
            y="frequencia_atividade",
            color="nvl_obsidade",
            title="Atividade Física por Nível de Obesidade",
            labels={
                "frequencia_atividade": "Frequência de Atividade Física (vezes por semana)",
                "nvl_obsidade": "Nível de Obesidade"
            },
            color_discrete_sequence=[
                "#A8DADC",  
                "#F6BD60",  
                "#F28482",  
                "#84A59D",  
                "#C47F36",  
                "#B8C0FF",
                "#2F2F2F",
            ]
        ) 

    
        fig4.update_xaxes(
            categoryorder="array",
            categoryarray=[
                "Peso Insuficiente",
                "Peso Normal",
                "Sobrepeso Nível 1",
                "Sobrepeso Nível 2",
                "Obesidade Nível 1",
                "Obesidade Nível 2",
                "Obesidade Nível 3"
            ]
        )

        fig4.update_traces()

        st.plotly_chart(fig4, use_container_width=True)


    mapa = {
        "Peso Insuficiente": 1,
        "Peso Normal": 2,
        "Sobrepeso Nível 1": 3,
        "Sobrepeso Nível 2": 4,
        "Obesidade Nível 1": 5,
        "Obesidade Nível 2": 6,
        "Obesidade Nível 3": 7,
    }


    calorias_frequente["classificacao"] = calorias_frequente["nvl_obsidade"].map(mapa)

    # Gráfico 3
    with tab3:
        fig5 = px.histogram(
            calorias_frequente,
            x="nvl_obsidade",          
            color="calorias_frequente", 
            barmode="group",
            title="Consumo de Alimentos Calóricos x Nível de Obesidade",
            labels={"calorias_frequente": "Consome Alimentos Calóricos?"},
            color_discrete_sequence=[
                "#F6E58D",
                "#F28482",
            ]
        )

        fig5.update_xaxes(
            categoryorder="array",
            categoryarray=[
                "Peso Insuficiente",
                "Peso Normal",
                "Sobrepeso Nível 1",
                "Sobrepeso Nível 2",
                "Obesidade Nível 1",
                "Obesidade Nível 2",
                "Obesidade Nível 3"
            ]
        )

        fig5.update_traces(
            texttemplate="%{y}", 
            textposition="outside"
        )

        st.plotly_chart(fig5, use_container_width=True)


    mapa = {
        "Peso Insuficiente": 1,
        "Peso Normal": 2,
        "Sobrepeso Nível 1": 3,
        "Sobrepeso Nível 2": 4,
        "Obesidade Nível 1": 5,
        "Obesidade Nível 2": 6,
        "Obesidade Nível 3": 7,
    }

    # Gráfico 4
    with tab4:
        fig6 = px.box(
            df_filtrado,
            x="nvl_obsidade",
            y="tempo_tecnologia",
            color="nvl_obsidade",
            title="Tempo de Exposição à Tecnologia por Nível de Obesidade",
            labels={
                "tempo_tecnologia": "Horas por Dia",
                "nvl_obsidade": "Nível de Obesidade"
            },
            color_discrete_sequence=[
                "#A8DADC", 
                "#F6BD60", 
                "#F28482",  
                "#84A59D",  
                "#C47F36",  
                "#B8C0FF",  
                "#2F2F2F",  

            ]
        )

    
        fig6.update_xaxes(
            categoryorder="array",
            categoryarray=[
                "Peso Insuficiente",
                "Peso Normal",
                "Sobrepeso Nível 1",
                "Sobrepeso Nível 2",
                "Obesidade Nível 1",
                "Obesidade Nível 2",
                "Obesidade Nível 3"
            ]
        )

        fig6.update_traces(

        )

        st.plotly_chart(fig6, use_container_width=True)


