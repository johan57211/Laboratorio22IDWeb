import json

libros = [
    {"id": 1, "titulo": "1984", "autor": "George Orwell", "año": 1949},
    {"id": 2, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "año": 1967},
    {"id": 3, "titulo": "Don Quijote", "autor": "Miguel de Cervantes", "año": 1605}
]

siguiente_id = 4

def app(environ, start_response):
    global siguiente_id
    
    metodo = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    
    if metodo == "GET" and path == "/libros":
        respuesta = json.dumps(libros, ensure_ascii=False, indent=2)
        status = "200 OK"
        headers = [("Content-Type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [respuesta.encode("utf-8")]
    
    elif metodo == "POST" and path == "/libros":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(content_length)
            
            datos = json.loads(body)
            
            if "titulo" not in datos or "autor" not in datos or "anio" not in datos:
                respuesta = json.dumps({
                    "error": "Faltan campos requeridos: titulo, autor, anio"
                })
                status = "400 Bad Request"
            else:
                nuevo_libro = {
                    "id": siguiente_id,
                    "titulo": datos["titulo"],
                    "autor": datos["autor"],
                    "año": datos["año"]
                }
                
                libros.append(nuevo_libro)
                siguiente_id += 1
                
                respuesta = json.dumps(nuevo_libro, ensure_ascii=False, indent=2)
                status = "201 Created"
        
        except json.JSONDecodeError:
            respuesta = json.dumps({"error": "JSON inválido"})
            status = "400 Bad Request"
        except Exception as e:
            respuesta = json.dumps({"error": str(e)})
            status = "500 Internal Server Error"
        
        headers = [("Content-Type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [respuesta.encode("utf-8")]
    
    elif metodo == "GET" and path.startswith("/libros/"):
        try:
            libro_id = int(path.split("/")[-1])
            
            libro_encontrado = None
            for libro in libros:
                if libro["id"] == libro_id:
                    libro_encontrado = libro
                    break
            
            if libro_encontrado:
                respuesta = json.dumps(libro_encontrado, ensure_ascii=False, indent=2)
                status = "200 OK"
            else:
                respuesta = json.dumps({"error": f"Libro con ID {libro_id} no encontrado"})
                status = "404 Not Found"
        
        except ValueError:
            respuesta = json.dumps({"error": "ID inválido, debe ser un número"})
            status = "400 Bad Request"
        
        headers = [("Content-Type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [respuesta.encode("utf-8")]
    
    else:
        respuesta = json.dumps({"error": "Ruta no encontrada"})
        status = "404 Not Found"
        headers = [("Content-Type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [respuesta.encode("utf-8")]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    
    server = make_server("localhost", 8000, app)
    
    print("=" * 70)
    print("API de Libros corriendo en http://localhost:8000")
    print("=" * 70)
    print("\nEndpoints disponibles:")
    print("  GET  /libros        → Listar todos los libros")
    print("  POST /libros        → Registrar un nuevo libro")
    print("  GET  /libros/<id>   → Consultar un libro por ID")
    print("\nEjemplos de uso:")
    print("  curl http://localhost:8000/libros")
    print("  curl http://localhost:8000/libros/1")
    print('  curl -X POST http://localhost:8000/libros -H "Content-Type: application/json" -d \'{"titulo":"El Principito","autor":"Antoine de Saint-Exupéry","año":1943}\'')
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido")
        server.shutdown()