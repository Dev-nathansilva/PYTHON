import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import datetime
import calendar
import locale

# Configurando o ambiente para português
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Função para carregar os dados
def carrega_dados(file_path):
    try:
        dados = pd.read_csv(file_path)
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# Carregar os dados
dados_estados = carrega_dados("dados/DDD-estado.csv")
dados_leads = carrega_dados("dados/Leads.csv")

# Calcular o valor do faturamento e a quantidade de leads que fecharam
valor_contrato = 7000
leads_fechados = dados_leads[dados_leads['Status:'] == 'Fechou contrato']
qtd_leads_fechados = len(leads_fechados)
valor_faturamento = qtd_leads_fechados * valor_contrato
total_leads = len(dados_leads)
porcentagem_fechados = (qtd_leads_fechados / total_leads) * 100 if total_leads > 0 else 0

# Calcular a quantidade de leads qualificados
leads_qualificados = dados_leads[dados_leads['Qualificação'] == 'Lead Qualificado']
qtd_leads_qualificados = len(leads_qualificados)
porcentagem_qualificados = (qtd_leads_qualificados / total_leads) * 100 if total_leads > 0 else 0

# Calcular o mês com mais fechamentos de contrato
leads_fechados['Data'] = pd.to_datetime(leads_fechados['Data'])
leads_fechados['Mês'] = leads_fechados['Data'].dt.month
mes_mais_fechamentos = leads_fechados['Mês'].value_counts().idxmax()

# Calcular o estado com mais fechamentos de contrato
ddd_estados = pd.read_csv("dados/DDD-estado.csv", delimiter=";")
ddd_estados_dict = dict(zip(ddd_estados["DDD"], ddd_estados["Estado"]))
leads_fechados["Estado"] = leads_fechados["DDD + Telefone:"].astype(str).str[:2].astype(int).map(ddd_estados_dict)
estado_mais_fechamentos = leads_fechados["Estado"].value_counts().idxmax()
quantidade_contratos_estado = leads_fechados["Estado"].value_counts().max()

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
# Adicionando o link para o Font Awesome no cabeçalho HTML
st.markdown(
    """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Colunas para os três blocos de texto
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: gray; padding: 20px; border-radius: 5px;'>
            <h5 style='color: white;'> <i class="fa-solid fa-sack-dollar" style="color: #FFD43B;"></i> Valor do Faturamento Total</h5>
            <p style='color: rgb(241 241 241); font-size: 40px; margin-top: -20px; font-weight:bold;'>R$ {valor_faturamento:,.2f} <i class="fa-solid fa-arrow-up" style=" color: rgb(9 227 9); font-size: 25px; margin-top: -10px; position: relative; top: -4px;;"></i></p>
            <div style="display: flex; gap: 8px; margin-top: -15px; align-items: center;">
                <p style='color: white;'>Qtdº de Leads que Fecharam</p>
                <p style='color: white;'><span style='font-weight: bold;'>{qtd_leads_fechados}</span> / {total_leads} ({porcentagem_fechados:.2f}%)</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: gray; padding: 20px; border-radius: 5px;'>
            <h5 style='color: white;'><i class="fa-solid fa-user-group"></i> Qtd de Leads Qualificados</h5>
            <p style='color: rgb(75 199 255); font-size: 40px; margin-top:-20px; font-weight:bold;'>{qtd_leads_qualificados} LEADS</p>
            <div style="display: flex; gap: 8px; margin-top: -15px; align-items: center;">
                <p style='color: white;'>Porcentagem de Leads Qualificados</p>
                <p style='color: white;'><span style='font-weight: bold;'>{porcentagem_qualificados:.2f}%</span> de {total_leads} leads</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: gray; padding: 20px; padding-bottom: 6px; border-radius: 5px;'>
            <h5 style='color: white;'><i class="fa-solid fa-calendar-check"></i> Mês com Mais Fechamentos</h5>
            <p style='color: rgb(75 199 255); font-size: 30px; margin-top: -20px; font-weight:bold;'>{calendar.month_name[mes_mais_fechamentos].capitalize()} de {datetime.now().year}</p>
            <p style='color: white; margin-top: -10px;'>Estado com Mais Fechamentos</p>
            <p style='color: white; margin-top: -16px;'><span style='font-weight: bold;'>{estado_mais_fechamentos} - {quantidade_contratos_estado} contratos</span></p>
        </div>
        """, unsafe_allow_html=True
    )

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
