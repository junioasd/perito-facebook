import os, json, requests

def enviar_relatorio_ares():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[ARES] Credenciais do Telegram em falta. Relatório ignorado.")
        return

    # Ler as métricas mais recentes do Módulo Apolo
    metricas_path = "modulo_4_apolo/apolo_metrics.json"
    info_extra = ""
    if os.path.exists(metricas_path):
        try:
            with open(metricas_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                info_extra = (
                    f"\n🏢 **Cliente:** {data.get('cliente', 'Geral')}"
                    f"\n⏱️ **Tempo de Execução:** {data.get('tempo_execucao_segundos', 0)}s"
                    f"\n🛡️ **Estado Atena:** {data.get('atena_policy', {}).get('atena_status', 'N/A')}"
                    f"\n⚙️ **Estado Geral:** {data.get('status_geral', 'OPERACIONAL')}"
                )
        except Exception as e:
            print(f"[ARES] Erro ao ler métricas do Apolo: {e}")

    mensagem = (
        "🏛️ **OLIMPO AI — Relatório de Autonomia 24/7**\n"
        "--------------------------------------------------"
        f"{info_extra}\n\n"
        "✅ Ciclo concluído com soberania e estabilidade na nuvem!"
    )
    
    # Teclado interativo com botões de controlo direto no Telegram
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔄 Forçar Nova Ronda", "callback_data": "forcar_ronda"},
                {"text": "📊 Ver Métricas Detalhadas", "callback_data": "ver_metricas"}
            ]
        ]
    }

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("[ARES] Relatório interativo enviado com sucesso para o Telegram!")
        else:
            print(f"[ARES] Erro ao enviar notificação: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ARES] Falha de rede ao contactar a API do Telegram: {e}")

if __name__ == "__main__":
    enviar_relatorio_ares()
