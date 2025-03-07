# ==================================================
# Bibliotecas Necessárias
# ==================================================
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

#-------------------------------------Início das Funções-----------------------------------

# ==================================================
# Funções
# ==================================================
def definicao_parametros_graficos():
    
    # Configurações gerais
    sns.set_theme()

    plt.rcParams['figure.figsize']=(6, 3) # Define o tamanho das figuras
    plt.rcParams['axes.titlesize']=10     # Define o tamanho do título das figuras
    plt.rcParams['axes.labelsize']=8      # Define o tamanho do rótulos dos eixos
    plt.rcParams['xtick.labelsize']=7     # Define o tamanho dos ticks dos eixos x
    plt.rcParams['ytick.labelsize']=7     # Define o tamanho dos ticks dos eixos y 
    plt.rcParams['legend.fontsize']=8     # Define o tamanho da legenda
    plt.rcParams['lines.markersize']=4    # Define o tamanho dos marcadores nas linhas
    
    # Configura o cabeçalho da página
    st.set_page_config(page_title='Análise de Vendas por Estado', page_icon='🌐', layout='wide')

    return None

def filtra_df(df):    # Side Bar
    st.sidebar.header('🔍 Filtros Avançados')
    
    st.sidebar.subheader(" Ajuste os filtros para personalizar sua análise!")

    lista_estados=sorted(list(df['seller_state'].unique()))

    estado_selecionado=st.sidebar.multiselect('Selecione o Estado',
                                                options=lista_estados,
                                                default=lista_estados)

    customers_df=df[df['customer_state'].isin(estado_selecionado)] 
    sellers_df=df[df['seller_state'].isin(estado_selecionado)] 
    
    # Filtro por Data
    min_date = pd.to_datetime('2017-01-01')  # Data mínima no dataset
    max_date = pd.to_datetime('2018-12-31')  # Data máxima no dataset
    date_range = st.sidebar.date_input("📅 Período de Pedido", [min_date, max_date])

    # Filtro por Status do Pedido
    status_list = ['delivered', 'shipped', 'canceled', 'processing', 'invoiced']
    selected_status = st.sidebar.multiselect("📦 Status do Pedido", status_list, default=['delivered'])

    # Filtro por Região
    regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    selected_region = st.sidebar.selectbox("🌍 Selecione a Região", regions)

    # Filtro por Faixa de Preço
    price_range = st.sidebar.slider("💰 Faixa de Preço (R$)", 0, 5000, (50, 1000))

    # Filtro por Número de Itens
    items_range = st.sidebar.slider("📊 Número de Itens por Pedido", 1, 10, (1, 5))
           
    return customers_df, sellers_df

def big_numbers(c_df, s_df):
    # Big Number
    st.subheader('📊 Indicadores Gerais')

    total_vendas = c_df['total_price'].sum()
    total_customers = c_df['customer_unique_id'].nunique()
    total_sellers = s_df['seller_id'].nunique()
    total_pedidos = c_df.shape[0]
    ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0
    faturamento_medio_seller = total_vendas / total_sellers if total_sellers > 0 else 0

    # Criando Colunas
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    col1.metric('📦 Número de Pedidos', f'{total_pedidos:,}')
    col2.metric('👥 Clientes Únicos', f'{total_customers:,}')
    col3.metric('🏪 Vendedores Únicos', f'{total_sellers:,}')
    
    col4.metric('💰 Vendas Totais', f'R${total_vendas:,.2f}')
    col5.metric('📈 Ticket Médio', f'R${ticket_medio:,.2f}')

    # Identificando Top Vendedor
    if 'total_price' in s_df.columns:
        top_seller = s_df.groupby('seller_id')['total_price'].sum().idxmax()
        top_seller_faturamento = s_df.groupby('seller_id')['total_price'].sum().max()
        st.metric('🏆 Top Vendedor', f'{top_seller}', f'R${top_seller_faturamento:,.2f}')

    return None

