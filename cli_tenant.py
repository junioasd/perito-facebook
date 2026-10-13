import os, sys, yaml

def criar_novo_tenant(nome_cliente: str, ambiente: str = "producao"):
    """
    Gera um ficheiro config.yaml parametrizado para um novo cliente corporativo,
    permitindo o onboarding multi-tenant instantâneo do Olimpo AI.
    """
    config_data = {
        "cliente": {
            "nome": nome_cliente,
            "ambiente": ambiente
        },
        "atena_policy": {
            "max_retries": 3,
            "timeout_segundos": 15,
            "verificar_rate_limit": True,
            "politicas_ativas": [
                "rate_limit_failover",
                "auditoria_seguranca",
                "conformidade_operacional"
            ]
        },
        "hermes_dispatch": {
            "prioridade_minima": "alta",
            "executar_tarefas_agendadas": True,
            "max_tarefas_por_ciclo": 5
        },
        "apolo_telemetria": {
            "salvar_historico_local": True,
            "nivel_log": "INFO"
        }
    }

    # Se já existir config, podemos criar com sufixo ou substituir
    caminho = "config.yaml"
    with open(caminho, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)
        
    print(f"[OLIMPO CLI] Sucesso! Tenant '{nome_cliente}' provisionado no arquivo '{caminho}'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nome = sys.argv[1]
        env = sys.argv[2] if len(sys.argv) > 2 else "producao"
        criar_novo_tenant(nome, env)
    else:
        print("Uso: python cli_tenant.py 'Nome do Cliente' 'ambiente'")
