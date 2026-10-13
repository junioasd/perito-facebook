import os
import json
import requests
from datetime import datetime
from modulo_1_ares.growth_supervisor import GrowthSupervisorAgent

class OlimpoRealMarketIntegration:
    """
    Motor Unificado para Operação B2B no Mercado Real:
    1. Entrada: Gateway de Webhooks (captura leads/eventos reais)
    2. Aprovação: Telegram Interativo (Human-in-the-Loop)
    3. Saída: Adaptadores de Despacho Hermes (LinkedIn/Twitter/API Externa)
    """
    def __init__(self):
        self.growth_agent = GrowthSupervisorAgent("Olimpo_Production")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "MOCK_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "MOCK_CHAT_ID")

    # --- FRENTE 1: ENTRADA VIA WEBHOOK GATEWAY ---
    def processar_webhook_entrada(self, payload_evento: dict) -> dict:
        print("\n📥 [FRENTE 1 - WEBHOOK GATEWAY] Evento B2B Recebido de Origem Externa...")
        origem = payload_evento.get("source", "Formulário Site B2B")
        cliente = payload_evento.get("client_name", "Cliente Enterprise")
        
        # O Ares gera automaticamente a proposta de campanha adaptada ao evento
        mensagem_gerada = (
            f"🤝 Boas-vindas à {cliente}! O Olimpo AI ativou o ecossistema autónomo "
            f"com prova SHA-256 e monitorização 24/7. Saiba mais na nossa Status Page."
        )
        
        proposta = self.growth_agent.criar_proposta_divulgacao(
            canal=f"Outreach B2B ({origem})",
            mensagem=mensagem_gerada
        )
        return proposta

    # --- FRENTE 2: NOTIFICAÇÃO MOBILE VIA TELEGRAM ---
    def notificar_gestor_telegram(self, proposta: dict):
        print("\n💬 [FRENTE 2 - TELEGRAM APPROVAL] Disparando Notificação com Botões Inline...")
        texto = (
            f"🔔 *NOVA SOLICITAÇÃO B2B PARA APROVAÇÃO*\n\n"
            f"🆔 *ID:* `{proposta['id']}`\n"
            f"🎯 *Canal:* {proposta['canal']}\n"
            f"💬 *Conteúdo:*\n_{proposta['mensagem']}_\n\n"
            f"⚡ *Ação Requerida:* Clique para Autorizar Publicação."
        )
        
        if self.telegram_token != "MOCK_TOKEN":
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": texto,
                "parse_mode": "Markdown",
                "reply_markup": {
                    "inline_keyboard": [[
                        {"text": "✅ Aprovar & Disparar", "callback_data": f"approve:{proposta['id']}"},
                        {"text": "❌ Barrar", "callback_data": f"reject:{proposta['id']}"}
                    ]]
                }
            }
            try:
                requests.post(url, json=payload, timeout=5)
                print("✅ Alerta enviado para o dispositivo mobile do gestor.")
            except Exception as e:
                print(f"⚠️ Erro ao conectar ao Telegram API: {e}")
        else:
            print("ℹ️ [Modo Simulação] Botão 'Aprovar' pronto na interface móvel do gestor.")

    # --- FRENTE 3: SAÍDA E PUBLICAÇÃO OFICIAL (HERMES ADAPTER) ---
    def despachar_canal_oficial(self, proposta_id: str):
        print("\n🚀 [FRENTE 3 - HERMES DISPATCH] Executando Publicação Oficial de Saída...")
        sucesso = self.growth_agent.aprovar_e_despachar(proposta_id)
        if sucesso:
            print("✨ [PAINEL REAL] Conteúdo publicado com sucesso na API de destino (LinkedIn/Social API)!")
            print("🔒 Registro de auditoria assinado com Hash Criptográfica SHA-256 no Módulo Zeus.")
        return sucesso

if __name__ == "__main__":
    print("==========================================================")
    print("🏛️ OLIMPO AI — SIMULAÇÃO COMPLETA DA TRÍPLICE DO MERCADO REAL")
    print("==========================================================")
    
    sistema = OlimpoRealMarketIntegration()
    
    # 1. Simula Entrada de Webhook
    proposta = sistema.processar_webhook_entrada({
        "source": "Typeform / Lead Capture",
        "client_name": "Tech Corp Int"
    })
    
    # 2. Notifica o Gestor no Telegram
    sistema.notificar_gestor_telegram(proposta)
    
    # 3. Gestor Aprova e o Hermes Despacha
    sistema.despachar_canal_oficial(proposta["id"])
