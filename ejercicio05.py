from wsgiref.simple_server import make_server

def app(environ, start_response):
    
    path = environ["PATH_INFO"]
    
    if path == "/":
        respuesta = b"Inicio"
        status = "200 OK"
        headers = [("Content-Type", "text/plain; charset=utf-8")]
    
    elif path == "/saludo":
        respuesta = b"Hola mundo desde WSGI"
        status = "200 OK"
        headers = [("Content-Type", "text/plain; charset=utf-8")]
    
    else:
        respuesta = b"404 - Ruta no encontrada"
        status = "404 Not Found"
        headers = [("Content-Type", "text/plain; charset=utf-8")]
    
    start_response(status, headers)
    return [respuesta]

if __name__ == "__main__":
    server = make_server("localhost", 8000, app)
    
    print("=" * 60)
    print("Servidor WSGI corriendo en http://localhost:8000")
    print("=" * 60)
    print("\nRutas disponibles:")
    print("  http://localhost:8000/         → Inicio")
    print("  http://localhost:8000/saludo   → Hola mundo desde WSGI")
    print("  http://localhost:8000/otra     → 404 (cualquier otra ruta)")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido")
        server.shutdown()