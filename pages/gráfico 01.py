import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados
df = pd.read_csv('Planilha - Projeto BigData Python.csv')

# Função para extrair o DDD do telefone
def extract_ddd(phone_number):
    return str(phone_number)[:2]

# Dicionário para mapear DDDs para estados
ddd_to_state = {
    '11': 'SP', '12': 'SP', '13': 'SP', '14': 'SP', '15': 'SP', '16': 'SP', '17': 'SP', '18': 'SP', '19': 'SP',
    '21': 'RJ', '22': 'RJ', '24': 'RJ',
    '27': 'ES', '28': 'ES',
    '31': 'MG', '32': 'MG', '33': 'MG', '34': 'MG', '35': 'MG', '37': 'MG', '38': 'MG',
    '41': 'PR', '42': 'PR', '43': 'PR', '44': 'PR', '45': 'PR', '46': 'PR',
    '47': 'SC', '48': 'SC', '49': 'SC',
    '51': 'RS', '53': 'RS', '54': 'RS', '55': 'RS',
    '61': 'DF',
    '62': 'GO', '64': 'GO',
    '63': 'TO',
    '65': 'MT', '66': 'MT',
    '67': 'MS',
    '68': 'AC',
    '69': 'RO',
    '71': 'BA', '73': 'BA', '74': 'BA', '75': 'BA', '77': 'BA',
    '79': 'SE',
    '81': 'PE', '87': 'PE',
    '82': 'AL',
    '83': 'PB',
    '84': 'RN',
    '85': 'CE', '88': 'CE',
    '86': 'PI', '89': 'PI',
    '91': 'PA', '93': 'PA', '94': 'PA',
    '92': 'AM', '97': 'AM',
    '95': 'RR',
    '96': 'AP',
    '98': 'MA', '99': 'MA'
}

# Extraindo o DDD e mapeando para o estado
df['DDD'] = df['DDD + Telefone:'].apply(lambda x: extract_ddd(x))
df['Estado'] = df['DDD'].map(ddd_to_state)

# Filtrando dados de leads que fecharam e não fecharam contrato
df_fechou = df[df['Status:'] == 'Fechou contrato']
df_nao_fechou = df[df['Status:'] != 'Fechou contrato']

# Contando leads por estado
estado_counts = df['Estado'].value_counts()
estado_fechou_counts = df_fechou['Estado'].value_counts()
estado_nao_fechou_counts = df_nao_fechou['Estado'].value_counts()

# Configurando a interface do Streamlit
st.title("Análise de Leads por Estado")

# Filtros
option = st.selectbox(
    "Selecione o tipo de leads para mostrar:",
    ("Ambos", "Fechou contrato", "Não fechou contrato")
)

# Preparando os dados para o gráfico empilhado
estados = estado_counts.index
fechou_values = estado_fechou_counts.reindex(estados, fill_value=0)
nao_fechou_values = estado_nao_fechou_counts.reindex(estados, fill_value=0)

# Gráfico de barras para leads por estado
fig, ax = plt.subplots()

if option == "Ambos":
    ax.bar(estados, fechou_values, label='Fechou contrato', color='green')
    ax.bar(estados, nao_fechou_values, bottom=fechou_values, label='Não fechou contrato', color='red')
elif option == "Fechou contrato":
    sns.barplot(x=estado_fechou_counts.index, y=estado_fechou_counts.values, ax=ax, color='green', label='Fechou contrato')
elif option == "Não fechou contrato":
    sns.barplot(x=estado_nao_fechou_counts.index, y=estado_nao_fechou_counts.values, ax=ax, color='red', label='Não fechou contrato')

plt.xticks(rotation=90)
plt.legend()
st.pyplot(fig)
