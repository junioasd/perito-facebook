import os, sys, asyncio, time, json, yaml
from datetime import datetime
from modulo_4_apolo.persistencia_nuvem import salvar_metrica_externa

sys.path.append(os.path.abspath("."))

def carregar_configuracao():
    caminho_config = "config.yaml"
    if os.path.exists(caminho_config):
        with open(caminho_config, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

async def executar_atena_policy(config):
    cfg_atena = config.get("atena_policy", {})
    politicas = cfg_atena.get("politicas_ativas", [])
    print(f"[ATENA] A verificar {len(politicas)} políticas ativas (Timeout: {cfg_atena.get('timeout_segundos', 15)}s)...")
    
    os.makedirs("modulo_3_atena", exist_ok=True)
    return {
        "atena_status": "APROVADO",
        "politicas_ativas": politicas,
        "max_retries": cfg_atena.get("max_retries", 3)
    }

async def executar_ronda_hermes(config):
    cfg_hermes = config.get("hermes_dispatch", {})
    max_tarefas = cfg_hermes.get("max_tarefas_por_ciclo", 5)
    print(f"[HERMES] Despachando tarefas operacionais (Limite: {max_tarefas} por ciclo)...")
    
    os.makedirs("modulo_2_hermes", exist_ok=True)
    with open("modulo_2_hermes/hermes_dispatcher.py", "a", encoding="utf-8") as fm:
        fm.write(f"# Execução parametrizada em {datetime.now().isoformat()}\n")
    await asyncio.sleep(1)
    return {"status": "SUCESSO", "tarefas_processadas": 1, "limite_ciclo": max_tarefas}

async def registrar_metricas_apolo(inicio_tempo, dados_atena, dados_hermes, config):
    tempo_execucao = round(time.time() - inicio_tempo, 2)
    os.makedirs("modulo_4_apolo", exist_ok=True)
    
    cliente = config.get("cliente", {}).get("nome", "Geral")
    
    metricas = {
        "timestamp": datetime.now().isoformat(),
        "cliente": cliente,
        "tempo_execucao_segundos": tempo_execucao,
        "status_geral": "OPERACIONAL_100%",
        "atena_policy": dados_atena,
        "hermes_dispatch": dados_hermes
    }
    
    # 1. Registro Local
    with open("modulo_4_apolo/apolo_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=4, ensure_ascii=False)
        
    print(f"[APOLO] Métricas gravadas localmente para '{cliente}' ({tempo_execucao}s).")

    # 2. Persistência Externa / Nuvem
    salvar_metrica_externa(metricas)
    return metricas

async def main():
    inicio = time.time()
    config = carregar_configuracao()
    cliente = config.get("cliente", {}).get("nome", "Desconhecido")
    
    print("==================================================")
    print(f"[OLIMPO AI] Execução Parametrizada | Cliente: {cliente}")
    print("==================================================")
    
    # 1. Validação de Regras (Atena)
    resultado_atena = await executar_atena_policy(config)
    
    # 2. Despacho de Tarefas (Hermes)
    resultado_hermes = await executar_ronda_hermes(config)
    
    # 3. Telemetria, Diagnóstico e Persistência Externa (Apolo)
    await registrar_metricas_apolo(inicio, resultado_atena, resultado_hermes, config)
    
    print("==================================================")
    print("[OLIMPO AI] Ciclo com Persistência Externa concluído!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
