import requests

url = "https://httpbin.org/get"
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