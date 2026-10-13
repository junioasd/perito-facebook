import os, json

METRICAS_CREDITOS_FILE = "modulo_4_apolo/tenant_credits.json"

def inicializar_saldo_tenant(tenant_id: str, creditos_iniciais: int = 100):
    dados = {}
    if os.path.exists(METRICAS_CREDITOS_FILE):
        try:
            with open(METRICAS_CREDITOS_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except Exception:
            dados = {}
            
    if tenant_id not in dados:
        dados[tenant_id] = {
            "saldo_creditos": creditos_iniciais,
            "total_consumido": 0,
            "status_conta": "ATIVA"
        }
        with open(METRICAS_CREDITOS_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"[APOLO BILLING] Tenant '{tenant_id}' inicializado com {creditos_iniciais} créditos.")
    return dados.get(tenant_id)

def verificar_e_consumir_credito(tenant_id: str, custo_ronda: int = 1) -> bool:
    """
    Verifica se o cliente tem saldo de créditos.
    Se sim, deduz o valor da ronda e permite a execução.
    Se não, bloqueia o ciclo para proteger a margem financeira do SaaS.
    """
    if not os.path.exists(METRICAS_CREDITOS_FILE):
        inicializar_saldo_tenant(tenant_id)

    with open(METRICAS_CREDITOS_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)

    info_tenant = dados.get(tenant_id, {"saldo_creditos": 0, "status_conta": "BLOQUEADA"})

    if info_tenant["saldo_creditos"] < custo_ronda:
        print(f"[APOLO BILLING ⚠️] SALDO INSUFICIENTE para '{tenant_id}'. Saldo: {info_tenant['saldo_creditos']}. Execução suspensa.")
        return False

    # Deduz o crédito
    info_tenant["saldo_creditos"] -= custo_ronda
    info_tenant["total_consumido"] += custo_ronda
    dados[tenant_id] = info_tenant

    with open(METRICAS_CREDITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"[APOLO BILLING 🟢] 1 Crédito consumido para '{tenant_id}'. Saldo restante: {info_tenant['saldo_creditos']}.")
    return True

if __name__ == "__main__":
    # Teste de inicialização e consumo
    inicializar_saldo_tenant("Empresa Alpha B2B", 50)
    verificar_e_consumir_credito("Empresa Alpha B2B")
