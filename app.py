import streamlit as st
import pandas as pd
import numpy as np
from helpers import read_markdown_file, analise_ano, analise_ano,fetch_data_csv, \
show_line,show_bar

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
        analise_ano(df_saresp,'arquivo','NOMESC')
    if menu_option == menu[3]:
        prof_intro = read_markdown_file('textos/proficiencia_intro.md')
        st.markdown(prof_intro,unsafe_allow_html=True)
        st.markdown('# Média das notas por disciplina ao longo dos anos')
        show_line(df_saresp,'arquivo','medprof','ds_comp')
        st.markdown('Na análise acima, observa-se uma evolução nas notas médias de Português e matemática.')
        st.markdown('Isolando-se as duas disciplinas, vamos agora observar o comportamento destas notas conforme a série.')
        show_bar(df_saresp)
if __name__ == "__main__":
    main()