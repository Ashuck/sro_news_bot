from telebot import TeleBot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import yaml


text = """*СРО простым языком \\- Как проверить членство в СРО?*

Двигаемся дальше, и сегодня новый подкаст, который отвечает на вопрос, и уже от друзей и подписчиков\\. Можно ли проверить, состоит ли организация в СРО? И если можно, то как это сделать обычному человеку\\.

Актуально? Тогда смотрите видео\\! В нем мы поговорили о том, на каких сайтах можно проверить, состоит ли организация в СРО, и как это сделать с помощью тг\\-бота, который мы запустили\\.

📝Если у вас есть вопросы или предложения \\- пишите @marrina\\_sm\\. Конструктивная обратная связь приветствуется\\!

\\#проСРО\\_простым\\_языком

> 1\\. Проверить организацию на членство в СРО\\. 
> 
> 2\\. Получить информацию и рассчитать примерную стоимость членства в СРО\\. 

Вам поможет наш бот \\- Путеводитель СРО

                          👇ЖМИ👇"""

print(len(text))

config_path = os.path.dirname(__file__)
with open(config_path + "/config.yaml") as f:
    CONFIG = yaml.safe_load(f)
with open(config_path + CONFIG["bot"]["template"]) as f:
    template = f.read()
bot = TeleBot(CONFIG["bot"]["token"])

kbr = InlineKeyboardMarkup()
kbr.add(
    InlineKeyboardButton("Вступить в СРО", url="https://t.me/ru_sro_bot")
)
kbr.add(
    InlineKeyboardButton("Проверить компанию по ИНН", url="https://t.me/about_sro_bot")
)


# bot.send_message(
#     chat_id=CONFIG["bot"]["chanel"],
#     text=text,
#     parse_mode="MarkdownV2", 
#     reply_markup=kbr,
# )
bot.send_video(
    chat_id=CONFIG["bot"]["chanel"],
    # chat_id='@ashuck210',
    video=open("./03.mp4", 'rb'),
    caption=text,
    parse_mode="MarkdownV2",
    reply_markup=kbr,
    # height=720,
    # width=1280,
    supports_streaming=True,
)
# bot.send_photo(
#     chat_id=CONFIG["bot"]["chanel"],
#     photo=open("./anons.jpg", 'rb'),
#     caption=text,
#     parse_mode="Markdown",
#     reply_markup=kbr
# )