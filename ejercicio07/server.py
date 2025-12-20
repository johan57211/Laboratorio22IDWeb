from wsgiref.simple_server import make_server
import json
import os
import mimetypes
from urllib.parse import unquote

equipos = [
    {"id": 1, "nombre": "Real Madrid", "ciudad": "Madrid", "nivelAtaque": 10, "nivelDefensa": 9},
    {"id": 2, "nombre": "Barcelona", "ciudad": "Barcelona", "nivelAtaque": 9, "nivelDefensa": 8},
    {"id": 3, "nombre": "Melgar", "ciudad": "Arequipa", "nivelAtaque": 5, "nivelDefensa": 4}
]

siguiente_id = 4

def servir_estatico(path):
    STATIC_DIR = "static"

    file_path = path.lstrip("/")
    
    full_path = os.path.join(STATIC_DIR, file_path.replace("static/", ""))
    
    if not os.path.isfile(full_path):
        return None, None
    
    content_type, _ = mimetypes.guess_type(full_path)
    if content_type is None:
        content_type = "application/octet-stream"
    
    with open(full_path, "rb") as f:
        return f.read(), content_type

def app(environ, start_response):
    global siguiente_id
    
    metodo = environ["REQUEST_METHOD"]
    path = unquote(environ["PATH_INFO"])
    
    if path.startswith("/static/"):
        contenido, tipo = servir_estatico(path)
        if contenido is None:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Archivo no encontrado"]
        start_response("200 OK", [("Content-Type", tipo)])
        return [contenido]
    
    if metodo == "GET" and path == "/":
        contenido, tipo = servir_estatico("/static/index.html")
        if contenido is None:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"index.html no encontrado en /static/"]
        start_response("200 OK", [("Content-Type", tipo)])
        return [contenido]
    
    if metodo == "GET" and path == "/equipos":
        respuesta = json.dumps(equipos, ensure_ascii=False, indent=2)
        start_response("200 OK", [("Content-Type", "application/json; charset=utf-8")])
        return [respuesta.encode("utf-8")]
    
    if metodo == "POST" and path == "/equipos":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(content_length)
            datos = json.loads(body)
            
            campos_requeridos = ["nombre", "ciudad", "nivelAtaque", "nivelDefensa"]
            if not all(campo in datos for campo in campos_requeridos):
                respuesta = json.dumps({
                    "error": f"Faltan campos requeridos: {', '.join(campos_requeridos)}"
                })
                start_response("400 Bad Request", [("Content-Type", "application/json")])
                return [respuesta.encode("utf-8")]
            
            if not (1 <= datos["nivelAtaque"] <= 10 and 1 <= datos["nivelDefensa"] <= 10):
                respuesta = json.dumps({
                    "error": "Los niveles de ataque y defensa deben estar entre 1 y 10"
                })
                start_response("400 Bad Request", [("Content-Type", "application/json")])
                return [respuesta.encode("utf-8")]
            
            nuevo_equipo = {
                "id": siguiente_id,
                "nombre": datos["nombre"],
                "ciudad": datos["ciudad"],
                "nivelAtaque": datos["nivelAtaque"],
                "nivelDefensa": datos["nivelDefensa"]
            }
            
            equipos.append(nuevo_equipo)
            siguiente_id += 1
            
            respuesta = json.dumps(nuevo_equipo, ensure_ascii=False, indent=2)
            start_response("201 Created", [("Content-Type", "application/json; charset=utf-8")])
            return [respuesta.encode("utf-8")]
        
        except json.JSONDecodeError:
            respuesta = json.dumps({"error": "JSON inválido"})
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [respuesta.encode("utf-8")]
        except Exception as e:
            respuesta = json.dumps({"error": str(e)})
            start_response("500 Internal Server Error", [("Content-Type", "application/json")])
            return [respuesta.encode("utf-8")]
    
    if metodo == "GET" and path.startswith("/equipos/"):
        try:
            equipo_id = int(path.split("/")[-1])
            
            equipo_encontrado = None
            for equipo in equipos:
                if equipo["id"] == equipo_id:
                    equipo_encontrado = equipo
                    break
            
            if equipo_encontrado:
                respuesta = json.dumps(equipo_encontrado, ensure_ascii=False, indent=2)
                start_response("200 OK", [("Content-Type", "application/json; charset=utf-8")])
            else:
                respuesta = json.dumps({"error": f"Equipo con ID {equipo_id} no encontrado"})
                start_response("404 Not Found", [("Content-Type", "application/json")])
            
            return [respuesta.encode("utf-8")]
        
        except ValueError:
            respuesta = json.dumps({"error": "ID inválido, debe ser un número"})
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [respuesta.encode("utf-8")]
    
    respuesta = json.dumps({"error": "Ruta no encontrada"})
    start_response("404 Not Found", [("Content-Type", "application/json")])
    return [respuesta.encode("utf-8")]


if __name__ == "__main__":
    server = make_server("localhost", 8000, app)
    
    print("=" * 70)
    print("Servidor WSGI - API de Eqsuipos de Fútbol")
    print("=" * 70)
    print("URL: http://localhost:8000")
    print("\nArchivos estáticos:")
    print("   http://localhost:8000/              → index.html")
    print("   http://localhost:8000/static/*      → archivos CSS, JS, imágenes")
    print("\nAPI Endpoints:")
    print("   GET  /equipos        → Listar todos los equipos")
    print("   POST /equipos        → Registrar un nuevo equipo")
    print("   GET  /equipos/<id>   → Consultar un equipo por ID")
    print("\nEjemplos de prueba:")
    print("   curl http://localhost:8000/equipos")
    print("   curl http://localhost:8000/equipos/1")
    print("   curl -X POST http://localhost:8000/equipos -H 'Content-Type: application/json' -d '{\"nombre\":\"Manchester United\",\"ciudad\":\"Manchester\",\"nivelAtaque\":8,\"nivelDefensa\":7}'")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido correctamente")
        server.shutdown()