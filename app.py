import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import seaborn as sns
import pandas as pd
import folium

from streamlit_folium import st_folium
from datetime import datetime

# Função para carregar os dados
def carrega_dados(file_path, delimitador):
    try:
        dados = pd.read_csv(file_path, delimiter = delimitador)
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()
    
# Extraindo o DDD e mapeando para o estado
def extract_ddd(phone_number):
    return str(phone_number)[:2]

# Lista com os nomes dos meses em português
meses_portugues = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# Carregar os dados
dados_estados = carrega_dados("dados/DDD-estado.csv", ",")
dados_leads = carrega_dados("dados/Leads.csv", ",")

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
nome_mes_mais_fechamentos = meses_portugues[mes_mais_fechamentos - 1]

ddd_estados_dict = dict(zip(dados_estados["DDD"], dados_estados["Estado"]))
leads_fechados["Estado"] = leads_fechados["DDD + Telefone:"].astype(str).str[:2].astype(int).map(ddd_estados_dict)
estado_mais_fechamentos = leads_fechados["Estado"].value_counts().idxmax()
quantidade_contratos_estado = leads_fechados["Estado"].value_counts().max()

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


# Dicionário para mapear DDDs por estados
ddd_to_estado = {str(row['DDD']): row['UF'] for _, row in dados_estados.iterrows()}

# Extraindo o DDD e mapeando para o estado
dados_leads['DDD'] = dados_leads['DDD + Telefone:'].apply(lambda x: extract_ddd(x))
dados_leads['Estado'] = dados_leads['DDD'].map(lambda x: ddd_to_estado.get(x, 'Desconhecido'))

# Filtrando dados de leads que fecharam e não fecharam contrato
dados_fechou = dados_leads[dados_leads['Status:'] == 'Fechou contrato']
dados_nao_fechou = dados_leads[dados_leads['Status:'] != 'Fechou contrato']

# Contando leads por estado
estado_fechou_counts = dados_fechou['Estado'].value_counts()
estado_nao_fechou_counts = dados_nao_fechou['Estado'].value_counts()

# Criando o mapa do Folium
mapa = folium.Map(location=[-14.235004, -51.92528], zoom_start=4)

# Iterando sobre os estados e adicionando marcadores ao mapa
for _, row in dados_estados.iterrows():
    estado_nome = row['UF']
    lat = row['Latitude']
    lon = row['Longitude']
    
    fechou = estado_fechou_counts.get(estado_nome, 0)
    nao_fechou = estado_nao_fechou_counts.get(estado_nome, 0)
    
     # Criando a descrição do marcador
    tooltip_html = f'''
        <div style='width: 300px; height: 80px;'>
            <h3 style='margin-bottom: 10px;'> {estado_nome} </h3>
            <p style='margin-top: -5px; font-size: 15px;'>Fecharam: {fechou}</p>
            <p style='margin-top: -15px; font-size: 15px;'>Não fecharam: {nao_fechou}</p>
        </div>
    '''   

    # Adicionando o marcador ao mapa
    folium.Marker(
        location=[lat, lon],
        # popup=popup_text,
        tooltip=tooltip_html,
        icon=folium.Icon(color='blue')
    ).add_to(mapa)


