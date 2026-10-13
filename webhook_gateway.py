import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # Validação opcional de segredo corporativo
        webhook_secret = os.getenv("WEBHOOK_SECRET", "olimpo_secret_default")
        req_secret = self.headers.get("X-Webhook-Secret", "")
        
        if webhook_secret != "olimpo_secret_default" and req_secret != webhook_secret:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized webhook secret"}')
            return

        try:
            payload = json.loads(post_data.decode('utf-8'))
            event_type = payload.get("event_type", "desconhecido")
            tenant = payload.get("tenant", "geral")
            
            print(f"[WEBHOOK GATEWAY] Evento recebido: '{event_type}' para o tenant '{tenant}' em {datetime.now().isoformat()}")
            
            # Registo imediato do evento para processamento prioritário pelo Hermes
            os.makedirs("modulo_2_hermes/eventos", exist_ok=True)
            evento_path = f"modulo_2_hermes/eventos/evento_{int(datetime.now().timestamp())}.json"
            with open(evento_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            resposta = {
                "status": "SUCESSO",
                "mensagem": f"Evento corporativo '{event_type}' capturado com sucesso pelo Olimpo AI."
            }
            self.wfile.write(json.dumps(resposta).encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "Olimpo AI Webhook Gateway is running 24/7"}')

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"[OLIMPO GATEWAY] Servidor de Webhooks ativo na porta {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    run_server(port)
