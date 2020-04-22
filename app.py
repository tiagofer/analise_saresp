import streamlit as st
import pandas as pd
import numpy as np
from helpers import read_markdown_file, analise_ano, analise_ano,fetch_data_csv

menu = ['Introdução','Entendendo os dados','Total Escolas entre 2011 e 2018',
'Proficiência por disciplina', 'Próximos passos e estudos futuros']

df_saresp = fetch_data_csv()

def main():
    menu_option = st.sidebar.selectbox('Menu',options=menu)
    if menu_option == menu[0]:
        intro_markdown = read_markdown_file('textos/intro.md')
        st.markdown(intro_markdown,unsafe_allow_html=True)
    if menu_option == menu[1]:
        etl = read_markdown_file('textos/etl.md')
        st.write(etl,unsafe_allow_html=True)
    if menu_option == menu[2]:
        texto_escolas = read_markdown_file('textos/analise_escolas.md')
        st.markdown(texto_escolas,unsafe_allow_html=True)
        analise_ano(df_saresp,'arquivo','CODESC')
    if menu_option == menu[3]:
        st.markdown('# pizza')
if __name__ == "__main__":
    main()