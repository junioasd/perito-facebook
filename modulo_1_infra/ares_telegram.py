import os
import sys
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Adicionar a pasta raiz ao PATH para importar o Módulo Atena
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modulo_3_atena.atena_engine import AtenaEngine

# Carregar variáveis de ambiente
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configuração de Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Inicializar o Cérebro Lógico (Atena)
atena = AtenaEngine()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user_id = update.effective_chat.id
    msg = f"🏛️ *[OLIMPO AI — ARES]*\n\nBoas-vindas ao sistema! O teu Chat ID é: `{user_id}`"
    
    await update.message.reply_text(msg, parse_mode="Markdown")
    
    # Notificar Atena que o sistema recebeu um /start
    await atena.process_event("SISTEMA_INICIADO", {"user_id": str(user_id)})

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Intercepta qualquer mensagem de texto e envia para o Atena processar."""
    user_text = update.message.text
    user_id = update.effective_chat.id

    print(f"📥 [Ares] Mensagem recebida de {user_id}: '{user_text}'")

    # Confirmar receção ao utilizador
    await update.message.reply_text("⚡ _Mensagem recebida e enviada para o Módulo Atena..._", parse_mode="Markdown")

    # Passar a mensagem para a lógica do Atena
    await atena.process_event("NOVA_MENSAGEM", {
        "text": user_text,
        "user_id": str(user_id)
    })

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("ERRO: TELEGRAM_BOT_TOKEN não encontrado no .env")

    print("⚡ [Ares] Bot ativo e escutando mensagens no Telegram...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()