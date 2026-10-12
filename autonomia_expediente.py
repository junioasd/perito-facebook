import os, sys, asyncio, time, json
from datetime import datetime

sys.path.append(os.path.abspath("."))

async def executar_ronda_hermes():
    """Simula e despacha as tarefas operacionais do Hermes."""
    print("[HERMES] A iniciar despacho de tarefas...")
    # Garante a estrutura necessária
    os.makedirs("modulo_2_hermes", exist_ok=True)
    with open("modulo_2_hermes/hermes_dispatcher.py", "a") as fm:
        fm.write(f"# Execução em {datetime.now().isoformat()}\n")
    await asyncio.sleep(1)  # Simulação de processamento
    return {"status": "sucesso", "tarefas_processadas": 1}

async def registrar_metricas_apolo(inicio_tempo, dados_hermes):
    """Gera e guarda os indicadores de telemetria no Módulo Apolo."""
    tempo_execucao = round(time.time() - inicio_tempo, 2)
    os.makedirs("modulo_4_apolo", exist_ok=True)
    
    metricas = {
        "timestamp": datetime.now().isoformat(),
        "tempo_execucao_segundos": tempo_execucao,
        "status_geral": "OPERACIONAL",
        "detalhes_hermes": dados_hermes
    }
    
    with open("modulo_4_apolo/apolo_metrics.json", "w") as f:
        json.dump(metricas, f, indent=4)
        
    print(f"[APOLO] Métricas registadas com sucesso ({tempo_execucao}s).")
    return metricas

async def main():
    inicio = time.time()
    print("==================================================")
    print("[OLIMPO AI] A iniciar ronda de autonomia 24/7")
    print("==================================================")
    
    # 1. Execução de Tarefas via Hermes
    resultado_hermes = await executar_ronda_hermes()
    
    # 2. Registo de Métricas via Apolo
    await registrar_metricas_apolo(inicio, resultado_hermes)
    
    print("[AUTONOMIA] Ronda do ecossistema concluída!")

if __name__ == "__main__":
    asyncio.run(main())
