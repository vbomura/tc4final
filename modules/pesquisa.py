import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
from joblib import load
from tools.utils import RenomearColunasTransf, MultiLabelEncoder, YesNoToBinaryTransformer, MinMax, OrdinalEncodingTransformer, DummyEncoderTransformer, ColumnsToIntTransformer


def app():
    #importando base (alterar para caminho do GIT)
    base = pd.read_csv(r"https://raw.githubusercontent.com/vbomura/TC4Final/refs/heads/main/arquivos/Obesity.csv", sep=',')
    #exmplo:
    #dados = pd.read_csv('https://raw.githubusercontent.com/alura-tech/alura-tech-pos-data-science-credit-scoring-streamlit/main/df_clean.csv')

    st.set_page_config(page_title="Levantamento sobre dados de obesidade")
    st.title("Levantamento sobre dados de obesidade")

    st.write('# Pesquisa sobre obesidade')

    #Age
    input_idade = float(st.slider('Selecione sua idade:', 14, 61))

    #Weight
    input_peso = st.number_input(
        "Insira seu peso (em kg)",
        min_value=50,      # Altura mínima razoável
        max_value=300,     # Altura máxima razoável
        value=80,         # Valor padrão
        step=1            # Passo de 1 kg
    )

    #family_history
    input_historico = st.radio('Histórico familiar de excesso de peso?',["***Sim***","***Não***"])

    #CAEC
    input_lanches = st.selectbox('Consumo de lanches entre as refeições?', ("Selecione...", "Não consome", "Às vezes", "Frequentemente", "Sempre"))

    # ===========================================================
    # 🔘 Botão e tratamento dos dados
    # ===========================================================

    # Separando os dados em treino e teste
    def data_split(df):
        treino_df, teste_df = train_test_split(df, test_size=0.2, random_state=42)
        return treino_df.reset_index(drop=True), teste_df.reset_index(drop=True)    

    def pipeline_teste(df):

        pipeline = Pipeline([
            ('renomear', RenomearColunasTransf()),
            ('min_max_scaler',MinMax()),
            ('ordinal_feature', OrdinalEncodingTransformer()),
            ('label_encoding', MultiLabelEncoder(
                columns=[
                    'historico_familiar',
                    'calorias_frequente',
                    'fuma',
                    'genero',
                    'monitora_calorias'
                ]
            )),
            #('transformarBinario',YesNoToBinaryTransformer()), #ja esta tratado no MultiLabelEncoder
            ('onehot_transporte', DummyEncoderTransformer()),
            ('ajustandoColunasTransporte',ColumnsToIntTransformer()),
        # ... outros transformers ou modelos ...
        ])
        df_pipeline = pipeline.fit_transform(df)
        return df_pipeline

    map_obesidade = {
        0: "abaixo do peso",              # Insufficient_Weight
        1: "peso normal",                 # Normal_Weight
        2: "sobrepeso I",                 # Overweight_Level_I
        3: "sobrepeso II",                # Overweight_Level_II
        4: "obesidade I",                 # Obesity_Type_I
        5: "obesidade II",                # Obesity_Type_II
        6: "obesidade III"                # Obesity_Type_III
    }

    if st.button("Adicionar Pesquisa"):

        campos_invalidos = []

        # Verificar se todos foram preenchidos corretamente
        if input_lanches == "Selecione...":
            campos_invalidos.append("Lanches")

        # Se houver campos não preenchidos
        if campos_invalidos:
            st.error(f"⚠️ Por favor, preencha todos os campos obrigatórios: {', '.join(campos_invalidos)}")
        else:
            # Dicionários de conversão da tela de streamlit para poder adicionar o valor no dataframe
            map_binario = {"***Sim***": "yes", "***Não***": "no"}
            map_genero = {"***Masculino***": "Male", "***Feminino***": "Female"}
            map_vegetais = {"Raramente": 1, "Às vezes": 2, "Sempre": 3}
            map_lanches = {"Não consome": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
            map_agua = {"***< 1 L/dia***": 1, "***1–2 L/dia***": 2, "***2 L/dia***": 3}
            map_atividade = {"***Nenhuma***": 0, "***~1–2×/sem***": 1, "***~3–4×/sem***": 2, "***5×/sem ou mais***": 3}
            map_dispositivo = {"***~0–2 h/dia***": 0, "***~3–5 h/dia***": 1, "***> 5 h/dia***": 2}
            map_alcoolica = {"Não bebe": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
            map_transporte = {"Carro": "Automobile", "Moto": "Motorbike", "Bicicleta": "Bike", "Transporte Público": "Public_Transportation", "A pé": "Walking"}

            # Conversão dos campos
            historico_num = map_binario[input_historico]
            lanches_num = map_lanches[input_lanches]
            # Monta lista final tratada

            #Criando objeto de acordo com a planilha base
            nova_pesquisa = [
                "Male",# sexo_num,
                input_idade,
                0, #input_altura,
                input_peso,
                historico_num,
                "no",#calorico_num,
                1,#vegetais_num,
                1,#input_refeicoes,
                lanches_num,
                "no",#fuma_num,
                1,#agua_num,
                "no",#calorias_num,
                0,#atividade_num,
                0,#dispositivo_num,
                "no",#alcoolica_num,
                "Automobile",#transporte_num,
                0 #####TRATAR OBESIDADE#####
            ]
            
            treino_df, teste_df = data_split(base)

            #Criando novo paciente
            paciente_predict_df = pd.DataFrame([nova_pesquisa],columns=teste_df.columns)

            #Concatenando novo paciente ao dataframe dos dados de teste
            teste_novo_paciente  = pd.concat([teste_df,paciente_predict_df],ignore_index=True)

            #Aplicando a pipeline
            teste_novo_paciente = pipeline_teste(teste_novo_paciente)
            #teste_novo_paciente = teste_novo_paciente.loc[:, teste_novo_paciente.columns.difference(['historico_familiar_cod','calorias_frequente_cod','fuma_cod','genero','vegetais_refeicao', 'entre_refeicao','frequencia_alcool','nvl_obsidade','entre_refeicao_ord','frequencia_alcool_ord'])]

            #Deixando somente dados que são utilizados na predição
            cliente_pred = teste_novo_paciente[['peso','historico_familiar_cod', 'idade', 'calorias_frequente_cod', 'entre_refeicao_ord']]


            model = joblib.load('tools\RandomForest.joblib')
            final_pred = model.predict(cliente_pred)

            predicaoGerada=-1
            predicaoGerada = final_pred[-1].astype(int)

            # Mostra resultado
            #st.write("**Lista tratada:**", nova_pesquisa)
            st.write("**Resultado da predição:**", predicaoGerada)
            st.write("**Obesidade:**", map_obesidade[predicaoGerada])

            # Tratamento das mensagens
            if predicaoGerada == 0:
                st.warning("Você está abaixo do peso. É importante avaliar se existe alguma causa nutricional ou metabólica.")
                st.info("Busque auxílio nutricional para alcançar um peso saudável.")

            elif predicaoGerada == 1:
                st.success("Parabéns! Você está dentro do peso considerado saudável.")
                st.info("Continue mantendo bons hábitos alimentares e atividade física!")

            elif predicaoGerada == 2:
                st.warning("Atenção: você está em sobrepeso nível I.")
                st.info("Revisar alimentação e aumentar atividades físicas pode ajudar.")

            elif predicaoGerada == 3:
                st.warning("Atenção: você está em sobrepeso nível II.")
                st.info("Pode ser um bom momento para acompanhamento nutricional.")

            elif predicaoGerada == 4:
                st.error("Risco alto: obesidade nível I.")
                st.info("Procure orientação profissional para reduzir riscos à saúde.")

            elif predicaoGerada == 5:
                st.error("Risco muito alto: obesidade nível II.")
                st.warning("Mudanças de estilo de vida e acompanhamento médico são importantes.")

            elif predicaoGerada == 6:
                st.error("Risco crítico: obesidade nível III.")
                st.warning("Recomendado acompanhamento médico especializado.")

            else:
                st.error("Erro na criação da predição para estes valores, por favor realizar uma nova consulta.")
                
