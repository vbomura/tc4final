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

    # GRÁFICOS DE HÁBITOS
    st.subheader("Relações entre Hábitos e Obesidade")

    st.markdown("""
    Os hábitos diários exercem influência direta no risco de obesidade.  
    A seguir, avaliamos três comportamentos principais:

    1. **Atividade física**
    2. **Consumo de alimentos calóricos**
    3. **Tempo de exposição à tecnologia**

    Essas análises ajudam a entender os padrões comportamentais que contribuem para diferentes níveis de obesidade, como por exemplo, a falta de atividade física + o alto consumo calórico, 
    aceleram as chances da pessoa ter obesidade.
                
    """)

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
    df_filtrado['nvl_obsidade'].value_counts()

    df_filtrado.rename(columns={'nvl_obsidade':'nivel_peso'}, inplace=True)
    # VISÃO GERAL
    st.subheader("Visão Geral da Base")

    st.write(f"**Total de Registros Base:** {total_registros}")

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

    st.subheader("Relações entre Hábitos e Obesidade")

    st.markdown("""
        A obesidade afeta homens e mulheres de maneiras distintas?

        Ao segmentarmos nossa base de dados por gênero, padrões interessantes emergem.
        
        O gráfico a seguir mostra que as mulheres se concentram nos níveis de peso mais baixos, 
            enquanto os homens representam a maior parte dos casos de sobrepeso e obesidade intermediária.
            No nível de Obesidade Grau 2, o público masculino apresenta os maiores valores. 
                
        Já no nível mais elevado, Obesidade Grau 3, o destaque passa a ser feminino.
            Essas diferenças reforçam que cada gênero segue um padrão distinto de evolução de peso, o que pode direcionar ações de saúde mais específicas.
                
    """)    

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

    df_filtrado["classificacao"] = df_filtrado["nivel_peso"].map(mapa)

    # Gráfico 1 
    with tab1:
        fig1 = px.histogram(
            df_filtrado,
            x="nivel_peso",
            color="genero",
            barmode="group",
            title="Distribuição de Níveis de Obesidade por Gênero",
            color_discrete_sequence=["#F28482", "#A8DADC"] # azul claro e rosa claro
        )

        fig1.update_yaxes(title_text="Quantidade")
        fig1.update_xaxes(title_text="Nível de Peso")

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

        st.markdown("""
            **Existe uma relação direta entre a frequência de exercícios e o nível de peso?**
            
            O gráfico de caixa **(boxplot)** abaixo nos ajuda a responder essa pergunta:
                    
            Indivíduos com peso normal praticam exercícios apenas algumas vezes por semana, e nos níveis mais altos de obesidade essa frequência se mantém semelhante.
            
            Isso indica que a baixa prática de atividade física é um comportamento geral da população analisada, independentemente do peso.
                                           
            """)


        fig4 = px.box(
            df_filtrado,
            x="nivel_peso",
            y="frequencia_atividade",
            color="nivel_peso",
            title="Atividade Física por Nível de Peso",
            labels={
                "frequencia_atividade": "Frequência de Atividade Física (vezes por semana)",
                "nivel_peso": "Nível de Peso"
            },
            color_discrete_sequence=[
                "#A8DADC",  
                "#F6BD60",  
                "#F28482",  
                "#84A59D",  
                "#C47F36",  
                "#B8C0FF",
                "#1E90FF"            
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


    calorias_frequente["classificacao"] = calorias_frequente["nivel_peso"].map(mapa)

    # Gráfico 3
    with tab3:

        st.markdown("""
            
            **Existe um padrão claro de alimentação entre os diferentes níveis de peso?** 
                    
            Nesta visualização, isolamos os participantes que consomem alimentos de alto teor calórico para entender como esse grupo se distribui.

            O **gráfico** mostra que o consumo de alimentos calóricos está presente em todos os níveis de peso, porém ganha intensidade à medida que a obesidade avança.

            A partir do Sobrepeso Nível 1, o volume cresce de forma consistente e atinge seus maiores valores nos graus mais altos de obesidade.

            Isso sugere que esse padrão alimentar pode contribuir para a progressão do ganho de peso, reforçando seu papel como fator de risco comportamental.
    
            """)

        fig5 = px.histogram(
            calorias_frequente,
            x="nivel_peso",          
            color="calorias_frequente", 
            barmode="group",
            title="Consumo de Alimentos Calóricos x Nível de Peso",
            labels={"calorias_frequente": "Consome Alimentos Calóricos?"},
            color_discrete_sequence=[
                "#F6E58D",
                "#F28482",
            ]
        )

        fig5.update_yaxes(title_text="Calorias")
        fig5.update_xaxes(title_text="Nível de Peso")
        
        fig5.update_yaxes(range=[0, 380])

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

        st.markdown("""
            **O uso excessivo de dispositivos tecnológicos está associado ao ganho de peso?**
            
            O gráfico abaixo investiga essa relação, mostrando a distribuição de **horas diárias** gastas com tecnologia (celulares, computadores, etc.) para cada nível de obesidade.

            A visualização abaixo mostra que o tempo de exposição à tecnologia é semelhante entre todos os níveis de peso, variando geralmente entre 1 e 2 horas por dia.
                
            Não há diferenças significativas entre os grupos, indicando que esse hábito é comum na população e não muda conforme o peso.
        
            """)
                
        fig6 = px.box(
            df_filtrado,
            x="nivel_peso",
            y="tempo_tecnologia",
            color="nivel_peso",
            title="Tempo de Exposição à Tecnologia por Nível de Peso",
            labels={
                "tempo_tecnologia": "Horas por Dia",
                "nivel_peso": "Nível de Peso"
            },
            color_discrete_sequence=[
                "#A8DADC", 
                "#F6BD60", 
                "#F28482",  
                "#84A59D",  
                "#C47F36",  
                "#B8C0FF",  
                "#1E90FF"

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


