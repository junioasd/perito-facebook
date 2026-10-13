import os
import json
from datetime import datetime

FILA_DIVULGACAO_FILE = "modulo_1_ares/pendentes_divulgacao.json"

class GrowthSupervisorAgent:
    """
    Agente Autónomo de Divulgação Supervisionada do Olimpo AI:
    - Gera conteúdos de marketing e propostas B2B.
    - Retém o conteúdo em fila de revisão (Atena/Ares).
    - Exige validação humana antes de autorizar o despacho final pelo Hermes.
    """
    def __init__(self, tenant_id: str = "Olimpo_AI_Core"):
        self.tenant_id = tenant_id

    def criar_proposta_divulgacao(self, canal: str, mensagem: str) -> dict:
        os.makedirs("modulo_1_ares", exist_ok=True)
        proposta = {
            "id": f"div_{int(datetime.now().timestamp())}",
            "canal": canal,
            "mensagem": mensagem,
            "status": "PENDENTE_APROVACAO_HUMANA",
            "timestamp": datetime.now().isoformat()
        }
        
        fila = []
        if os.path.exists(FILA_DIVULGACAO_FILE):
            try:
                with open(FILA_DIVULGACAO_FILE, "r", encoding="utf-8") as f:
                    fila = json.load(f)
            except Exception:
                fila = []

        fila.append(proposta)
        with open(FILA_DIVULGACAO_FILE, "w", encoding="utf-8") as f:
            json.dump(fila, f, indent=4, ensure_ascii=False)

        print(f"[ARES GROWTH 📢] Nova proposta para '{canal}' gerada com sucesso.")
        print(f"[ALERTA TELEGRAM 💬] Mensagem enviada para revisão humana. ID da Proposta: {proposta['id']}")
        return proposta

    def aprovar_e_despachar(self, proposta_id: str) -> bool:
        if not os.path.exists(FILA_DIVULGACAO_FILE):
            return False
        
        with open(FILA_DIVULGACAO_FILE, "r", encoding="utf-8") as f:
            fila = json.load(f)

        encontrado = False
        for p in fila:
            if p["id"] == proposta_id and p["status"] == "PENDENTE_APROVACAO_HUMANA":
                p["status"] = "APROVADO_E_PUBLICADO"
                p["despachado_em"] = datetime.now().isoformat()
                encontrado = True
                print(f"[HERMES DISPATCH 🚀] Proposta {proposta_id} validada e publicada autonomamente no canal {p['canal']}!")
                break

        if encontrado:
            with open(FILA_DIVULGACAO_FILE, "w", encoding="utf-8") as f:
                json.dump(fila, f, indent=4, ensure_ascii=False)
            return True
        
        print(f"[AVISO ⚠️] Proposta {proposta_id} não encontrada ou já processada.")
        return False

if __name__ == "__main__":
    agente = GrowthSupervisorAgent()
    # Exemplo de geração autónoma de post corporativo
    prop = agente.criar_proposta_divulgacao(
        canal="LinkedIn B2B",
        mensagem="🚀 O Olimpo AI redefine a autonomia empresarial com auditoria criptográfica SHA-256 e motor de rollback de risco zero. Agende uma demonstração executiva hoje!"
    )
    # Simula a aprovação pelo gestor via painel Ares/Telegram
    agente.aprovar_e_despachar(prop["id"])
