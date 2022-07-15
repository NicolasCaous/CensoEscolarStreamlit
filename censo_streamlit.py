import streamlit as st

from censo_loader import load_data_pd, load_helpers

df = load_data_pd()
helpers = load_helpers()

filters = st.multiselect("Filtros", list(df))

with st.expander("Parâmetros", expanded=False):
    for column in filters:
        print(column, len(df[column].unique()))
        with st.container():
            st.markdown("---")
            st.text(helpers[column])
            
            if column in ["CO_MUNICIPIO", "CO_MESORREGIAO", "CO_MICRORREGIAO", "CO_ENTIDADE",
                          "CO_DISTRITO", "NO_ENTIDADE", "DS_ENDERECO", "NU_ENDERECO",
                          "DS_COMPLEMENTO", "NO_BAIRRO", "NU_DDD", "NU_TELEFONE", "CO_CEP",
                          "CO_ESCOLA_SEDE_VINCULADA", "NU_CNPJ_ESCOLA_PRIVADA", "NU_CNPJ_MANTENEDORA",
                          "NU_CNPJ_ESCOLA_PRIVADA", "NU_CNPJ_MANTENEDORA", "CO_IES_OFERTANTE"]:
                text = st.text_input(column)
                if len(text) > 0:
                    df = df[df[column].astype(str).str.contains(text)]
            elif column.startswith("QT_"):
                min_bound = float(df[column].min())
                max_bound = float(df[column].max())
                selected_min, selected_max = st.slider(column, min_bound, max_bound, (min_bound, max_bound))
                print(selected_min, selected_max)
                df = df[(df[column] > selected_min) & (df[column] < selected_max)]
            else:
                selected = st.multiselect(column, df[column].unique())
                if len(selected) > 0:
                    df = df[df[column].isin(selected)]

columns = st.multiselect("Colunas", sorted(list(df)))

if len(columns) == 0:
    st.dataframe(df)    
else:
    st.dataframe(df[columns])