# 📊 Tech Challenge – Fase 4  
## Dashboard e Previsão de Obesidade com Machine Learning

Este projeto foi desenvolvido como parte do **Tech Challenge da FIAP – Fase 4**, com foco em criar uma aplicação completa de **Machine Learning**, incluindo análise exploratória, pré-processamento, construção de modelos e interface interativa com **Streamlit**.

A aplicação está publicada online e acessível aqui:

👉 **https://tc4final-9oedbhdg7nvpzhwtmtrnyr.streamlit.app/**

---

# 🚀 Objetivo do Projeto

O objetivo principal deste trabalho é:

- Realizar análises gráficas e estatísticas sobre fatores relacionados à **obesidade**
- Construir modelos de **Machine Learning** que podem identificar padrões
- Criar uma interface interativa em **Streamlit** para facilitar o uso por qualquer usuário

O projeto engloba desde a preparação dos dados até a disponibilização online da solução.

---

# 🖥️ Funcionalidades da Aplicação

A interface web possui:

### ✔ **Pesquisa de Obesidade**
- Coleta de informações do usuário  
- Interface simples e intuitiva  

### ✔ **Dashboard de Análises**
- Gráficos interativos  
- Distribuições e correlações  
- Análises técnicas  

### ✔ **Sobre o Projeto**
- Informações gerais  
- Explicações sobre o modelo e a solução  

---

# 🧠 Machine Learning

O projeto inclui:

- Pré-processamento de dados
- Tratamento de variáveis categóricas e numéricas
- Transformações e normalizações
- Aplicação de modelos:

### Modelos testados:
- **Regressão Logística**  
- **Random Forest**  
- **XGBoost** (se aplicável)  

### Métricas avaliadas:
- Acurácia  
- Precision  
- Recall  
- Matriz de confusão  


### Modelo escolhido foi: **Random Forest**  
---

# 📁 Estrutura do Projeto

```bash
tc4final/
│── assets/                     # Imagens e arquivos auxiliares
│   └── grafico.png
│
│── tools/                      # Arquivos para Pipeline e modelos salvos
│   ├── RandomForest.joblib
│   └── utils.py
│
│── modules/                    # Lógica das páginas do Streamlit
│   ├── dashboard.py
│   ├── imagem.py
│   ├── pesquisa.py
│   └── sobre.py
│
│── main.py                     # Arquivo principal da aplicação Streamlit
│── requirements.txt            # Dependências do projeto
│── README.md                   # Documentação do repositório
```

# 📦 Requisitos

As principais dependências estão no arquivo requirements.txt.


# 👨‍💻 Autores
Bryan
Gustavo
Luiz
Pedro
Vitor Bomura(https://github.com/vbomura)
