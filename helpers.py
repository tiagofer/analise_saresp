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
