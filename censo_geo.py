import time
import googlemaps
from diskcache import Cache

from censo_loader import load_data

gmaps = googlemaps.Client(key='')

dados = load_data()
cache = Cache("geo.cache")

for index, row in dados[(dados["NO_UF"] == "São Paulo") & (dados["NO_MUNICIPIO"] == "São Paulo")].iterrows():
    if row["CO_CEP"] in cache:
        continue

    cep = "0" + str(row["CO_CEP"])[0:4] + "-" + str(row["CO_CEP"])[4:]
    print(cep)
    
    geocode_result = gmaps.geocode(cep)
    try:
        print(geocode_result[0]["formatted_address"], geocode_result[0]["geometry"]["location"])
    except:
        print(geocode_result)
    
    cache[row["CO_CEP"]] = geocode_result
    time.sleep(0.2)

for cep in cache:
    if len(cache[cep]) == 0:
        row = dados[dados["CO_CEP"] == cep]
        endereco = str(row["DS_ENDERECO"].values[0]) + " " + str(row["NU_ENDERECO"].values[0]) + ", " + str(row["NO_MUNICIPIO"].values[0]) + " - " + str(row["SG_UF"].values[0])

        print(endereco)
        geocode_result = gmaps.geocode(str(cep)[:5] + " Brazil")

        cache[cep] = geocode_result
        time.sleep(0.2)