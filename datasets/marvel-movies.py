import streamlit as st
import pandas as pd
import plotly.express as px

## Configurações Gerais da Página
st.set_page_config(
    page_title="Dados de Bilheteria - Marvel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

### Estilização CSS
with open ('style.css', 'r') as fp:
    st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

#### Carregamento de dados com Pandas
df_reshaped = pd.read_csv('./Marvel-Movies.csv')

###### Sidebar
with st.sidebar:
    st.title ('Bilheterias Marvel')

    list_anos = sorted(df_reshaped.year.unique(), reverse=True)

    selected_year = st.selectbox('Selecione um ano: ',list_anos)
    df_selected_year = df_reshaped [df_reshaped.year == selected_year]
    df_filtered_year = df_reshaped[df_reshaped.year == selected_year]

    st.markdown('##### Desenvolvido por Breno Mencalha, PDITA098')

######## Cabeçalho
st.header('Desempenho financeiro dos filmes da Marvel - 2008 a 2023')
st.markdown('Essa análise tem como escopo fornecer informações sobre o sucesso comercial e a recepção destes filmes, ajudando a compreender o seu desempenho sob múltiplas perspectivas.')

######## Métricas
cols1 = st.columns(3)

cols1[0].metric('Orçamento Anual', f'$ {df_selected_year["budget"].sum():.0f} M')
cols1[1].metric('Faturamento Anual Bruto', f'$ {df_selected_year["worldwide gross ($m)"].sum():.0f} M')
cols1[2].metric('Lucro Líquido Anual', f'$ {df_selected_year["net profit"].sum():.0f} M')

######## Plots
cols3 = st.columns((2), gap="medium")

with cols3[0]:
    finance_total = df_filtered_year.groupby(["category", 'year'])[["worldwide gross ($m)"]].sum().reset_index()
    fig_finance_total = px.bar(finance_total, x="category",y="worldwide gross ($m)", color_discrete_sequence=['#73242A'])
    fig_finance_total.update_layout(yaxis_title="Faturamento Bruto ($ M)", xaxis_title="Categoria", showlegend=False,title="Faturamento anual por categoria")
    st.plotly_chart(fig_finance_total,use_container_width=True)

with cols3[1]:
    fig_movies_fragment = px.pie(df_filtered_year,values="worldwide gross ($m)", names="movie", title="Percentual do faturamento por filmes (%)", color_discrete_sequence=['#73242A','#26151A','#162226'])
    fig_movies_fragment.update_traces(textposition="inside", textinfo='percent')
    fig_movies_fragment.update_layout(showlegend=True)
    st.plotly_chart(fig_movies_fragment,use_container_width=True)

cols4 = st.columns((2), gap="medium")

with cols4[0]:
    lucro_liquido_por_filme = df_filtered_year.groupby(["movie",'year'])['net profit'].sum().reset_index().sort_values('net profit')
    fig_lucro_liquido = px.bar(lucro_liquido_por_filme,x='net profit', y='movie',title="Lucro Líquido Anual por Filme", orientation='h',color_discrete_sequence=['#73242A'])
    fig_lucro_liquido.update_layout(yaxis_title="Filmes", xaxis_title="Lucro Líquido ($ M)", showlegend=False)
    fig_lucro_liquido.update_traces(textposition="inside")
    st.plotly_chart(fig_lucro_liquido,use_container_width=True)

with cols4[1]:
    fig_percentual_lucro = px.pie(df_filtered_year,values="net profit", names="movie", title="Percentual de lucro por filmes (%)", color_discrete_sequence=['#73242A','#26151A','#162226'])
    fig_percentual_lucro.update_traces(textposition="inside", textinfo='percent')
    fig_percentual_lucro.update_layout(showlegend=True)
    st.plotly_chart(fig_percentual_lucro,use_container_width=True)

cols5 = st.columns(1)
with cols5[0]:
    st.markdown('## Informações Complementares de Desempenho')
    st.dataframe(df_filtered_year)


