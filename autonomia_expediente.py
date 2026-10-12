import os, sys, asyncio

sys.path.append(os.path.abspath("."))

async def main():
    print("[AUTONOMIA] Construtor ativo.")
    print("[AUTONOMIA] Iniciando ronda do protocolo de autonomia...")
    
    # Lógica de execução da ronda
    os.makedirs("modulo_2_hermes", exist_ok=True)
    with open("modulo_2_hermes/hermes_dispatcher.py", "a") as fm:
        fm.write("# Execução de ciclo efetuada com sucesso\n")
    
    print("[AUTONOMIA] Ronda concluída com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
