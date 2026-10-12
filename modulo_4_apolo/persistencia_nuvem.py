import os, json, requests
from datetime import datetime

def salvar_metrica_externa(metricas: dict) -> bool:
    """
    Envia as métricas consolidadas do Apolo para uma base de dados externa via REST.
    Suporta Supabase / Upstash / Webhook personalizado.
    """
    db_url = os.getenv("PERSISTENCE_DB_URL")
    db_api_key = os.getenv("PERSISTENCE_DB_KEY")
    
    if not db_url:
        print("[APOLO PERSISTÊNCIA] Nenhuma URL de banco externa configurada. Mantendo apenas backup local.")
        return False

    headers = {
        "Content-Type": "application/json",
        "apikey": db_api_key or "",
        "Authorization": f"Bearer {db_api_key or ''}"
    }

    try:
        response = requests.post(db_url, json=metricas, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print(f"[APOLO PERSISTÊNCIA] Métricas salvas com SUCESSO na base externa (HTTP {response.status_code}).")
            return True
        else:
            print(f"[APOLO PERSISTÊNCIA] Alerta ao salvar na nuvem: HTTP {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[APOLO PERSISTÊNCIA] Falha ao conectar à base externa: {e}")
        return False
