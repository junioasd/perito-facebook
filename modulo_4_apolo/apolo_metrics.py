import os
import sys
import json
import asyncio
from datetime import datetime

# Adicionar a pasta raiz ao PATH para importar outros módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modulo_2_hermes.hermes_dispatcher import HermesDispatcher

class ApoloMetrics:
    """
    Módulo Apolo: Responsável pela monitorização de métricas, 
    registo de logs operacionais e relatórios de saúde do Olimpo AI.
    """
    def __init__(self, log_file="apolo_metrics.json"):
        self.log_file = os.path.join(os.path.dirname(__file__), log_file)
        self.dispatcher = HermesDispatcher()
        self._ensure_log_file()
        print("☀️ [Apolo] Módulo de Métricas e Monitorização Inicializado.")

    def _ensure_log_file(self):
        """Garante que o ficheiro de métricas existe."""
        if not os.path.exists(self.log_file):
            initial_data = {
                "total_eventos": 0,
                "mensagens_processadas": 0,
                "alertas_disparados": 0,
                "historico": []
            }
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=4, ensure_ascii=False)

    def record_event(self, event_type: str, details: dict):
        """Regista um evento no histórico e atualiza as contagens."""
        with open(self.log_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data["total_eventos"] += 1
            
            if event_type == "NOVA_MENSAGEM":
                data["mensagens_processadas"] += 1
            elif event_type == "ALERTA_ENVIADO":
                data["alertas_disparados"] += 1

            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tipo": event_type,
                "detalhes": details
            }
            data["historico"].append(entry)

            # Manter apenas os últimos 50 eventos no histórico para otimização
            if len(data["historico"]) > 50:
                data["historico"] = data["historico"][-50:]

            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()

        print(f"☀️ [Apolo] Evento '{event_type}' registado com sucesso.")

    async def generate_report(self):
        """Gera e envia um relatório de métricas consolidado via Hermes."""
        with open(self.log_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        report_message = (
            f"📊 *Total de Eventos:* `{data['total_eventos']}`\n"
            f"💬 *Mensagens Processadas:* `{data['mensagens_processadas']}`\n"
            f"🚨 *Alertas Disparados:* `{data['alertas_disparados']}`\n\n"
            f"☀️ _Status do Olimpo AI: 100% Operacional e Monitorizado_"
        )

        await self.dispatcher.send_alert(
            title="Relatório de Métricas Operacionais",
            message=report_message,
            level="INFO"
        )

# Teste direto do Módulo Apolo
if __name__ == "__main__":
    async def main():
        apolo = ApoloMetrics()
        
        # Teste 1: Registo de métricas simuladas
        apolo.record_event("NOVA_MENSAGEM", {"user_id": "8928125542", "text": "Teste Apolo"})
        apolo.record_event("ALERTA_ENVIADO", {"origem": "Hermes"})

        # Teste 2: Emitir relatório para o Telegram
        await apolo.generate_report()

    asyncio.run(main())
    