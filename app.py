import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import folium

from streamlit_folium import st_folium

#@st.cache_data
def carrega_dados(file_path):
    try:
        dados = pd.read_csv(file_path)
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()





dados_estados = carrega_dados("dados/DDD-estado.csv")
dados_leads = carrega_dados("dados/Leads.csv")







# Dados fictícios para o exemplo
categorias = ['A', 'B', 'C', 'D']
valores = [10, 15, 7, 25]
porcentagens = [10, 15, 35, 40]

# Gráfico de área (exemplo)
x = np.arange(10)
y = np.random.randn(10).cumsum()

fig_area = go.Figure(data=go.Scatter(x=x, y=y, fill='tozeroy'))
fig_area.update_layout(title='Gráfico de Área', template='plotly_dark')

# Gráfico de barra horizontal
# fig_bar = go.Figure(data=[go.Bar(y=categorias, x=valores, orientation='h')])
# fig_bar.update_layout(title='Gráfico de Barra Horizontal', xaxis_title='Valores', yaxis_title='Categorias', template='plotly_dark')






# Gráfico de barra horizontal
contagem_nao_fechou = dados_leads['Por que não fechou?'].value_counts()

fig_bar = go.Figure(data=[go.Bar(
    y=contagem_nao_fechou.index,
    x=contagem_nao_fechou.values,
    orientation='h',
    hovertemplate='<b>%{y}</b><br>Quantidade de Leads: %{x}<extra></extra>'
)])

fig_bar.update_layout(
    title='',
    xaxis_title='Valores',
    yaxis_title='',
    template='plotly_dark'
)

# Gráfico de pizza
contato_counts = dados_leads['Contato:'].value_counts()
percentages = 100 * contato_counts / contato_counts.sum()
labels = [f'{name} ({percentage:.1f}%)' for name, percentage in zip(contato_counts.index, percentages)]

fig_pie = px.pie(values=contato_counts.values, names=labels, title='', template='plotly_dark')
fig_pie.update_traces(
    marker=dict(line=dict(color='#000000', width=1)),
    textposition='inside',
    textinfo='percent',
    hovertemplate='<b>%{label}</b> <br> <b>Total Leads: %{value}</b>'
)




# Criar o mapa do Folium
m = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)  # Localização fictícia (São Paulo, Brasil)

# Adicionar um marcador
folium.Marker([-23.5505, -46.6333], popup="São Paulo").add_to(m)

# Layout do Streamlit
st.set_page_config(layout="wide")

st.title("Dashboard com Plotly e Streamlit")

# Colunas para os três gráficos
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_area, use_container_width=True)

with col2:
    st.plotly_chart(fig_bar, use_container_width=True)

with col3:
    st.plotly_chart(fig_pie, use_container_width=True)

# Adicionando o mapa do Folium ocupando toda a largura abaixo dos outros gráficos
st_folium(m, width=None, height=600)