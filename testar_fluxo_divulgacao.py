from modulo_1_ares.growth_supervisor import GrowthSupervisorAgent

print("==================================================")
print("🏛️ OLIMPO AI — TESTE DOS 2 PASSOS DE DIVULGAÇÃO")
print("==================================================")

# Instancia o Agente de Crescimento
agente = GrowthSupervisorAgent("Olimpo_Enterprise")

print("\n--- [PASSO 1] GERANDO PROPOSTA AUTÓNOMA DE DIVULGAÇÃO B2B ---")
proposta = agente.criar_proposta_divulgacao(
    canal="LinkedIn B2B Enterprise",
    mensagem="🚀 O Olimpo AI redefine a autonomia empresarial com auditoria criptográfica SHA-256 e motor de rollback de risco zero. Agende uma demonstração executiva hoje!"
)
print(f"ID Atribuído: {proposta['id']}")
print(f"Estado Inicial: {proposta['status']}")

print("\n--- [PASSO 2] SIMULANDO APROVAÇÃO HUMANA (HUMAN-IN-THE-LOOP) ---")
sucesso = agente.aprovar_e_despachar(proposta["id"])

if sucesso:
    print("\n✅ Fluxo de 2 Passos concluído com sucesso absoluto!")
    print("O conteúdo foi gerado autonomamente, retido em segurança pela política de Atena e aprovado pelo gestor para despacho do Hermes.")
else:
    print("\n⚠️ Falha ao processar a aprovação.")