def visoes_gerais(c_df, s_df):
    #Visão Geral
    st.subheader('📍 Visão Geral das Vendas por Estado')
 
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
 
    #Vendas Totais por Estado
    vendas_estados = c_df.groupby('customer_state')['total_price'].sum().reset_index()
    vendas_estados = vendas_estados.sort_values(by='total_price', ascending=False)  # Ordenação
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=vendas_estados, x='customer_state', y='total_price', ax=ax1, palette='viridis')
    ax1.set_title('💰 Vendas Totais por Estado')
    ax1.set_xlabel('Estado')
    ax1.set_ylabel('Vendas (R$)')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)  # Rotacionar labels do eixo X
    col1.pyplot(fig1)

    # Quantidade de Clientes Únicos por Estado
    clientes_estados = c_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
    clientes_estados = clientes_estados.sort_values(by='customer_unique_id', ascending=False)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=clientes_estados, x='customer_state', y='customer_unique_id', ax=ax2, palette='coolwarm')
    ax2.set_title('👥 Clientes Únicos por Estado')
    ax2.set_xlabel('Estado')
    ax2.set_ylabel('Clientes Únicos')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    col2.pyplot(fig2)

    # Quantidade de Vendedores Únicos por Estado
    vendedores_estados = s_df.groupby('seller_state')['seller_id'].nunique().reset_index()
    vendedores_estados = vendedores_estados.sort_values(by='seller_id', ascending=False)
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=vendedores_estados, x='seller_state', y='seller_id', ax=ax3, palette='magma')
    ax3.set_title('🏪 Vendedores Únicos por Estado')
    ax3.set_xlabel('Estado')
    ax3.set_ylabel('Vendedores Únicos')
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
    col3.pyplot(fig3)

    # Ticket Médio por Estado (Vendas Totais / Clientes Únicos)
    ticket_medio_estados = vendas_estados.merge(clientes_estados, on='customer_state')
    ticket_medio_estados['ticket_medio'] = ticket_medio_estados['total_price'] / ticket_medio_estados['customer_unique_id']
    ticket_medio_estados = ticket_medio_estados.sort_values(by='ticket_medio', ascending=False)

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=ticket_medio_estados, x='customer_state', y='ticket_medio', ax=ax4, palette='plasma')
    ax4.set_title('📈 Ticket Médio por Estado')
    ax4.set_xlabel('Estado')
    ax4.set_ylabel('Ticket Médio (R$)')
    ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45)
    col4.pyplot(fig4)

    return None

def visoes_temporais(c_df, s_df):
    st.subheader('📅 Visões Temporais (Mês)')

    # Converter para datetime para ordenação correta
    c_df['order_purchase_year_month'] = pd.to_datetime(c_df['order_purchase_year_month'], format='%Y-%m')
    s_df['order_purchase_year_month'] = pd.to_datetime(s_df['order_purchase_year_month'], format='%Y-%m')

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 📊 Vendas Totais por Mês
    vendas_temporal = c_df.groupby('order_purchase_year_month')['total_price'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=vendas_temporal, x='order_purchase_year_month', y='total_price', ax=ax1, marker='o', color='blue', label='Vendas')
    ax1.set_title('💰 Vendas Totais por Mês')
    ax1.set_xlabel('Ano - Mês')
    ax1.set_ylabel('Vendas (R$)')
    ax1.tick_params(axis='x', rotation=45)
    col1.pyplot(fig1)

    # 📈 Clientes Únicos por Mês
    clientes_temporal = c_df.groupby('order_purchase_year_month')['customer_unique_id'].nunique().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=clientes_temporal, x='order_purchase_year_month', y='customer_unique_id', ax=ax2, marker='o', color='green', label='Clientes Únicos')
    ax2.set_title('👥 Clientes Únicos por Mês')
    ax2.set_xlabel('Ano - Mês')
    ax2.set_ylabel('Clientes Únicos')
    ax2.tick_params(axis='x', rotation=45)
    col2.pyplot(fig2)

    # 🏪 Vendedores Únicos por Mês
    vendedores_temporal = s_df.groupby('order_purchase_year_month')['seller_id'].nunique().reset_index()
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=vendedores_temporal, x='order_purchase_year_month', y='seller_id', ax=ax3, marker='o', color='red', label='Vendedores Únicos')
    ax3.set_title('🏪 Vendedores Únicos por Mês')
    ax3.set_xlabel('Ano - Mês')
    ax3.set_ylabel('Vendedores Únicos')
    ax3.tick_params(axis='x', rotation=45)
    col3.pyplot(fig3)

    # 📊 Ticket Médio por Mês (Vendas Totais / Clientes Únicos)
    ticket_medio_temporal = vendas_temporal.merge(clientes_temporal, on='order_purchase_year_month')
    ticket_medio_temporal['ticket_medio'] = ticket_medio_temporal['total_price'] / ticket_medio_temporal['customer_unique_id']
    
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=ticket_medio_temporal, x='order_purchase_year_month', y='ticket_medio', ax=ax4, marker='o', color='purple', label='Ticket Médio')
    ax4.set_title('📈 Ticket Médio por Mês')
    ax4.set_xlabel('Ano - Mês')
    ax4.set_ylabel('Ticket Médio (R$)')
    ax4.tick_params(axis='x', rotation=45)
    col4.pyplot(fig4)

    return None

