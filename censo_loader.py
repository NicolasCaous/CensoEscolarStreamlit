import pandas as pd
import streamlit as st

from openpyxl import load_workbook


def load_data():
    df = pd.read_csv("./microdados_censo_escolar_2021/2021/dados/microdados_ed_basica_2021.csv",  sep=';', encoding="latin-1")
    df['CO_ORGAO_REGIONAL'] = df['CO_ORGAO_REGIONAL'].astype(str)
    return df

@st.cache
def load_data_pd():
    df = pd.read_csv("./microdados_censo_escolar_2021/2021/dados/microdados_ed_basica_2021.csv",  sep=';', encoding="latin-1")
    df['CO_ORGAO_REGIONAL'] = df['CO_ORGAO_REGIONAL'].astype(str)
    return df

@st.cache
def load_helpers():
    wb = load_workbook(filename="./microdados_censo_escolar_2021/2021/Anexos/ANEXO I - Dicionário de Dados/dicionário_dados_educação_básica.xlsx")
    ws = wb["Cadastro_Escolas"]
    
    helpers = {}
    for cellB, cellC, cellF in zip(ws["B"], ws["C"], ws["F"]):
        helpers[cellB.value] = cellC.value
        if cellF.value is not None:
            helpers[cellB.value] += "\n" + cellF.value
    
    for column in ["Alteração de nomenclatura", "Variável nova", "Descontinuidade", None, "Nome da Variável"]:
        del helpers[column]

    return helpers
    
    