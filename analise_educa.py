# %%
import pandas as pd
import numpy as np 
import os
import re
from pathlib import Path
import datetime as dt 
import plotly.express as px
import plotly.graph_objects as go
# %%
########Função para carregar todos os arquivos csv em uma pasta e converter em dataframe########
def load_all_csv(folder_name,sep):
    """Carrega todos os arquivos do tipo CSV de uma pasta
    e retorna uma lista de dataframes 
    
    Arguments:
        folder_name {str} -- string com o nome da pasta onde estão os arquivos
        sep {str} -- string com o tipo de separador ';'; ',', etc.
    
    Returns:
        list -- lista com os arquivos convertidos em DataFrame
    """    
    #formata nome do caminho
    path_name = folder_name+'/'
    #cria array com todos os arquivos do diretório
    n_path = np.array(os.listdir(path_name))
    print('#verificando diretório: {}'.format(n_path))
    #cria dataframe de retorno
    df_list = list()
    #itera sobre o array de arquivos listados na pasta
    for filename in np.nditer(n_path):
        print('#inicio carregamento de arquivo {}'.format(filename))
        #verifica se o arquivo é csv
        if 'csv' in str(filename):
            #concatena o nome do caminho com o nome do arquivo
            arch = str(path_name) + str(filename)
            with open(arch,encoding='UTF-8') as f:
                df_temp = pd.read_csv(f,sep=sep,error_bad_lines=False)
            #adiciona o nome do arquivo no dataframe
            df_temp['arquivo'] = filename
            #adiciona dataframe na lista
            df_list.append(df_temp)
    return df_list

# %%
#cria dataframe auxiliar
def create_df_aux(dataframe):
    """Cria um dataframe de especificações do dataframe passado
    
    Arguments:
        dataframe {DataFrame} -- dataframe passado para análise
    
    Returns:
        DataFrame -- DataFrame {
            colunas: nome das colunas 
            tipos_dados: tipos de dados de cada coluna
            total_registros: total de registros de cada coluna
            NA #: número de registros nulos de cada coluna
            NA %: porcentagem de registros nulos de cada coluna
        }
    """    
    df_return = pd.DataFrame({
        'colunas' : dataframe.columns,
        'tipos_dados' : dataframe.dtypes,
        'total_registros' : dataframe.count(),
        'NA #': dataframe.isna().sum(),
        'NA %': (dataframe.isna().sum() / dataframe.shape[0]) * 100
    },index=None)
    return df_return

def convert_to_categorical(dataframe,columns):
    """converte uma lista de colunas para o tipo category
    
    Arguments:
        dataframe {DataFrame} -- dataframe que contém as colunas para conversão
        columns {list} -- lista com o nome das colunas
    
    Returns:
        DataFrame -- dataframe com as colunas convertidas
    """    
    for col in columns:
        dataframe[col] = dataframe[col].astype('category')
    return dataframe
# %%
#carregando todos os arquivos em uma lista, ja convertidos em dataframes
ls_resultado_saresp = load_all_csv('saresp_resultado',';')


# %% 
# Análises Descritiva resultados Saresp 2011 à 2018
ls_resultado_saresp[4]
# %%
#inserindo coluna codRMet no dataframe de 2011 index [4]
df_temp = ls_resultado_saresp[4]
df_temp.insert(loc=3,column='codRMet',value='Unknow')
# %%
#remove item da lista
del ls_resultado_saresp[4]


# %%
#adiciona dataframe com a coluna faltante adicionada
ls_resultado_saresp.append(df_temp)


# %%
#cria um único dataframe concatenando a lista com os demais
df_completo = pd.DataFrame()
for df in ls_resultado_saresp:
    df_completo = pd.concat([df_completo,df],
    sort=False,ignore_index=True)
df_completo.info()

# %%
#Transformação dos dataframe nota_saresp
df_completo['arquivo'] = df_completo['arquivo'].str.extract(r'(\d+)')
df_completo['medprof'] = df_completo['medprof'].str.replace(',','.').astype('float')
# %%
df_completo['arquivo'] = pd.to_datetime(df_completo['arquivo'],format='%Y')
# %%
#visualização do novo dataframe
create_df_aux(df_completo)

# %%
#salva modificações no arquivo saresp_resultado.pkl
df_completo.to_pickle('dados/saresp_resultado.pkl')
df_completo.to_csv('dados/saresp_resultado.csv',sep=';')

# %%
df_escolas = df_completo.groupby('arquivo').nunique()
px.line(df_escolas,x=df_escolas.index,y='CODESC')

# %%
df_competencias = df_completo.groupby(['ds_comp','arquivo'])['medprof'].mean().reset_index()

# %%
fig = go.Figure()
fig = (px.scatter(x=df_competencias['arquivo'],y=df_competencias['medprof'],
color=df_competencias['ds_comp'],labels={
    'x' : 'Ano',
    'y':'Nota Competência'
}).update_traces(mode='lines+markers'))
fig.show()
