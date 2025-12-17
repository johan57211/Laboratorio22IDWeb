import requests

url = "https://httpbin.org/get"
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

