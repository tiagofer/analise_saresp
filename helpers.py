import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from pathlib import Path
import plotly.express as px

def read_markdown_file(markdown_file):
    """Método para leitura de arquivo markdown externo

    Arguments:
        markdown_file {str} -- nome do arquivo markdown para leitura

    Returns:
        str -- [retorna string com o texto do arquivo]
    """    
    return Path(markdown_file).read_text()

@st.cache
def fetch_data_csv():
    df_resultado = pd.read_pickle('dados/saresp_resultado.pkl')
    return df_resultado

def analise_ano(df,x,y):
    df_escolas = df.groupby(x).nunique()
    fig = px.bar(df_escolas,x=df_escolas.index,y=y,
    labels={'x': 'Anos',
    'CODESC': 'Total Escolas'})
    st.plotly_chart(fig)

def show_line(df,x,y,g):
    df = df.groupby([g,x])[y].mean().reset_index()
    fig = (px.scatter(df,x=x,y=y,
    color=g,labels={
        x : 'Ano',
        y :'Nota Competência',
        g : 'Competências'
    }).update_traces(mode='lines+markers'))
    st.plotly_chart(fig)

def show_line_series(df,x,y,g):
    df = df.groupby([g,x])[y].mean().reset_index()
    fig = (px.scatter(x=df[x],y=df[y],
    color=df[g],labels={
        'x' : 'Ano',
        'y':'Nota Competência'
    }).update_traces(mode='lines+markers'))
    st.plotly_chart(fig)

def show_bar(df):
    df_nota_serie = df.groupby(['SERIE_ANO','ds_comp'])['medprof'].mean().reset_index()
    df_nota = df_nota_serie.query('ds_comp != "HISTÓRIA" & ds_comp != "CIÊNCIAS" & ds_comp != "GEOGRAFIA"')
    fig = px.bar(df_nota,x='SERIE_ANO',y='medprof',color='ds_comp',barmode='group')
    st.plotly_chart(fig)