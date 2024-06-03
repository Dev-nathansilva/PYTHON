import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Planilha - Projeto BigData Python.csv')

# Gráfico de barras para contagem de leads por status usando Seaborn
st.write("Contagem de Leads por Status")
plt.figure(figsize=(10, 6))  # Definindo o tamanho da figura
sns.countplot(data=df, x='Status:')  # Criando o gráfico de barras usando Seaborn
plt.xticks(rotation=45)  # Rotacionando os rótulos no eixo x para melhor visualização
fig = plt.gcf()  # Obtendo a figura atual
st.pyplot(fig)  # Passando a figura como argumento para st.pyplot()



# Contagem de Leads por Qualificação
st.write("Contagem de Leads por Qualificação")
qualificacao_counts = df['Qualificação'].value_counts()
st.bar_chart(qualificacao_counts)

# Gráfico de barras para razões de não fechamento de contrato
st.write("Razões para não fechamento de contrato")
nao_fechou_counts = df['Por que não fechou?'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=nao_fechou_counts.index, y=nao_fechou_counts.values, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)


# Gráfico de pizza para método de contato
st.write("Método de Contato")
contato_counts = df['Contato:'].value_counts()
fig, ax = plt.subplots()
ax.pie(contato_counts, labels=contato_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)