# Layout do Streamlit
st.set_page_config(layout="wide")
st.title("Dashboard Figueiredo correia (BPC-LOAS) autismo")

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
        <div style='background-color: #e0e0e0; padding: 20px; border-radius: 5px; border:1px solid;'>
            <h5 style='color: #000;'> <i class="fa-solid fa-sack-dollar" style="color: #000;"></i> Valor do Faturamento Total</h5>
            <p style='color:rgb(110 110 110); font-size: 40px; margin-top: -20px; font-weight:bold;'>R$ {valor_faturamento:,.2f} <i class="fa-solid fa-arrow-up" style=" color: rgb(18 150 18); font-size: 25px; margin-top: -10px; position: relative; top: -4px;;"></i></p>
            <div style="display: flex; gap: 8px; margin-top: -15px; align-items: center;">
                <p style='color: #000;'>Qtdº de Leads que Fecharam</p>
                <p style='color: #000;'><span style='font-weight: bold;'>{qtd_leads_fechados}</span> / {total_leads} ({porcentagem_fechados:.2f}%)</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #e0e0e0; padding: 20px; border-radius: 5px; border:1px solid;'>
            <h5 style='color: #000;'><i class="fa-solid fa-user-group"></i> Qtd de Leads Qualificados</h5>
            <p style='color: rgb(0 129 187); font-size: 40px; margin-top:-20px; font-weight:bold;'>{qtd_leads_qualificados} LEADS</p>
            <div style="display: flex; gap: 8px; margin-top: -15px; align-items: center;">
                <p style='color: #000;'>Porcentagem de Leads Qualificados</p>
                <p style='color: #000;'><span style='font-weight: bold;'>{porcentagem_qualificados:.2f}%</span> de {total_leads} leads</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: #e0e0e0; padding: 20px; padding-bottom: 6px; border-radius: 5px; border:1px solid;'>
            <h5 style='color: #000;'><i class="fa-solid fa-calendar-check"></i> Mês com Mais Fechamentos</h5>
            <p style='color: rgb(0 129 187); font-size: 30px; margin-top: -20px; font-weight:bold;'>{nome_mes_mais_fechamentos} de {datetime.now().year}</p>
            <p style='color: #000; margin-top: -10px;'>Estado com Mais Fechamentos</p>
            <p style='color: #000; margin-top: -16px;'><span style='font-weight: bold;'>{estado_mais_fechamentos} - {quantidade_contratos_estado} contratos</span></p>
        </div>
        """, unsafe_allow_html=True
    )

# Colunas para os três gráficos
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='margin-top: 1.5rem;'>Análise de Leads por Estado</h3>", unsafe_allow_html=True)

    # Filtros
    option = st.selectbox(
        "Selecione o tipo de leads para mostrar:",
        ("Ambos", "Fechou contrato", "Não fechou contrato")
    )

    # Preparando os dados para o gráfico empilhado
    estado_counts = dados_leads['Estado'].value_counts()
    if option == "Fechou contrato":
        estado_counts = estado_fechou_counts
    elif option == "Não fechou contrato":
        estado_counts = estado_nao_fechou_counts
    estados = estado_counts.index
    fechou_values = estado_fechou_counts.reindex(estados, fill_value=0)
    nao_fechou_values = estado_nao_fechou_counts.reindex(estados, fill_value=0)

    # Gráfico de barras para leads por estado com Plotly
    if option == "Ambos":
        fig_estado = go.Figure(data=[
            go.Bar(name='Fechou contrato', x=estados, y=fechou_values, marker_color='green', hovertemplate='Estado: %{x}<br>Fechou: %{y}'),
            go.Bar(name='Não fechou contrato', x=estados, y=nao_fechou_values, marker_color='red', base=fechou_values, hovertemplate='Estado: %{x}<br>Não fechou: %{y}')
        ])
    elif option == "Fechou contrato":
        fig_estado = go.Figure(data=[
            go.Bar(name='Fechou contrato', x=estados, y=fechou_values, marker_color='green', hovertemplate='Estado: %{x}<br>Fechou: %{y}')
        ])
    elif option == "Não fechou contrato":
        fig_estado = go.Figure(data=[
            go.Bar(name='Não fechou contrato', x=estados, y=nao_fechou_values, marker_color='red', hovertemplate='Estado: %{x}<br>Não fechou: %{y}')
        ])

    fig_estado.update_layout(
        barmode='stack',
        title='',
        xaxis_title='Estados',
        yaxis_title='Quantidade de Leads',
        template='plotly_dark'
    )

    st.plotly_chart(fig_estado, use_container_width=True)
with col2:
    st.markdown("<h3 style='margin-top: 1.5rem;'>Porque não fecharam?</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)

with col3:
    st.markdown("<h3 style='margin-top: 1.5rem;'>Distribuição Percentual de Contatos</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)


# Adicionando o mapa do Folium ocupando toda a largura abaixo dos outros gráficos
st.title("Distribuição dos Leads no Mapa do Brasil")
st_folium(mapa, width=None, height=600)