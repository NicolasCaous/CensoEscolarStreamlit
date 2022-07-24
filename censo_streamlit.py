import io
import streamlit as st
import pydeck as pdk

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

row_count = len(df.index)
st.markdown("---\nSelecione o mínimo de linhas possível. Isso faz o programa funcionar mais rápido.")
st.text("Número total de linhas: " + str(row_count))
limit = st.number_input("Limite de linhas", 0, row_count, row_count if row_count < 100 else 100)
df = df.head(limit)

if len(columns) == 0:
    st.dataframe(df)    
else:
    st.dataframe(df[columns])
    
file_to_download = io.BytesIO()
df.to_csv(file_to_download, sep=";")
st.download_button("Download resultado", file_to_download, file_name="censo_escolar_selecao")
    
df = df[["NO_ENTIDADE", "lat", "lng", "DS_ENDERECO", "NU_ENDERECO", "NO_MUNICIPIO", "SG_UF", "CO_CEP", "NU_DDD", "NU_TELEFONE"]]
df = df[(df["lat"] != 0) & (df["lng"] != 0)]

if len(df.index) > 0:
    st.markdown("O mapa está disponível apenas para a cidade de São Paulo pois é o único município cujo dado foi geolocalizado. Contatar Nicolas para geolocalizar outros municipios.")
    if st.checkbox("Mostrar mapa", False):
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=-23.55,
                longitude=-46.63,
                zoom=9,
                pitch=50,
            ),
            tooltip={
                "html": "<b>NO_ENTIDADE:</b> {NO_ENTIDADE}<br/> <b>Endereço:</b> {DS_ENDERECO} {NU_ENDERECO}, {NO_MUNICIPIO} - {SG_UF}<br/> <b>CO_CEP:</b> {CO_CEP}<br/> <b>Telefone:</b> ({NU_DDD}) {NU_TELEFONE}",
                "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}
            },
            layers=[
                pdk.Layer(
                    'ColumnLayer',
                    data=df,
                    pickable=True,
                    auto_highlight=True,
                    elevation_scale=1,
                    elevation_range=[0, 3000],
                    extruded=True,                 
                    coverage=1,
                    get_position='[lng, lat]',
                    get_color='[255, 0, 0, 50]',
                    radius=50
                ),
            ],
        ))