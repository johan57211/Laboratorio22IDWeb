import requests

url = "https://pokeapi.co/api/v2/pokemon"

parametros = {
    "limit": 10, 
    "offset": 0   
}

print("> Obteniendo los primeros 10 Pokémon...\n")
respuesta = requests.get(url, params=parametros)

if respuesta.status_code == 200:
    datos = respuesta.json()
    print("=" * 30)
    print("PRIMEROS 10 POKÉMON:")
    print("=" * 30)

    for i, pokemon in enumerate(datos['results'], 1):
        nombre = pokemon['name']
        print(f"{i}. {nombre.capitalize()}")
    
else:
    print(f"Error: {respuesta.status_code}")
    print(f"Mensaje: {respuesta.text}")