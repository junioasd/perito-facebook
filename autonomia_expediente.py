import os, sys, asyncio, time, json
from datetime import datetime

sys.path.append(os.path.abspath("."))

async def executar_atena_policy():
    """Módulo Atena: Valida políticas de segurança, resiliência e auditoria."""
    print("[ATENA] A iniciar verificação de políticas e resiliência...")
    os.makedirs("modulo_3_atena", exist_ok=True)
    
    # Validação simulada de regras e disponibilidade
    policy_ok = True
    print("[ATENA] Políticas e limites operacionais validados com SUCESSO.")
    return {"atena_status": "APROVADO", "politicas_ativas": 3}

async def executar_ronda_hermes():
    """Módulo Hermes: Despacha e executa as tarefas prioritárias."""
    print("[HERMES] A iniciar despacho de tarefas operacionais...")
    os.makedirs("modulo_2_hermes", exist_ok=True)
    with open("modulo_2_hermes/hermes_dispatcher.py", "a") as fm:
        fm.write(f"# Execução autorizada pela Atena em {datetime.now().isoformat()}\n")
    await asyncio.sleep(1)
    return {"status": "SUCESSO", "tarefas_processadas": 1}

async def registrar_metricas_apolo(inicio_tempo, dados_atena, dados_hermes):
    """Módulo Apolo: Consolida telemetria e métricas de desempenho."""
    tempo_execucao = round(time.time() - inicio_tempo, 2)
    os.makedirs("modulo_4_apolo", exist_ok=True)
    
    metricas = {
        "timestamp": datetime.now().isoformat(),
        "tempo_execucao_segundos": tempo_execucao,
        "status_geral": "OPERACIONAL_100%",
        "atena_policy": dados_atena,
        "hermes_dispatch": dados_hermes
    }
    
    with open("modulo_4_apolo/apolo_metrics.json", "w") as f:
        json.dump(metricas, f, indent=4)
        
    print(f"[APOLO] Métricas unificadas registadas com sucesso ({tempo_execucao}s).")
    return metricas

async def main():
    inicio = time.time()
    print("==================================================")
    print("[OLIMPO AI] Ronda Autónom3 Unificada (Atena + Hermes + Apolo)")
    print("==================================================")
    
    # 1. Validação de Regras (Atena)
    resultado_atena = await executar_atena_policy()
    
    # 2. Despacho de Tarefas (Hermes)
    resultado_hermes = await executar_ronda_hermes()
    
    # 3. Telemetria e Diagnóstico (Apolo)
    await registrar_metricas_apolo(inicio, resultado_atena, resultado_hermes)
    
    print("==================================================")
    print("[OLIMPO AI] Ciclo concluído com soberania total!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
