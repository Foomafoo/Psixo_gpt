
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "gpt": "задать вопрос ChatGPT"
    })
async def gpt(update, context):
    dialog.mode = "gpt"
    await send_text(update, context, "Напишите сообщение *ChatGPT*:")

async def gpt_dialog(update, context):
    prompt = load_prompt("gpt")
    text = update.message.text
    answer = await chatgpt.send_question(prompt,  text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, "Привет!")
        await send_photo(update, context, "data_gosling")
        await send_text(update, context, "Как дела, *дружище*?")
        await send_text(update, context, "Ты написал " + update.message.text)
        await send_text_buttons(update,context,'Запустить процесс',{
            'start':'Запустить',
            'stop':'Остановить'})
async def hello_button(update, context):
    query = update.callback_query.data   #код кнопки
    await update.callback_query.answer() #помечаем что обработали нажатие на кнопку
    await send_text(update, context, "Вы нажали на кнопку " + query)

dialog=Dialog()
dialog.mode="main"
chatgpt=ChatGptService(token='sk-pUFKDJLKK09898KJKJLJLK87878jkjkkllougTImm')


app = ApplicationBuilder().token("7761287153:AAGY3yS2zqFbdFIt5ynPD3Tnp8egt8XhFb8").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello)) # отключаем команды

app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()

