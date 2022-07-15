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