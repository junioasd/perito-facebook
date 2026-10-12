import os
import requests

def enviar_relatorio():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Erro: Credenciais do Telegram não encontradas.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "🏛️ Olimpo AI: Ciclo de autonomia executado e relatório gerado com sucesso!"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Relatório enviado com sucesso para o Telegram!")
    else:
        print(f"Erro ao enviar relatório: {response.text}")

if __name__ == "__main__":
    enviar_relatorio()
