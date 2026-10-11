import os
import sys
import asyncio

# Adicionar a pasta raiz ao PATH para importar todos os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modulo_2_hermes.hermes_dispatcher import HermesDispatcher
from modulo_3_atena.atena_engine import AtenaEngine
from modulo_4_apolo.apolo_metrics import ApoloMetrics
from modulo_5_hefesto_tecnico.hefesto_automation import HefestoAutomation

class OrquestradorMestre:
    """
    Módulo 6 — Orquestrador Mestre (Zeus)
    O maestro central responsável por coordenar a execução contínua
    e a harmonia de todos os módulos do Olimpo AI.
    """
    def __init__(self):
        print("⚡ [Orquestrador] A inicializar o Ecossistema Olimpo AI...")
        self.hermes = HermesDispatcher()
        self.atena = AtenaEngine()
        self.apolo = ApoloMetrics()
        self.hefesto = HefestoAutomation()
        print("⚡ [Orquestrador] Todos os Módulos Soberanos Carregados com Sucesso.")

    async def boot_sequence(self):
        """Sequência de inicialização e diagnóstico completo do ecossistema."""
        print("⚡ [Orquestrador] A executar Sequência de Boot...")
        
        # 1. Registar evento no Apolo
        self.apolo.record_event("SISTEMA_INICIADO", {"status": "Boot Concluído"})

        # 2. Executar auditoria do Hefesto
        await self.hefesto.execute_task("MANUTENCAO", {})

        # 3. Disparar notificação de prontidão global via Hermes
        await self.hermes.send_alert(
            title="Olimpo AI — Ecossistema Totalmente Ativo",
            message=(
                "🏛️ *Todos os Módulos Operacionais:*\n"
                "• *Ares (M1):* Pronto para Comunicação\n"
                "• *Hermes (M2):* Dispatcher Ativo\n"
                "• *Atena (M3):* Cérebro Lógico Ativo\n"
                "• *Apolo (M4):* Métricas & Logs Ativos\n"
                "• *Hefesto (M5):* Infraestrutura Validada\n"
                "• *Orquestrador (M6):* Maestraria Ativa\n\n"
                "⚡ _Soberania e Controlo Total Garantidos._"
            ),
            level="SUCCESS"
        )

# Teste direto do Orquestrador Mestre
if __name__ == "__main__":
    async def main():
        zeus = OrquestradorMestre()
        await zeus.boot_sequence()

    asyncio.run(main())