#-----------------------------Início da Estrutura lógica do código----------------------------
if __name__ == '__main__':
    
    definicao_parametros_graficos()
    
    # ==================================================
    # Import dataset
    # ==================================================
    df = pd.read_csv('..order_items_cleaned.csv')

    # ==================================================
    # Barra Lateral
    # ==================================================
    image=Image.open('logo.jpeg')
    st.sidebar.image(image, width=250)
    
    st.sidebar.title('ALLSHOP')
    st.sidebar.subheader(' Transforme Dados em Decisões!')
    st.sidebar.subheader('Descubra Tendências e Oportunidades', divider='gray')
    
    customers_df, sellers_df=filtra_df(df)
    
    st.sidebar.subheader('', divider='gray')
    st.sidebar.subheader('Powered by: Jadson N Santos')
    # ==================================================
    # Layout no Streamliy
    # ==================================================
    tab1, tab2, tab3, tab4=st.tabs(['🏠 Home', '📉 Indicadores Gerais', '📊 Visão Geral Gráfica', '📈 Análises dos Gráficos'])

    with tab1:
        st.write('# Projeto de Análise de Vendas por Estado- Dashbord')
        st.markdown(
    """ 
    <span style="font-size:22px;">
    A AllShop, uma loja de departamento que opera em marketplaces, está enfrentando desafios para entender e otimizar suas operações
    comerciais. O rápido crescimento da empresa trouxe consigo a necessidade de uma análise de dados mais estruturada para embasar a tomada de decisões estratégicas. 
    Um dos principais problemas identificados envolve a avaliação das vendas, o faturamento por categoria e a relação entre a quantidade de fotos e produtos cadastrados. 
    Além disso, o CEO demonstrou preocupação com o faturamento perdido devido a pedidos cancelados e quer um acompanhamento detalhado sobre esse impacto.
    </span>
    <br><br>
    <span style="font-size:22px;">
    Após uma reunião com a diretoria, foi decidido desenvolver análises gráficas para responder a questões-chave, como a evolução das vendas diárias e mensais, 
    a relação entre categorias e faturamento, e a performance dos produtos em relação às imagens cadastradas. Além disso, o CEO deseja aprimorar as análises anteriores 
    com representações gráficas mais intuitivas, focando em três métricas principais: Número de Vendas, Número de Clientes Únicos e Número de Vendedores Únicos.
    </span>
    <br><br>
    <span style="font-size:22px;">
    Para tornar essas análises mais interativas, o líder técnico sugeriu a utilização do framework Streamlit, permitindo que os usuários filtrem os dados dinamicamente. 
    No entanto, durante a revisão dos materiais, foi identificado que a organização dos notebooks e scripts poderia ser aprimorada para facilitar a compreensão por toda a equipe. 
    Como solução, foi solicitado que o notebook final e o script do dashboard sejam reorganizados seguindo as melhores práticas de ETL (Extração, Transformação e Carga de Dados), 
    garantindo clareza no fluxo de trabalho.
    </span>
    <br><br>
    <span style="font-size:22px;">
    Além disso, foram sugeridas melhorias no dashboard, como a implementação de um filtro de multi-seleção de estados, garantindo que todos os dados apresentados 
    sejam filtrados corretamente e que o posicionamento dos filtros facilite a visualização. Com essas melhorias, espera-se que a AllShop consiga tomar decisões 
    mais embasadas e estratégicas para manter sua competitividade no mercado.
    </span>
    """,
    unsafe_allow_html=True)     
 
with tab2: 
    # Big Number
    big_numbers(customers_df, sellers_df)
    
with tab3:
    # Visão Geral Gráficas
    visoes_gerais(customers_df, sellers_df)

with tab4:
    # Visões Temporais (mês) para o Estado Selecionado
    visoes_temporais(customers_df, sellers_df)
