from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SumaHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            a = data.get('a', 0)
            b = data.get('b', 0)
            
            suma = a + b
            
            respuesta = {
                "a": a,
                "b": b,
                "suma": suma,
                "operacion": f"{a} + {b} = {suma}"
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error = {"error": "JSON inválido"}
            self.wfile.write(json.dumps(error).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error = {"error": str(e)}
            self.wfile.write(json.dumps(error).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = """
        <html>
        <head><title>Servidor de Suma</title></head>
        <body>
            <h1>Servidor de Suma</h1>
            <p>Envía un POST a esta URL con el formato:</p>
            <pre>{"a": 5, "b": 3}</pre>
        </body>
        </html>
        """
        self.wfile.write(html.encode())


if __name__ == "__main__":
    server_address = ("localhost", 8000)
    server = HTTPServer(server_address, SumaHandler)
    
    print("=" * 50)
    print("Servidor corriendo en http://localhost:8000")
    print("Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        server.shutdown()