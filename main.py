import streamlit as st
#from streamlit_option_menu import option_menu # Você pode instalar essa biblioteca para personalizar ainda mais
import importlib
from modules import pesquisa, sobre, obesity_dashboard, imagem, principal # Importe as páginas criadas na pasta 'pages'

st.sidebar.title("Menu")

# MAPEAMENTO PERSONALIZADO
paginas = {
    "🏠 Página Inicial": "modules.principal",
    "📝 Questionário": "modules.pesquisa",
    "📊 Dashboard": "modules.obesity_dashboard",    
    "ℹ️ Predição": "modules.imagem"
}

# SELECTBOX MOSTRA APENAS NOMES BONITOS
escolha = st.sidebar.selectbox("", list(paginas.keys()))

# IMPORTA O ARQUIVO CORRESPONDENTE
modulo = importlib.import_module(paginas[escolha])

# CADA ARQUIVO EM pages/ PRECISA TER UMA FUNÇÃO app()
modulo.app()


