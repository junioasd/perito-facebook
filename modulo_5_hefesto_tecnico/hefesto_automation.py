import os
import sys
import asyncio
import json
from datetime import datetime

# Adicionar a pasta raiz ao PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modulo_2_hermes.hermes_dispatcher import HermesDispatcher

# Tentar importar Supabase de forma segura (Fallback gracioso se não estiver instalado/configurado)
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False


class HefestoAutomation:
    """
    Módulo Hefesto: Responsável por automações técnicas, 
    manutenção da infraestrutura e persistência no Supabase.
    """
    def __init__(self):
        self.dispatcher = HermesDispatcher()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.db_client = None

        if HAS_SUPABASE and self.supabase_url and self.supabase_key:
            try:
                self.db_client: Client = create_client(self.supabase_url, self.supabase_key)
                print("🔨 [Hefesto] Conexão com Supabase estabelecida com sucesso.")
            except Exception as e:
                print(f"⚠️ [Hefesto] Erro ao conectar ao Supabase: {e}")
        else:
            print("🔨 [Hefesto] Supabase não configurado ou credenciais ausentes. Operando em modo de fallback local.")

    def save_log_to_db(self, event_type: str, details: dict):
        """Persiste logs de sistema diretamente no Supabase."""
        if self.db_client:
            try:
                data = {
                    "event_type": event_type,
                    "details": json.dumps(details, ensure_ascii=False),
                    "created_at": datetime.utcnow().isoformat()
                }
                self.db_client.table("system_logs").insert(data).execute()
                print(f"💾 [Hefesto/Supabase] Evento '{event_type}' gravado na base de dados.")
            except Exception as e:
                print(f"⚠️ [Hefesto/Supabase] Falha ao gravar log no Supabase: {e}")
        else:
            print(f"📝 [Hefesto Local] Evento '{event_type}' registado localmente.")

    async def run_system_maintenance(self):
        """Executa rotinas de auditoria da infraestrutura e guarda o resultado."""
        print("🔨 [Hefesto] A iniciar verificação e manutenção da infraestrutura...")
        
        modules = [
            "modulo_1_infra",
            "modulo_2_hermes",
            "modulo_3_atena",
            "modulo_4_apolo",
            "modulo_5_hefesto_tecnico",
            "modulo_6_orquestrador_mestre"
        ]
        
        status_report = []
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        for mod in modules:
            mod_path = os.path.join(base_dir, mod)
            exists = os.path.exists(mod_path)
            symbol = "✅" if exists else "❌"
            status_report.append(f"{symbol} `{mod}`")

        report_details = "\n".join(status_report)

        # Registar a manutenção no Supabase
        self.save_log_to_db("MANUTENCAO_SISTEMA", {"modulos_auditados": len(modules), "status": "OK"})

        # Notificar via Hermes
        await self.dispatcher.send_alert(
            title="Manutenção Técnica Concluída",
            message=f"Hefesto concluiu a auditoria da estrutura:\n\n{report_details}",
            level="SUCCESS"
        )

    async def execute_task(self, task_name: str, payload: dict):
        """Executa automações técnicas específicas."""
        print(f"🔨 [Hefesto] A executar tarefa técnica: '{task_name}'")
        
        if task_name == "MANUTENCAO":
            await self.run_system_maintenance()
        else:
            print(f"🔨 [Hefesto] Tarefa '{task_name}' não reconhecida.")

# Teste direto
if __name__ == "__main__":
    async def main():
        hefesto = HefestoAutomation()
        await hefesto.execute_task("MANUTENCAO", {})

    asyncio.run(main())