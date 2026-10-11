import os, sys, asyncio, time
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

async def main():
    print("[AUTONOMIA] Construtor ativo.")
    while True:
        os.makedirs("modulo_2_hermes", exist_ok=True)
        with open("modulo_2_hermes/hermes_dispatcher.py", "w", encoding="utf-8") as fm:
            fm.write("class HermesDispatcher:\n    def dispatch(self):\n        return 'ok'\n")
        await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(main())
