import requests

url = "https://pokeapi.co/api/v2/pokemon?limit=10"
r = requests.get(url)

data = r.json()

for pokemon in data["results"]:
    print(pokemon["name"])
