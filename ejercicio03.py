from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MiServidor(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Mi Servidor</title>
                <style>
                    body {
                        background-color: #f0f0f0;
                        margin: 50px;
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                    }
                    p {
                        color: #666;
                    }
                    a {
                        color: #0066cc;
                        text-decoration: none;
                    }
                </style>
            </head>
            <body>
                <h1>¡Bienvenido a mi servidor!</h1>
                <p>Este es un HTML estático servido desde Python</p>
                <p>Prueba visitar: <a href="/saludo">/saludo</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        
        elif self.path == "/saludo":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            respuesta = {"msg": "Hola"}
            self.wfile.write(json.dumps(respuesta).encode("utf-8"))
        
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Pagina no encontrada")

if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8000), MiServidor)
    print("=" * 50)
    print("Servidor corriendo en http://localhost:8000")
    print("=" * 50)
    print("Rutas disponibles:")
    print("  - http://localhost:8000/       (HTML)")
    print("  - http://localhost:8000/saludo (JSON)")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido")
        servidor.shutdown()