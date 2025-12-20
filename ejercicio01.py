import requests

url = "https://httpbin.org/get"
<<<<<<< HEAD
print(f"> Realizando petición GET a: {url}\n")

respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    print("=" * 30)
    print("IP DEL CLIENTE:")
    print("=" * 30)
    print(f"> IP: {datos['origin']}\n")
    
    print("=" * 30)
    print("HEADERS ENVIADOS:")
    print("=" * 30)
    for clave, valor in datos['headers'].items():
        print(f"> {clave}: {valor}")
    print()
    
    print("=" * 30)
    print("ARGS (parámetros de consulta):")
    print("=" * 30)
    if datos['args']:
        for clave, valor in datos['args'].items():
            print(f"> {clave}: {valor}")
    else:
        print("> No se enviaron parámetros")
    print()
    
else:
    print(f"Error: {respuesta.status_code}")
    print(f"Mensaje: {respuesta.text}")
=======
r = requests.get(url)

data = r.json()

print("IP:", data["origin"])

print("\nHeaders:")
for key, value in data["headers"].items():
    print(f"{key}: {value}")

print("\nArgs:")
if data["args"]:
    for key, value in data["args"].items():
        print(f"{key}: {value}")
else:
    print("No hay argumentos")

>>>>>>> ecc1d9729d916b6b17f005ae1029d51abb8b7609
