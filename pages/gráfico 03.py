import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
dados = pd.read_csv('Planilha - Projeto BigData Python.csv')




#####
##### GRAFICO 1
#####

contagem_nao_fechou = dados['Por que não fechou?'].value_counts()

# Visualização de dados
st.title('Análise de Leads BPC LOAS para Autismo')
# Gráfico de barras horizontais para contagem de motivos de não fechamento
st.subheader('Motivos de Não Fechamento')
fig, ax = plt.subplots()
sns.barplot(x=contagem_nao_fechou.values, y=contagem_nao_fechou.index, orient='horizontal', ax=ax)
st.pyplot(fig)



