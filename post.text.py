from telebot import TeleBot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import yaml


text = """*СРО простым языком \\- Как выбрать СРО и проверить его надежность?*

Сегодня расскажем ответы на очень важные вопросы:
✔️Как выбрать СРО строителей, проектировщиков?
✔️Как проверить СРО на надежность?
✔️На каких сайтах можно найти перечень СРО?
✔️Почему важно проверять сведения о СРО на надежных ресурсах?

Возможно у кого\\-то был опыт поиска СРО? Какими ресурсами пользовались?
Напишите в предложку\\.

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
    video=open("./06.mp4", 'rb'),
    supports_streaming=True,
    caption=text,
    parse_mode="MarkdownV2",
    reply_markup=kbr,
    # height=720,
    # width=1280,
)
# bot.send_photo(
#     chat_id=CONFIG["bot"]["chanel"],
#     photo=open("./anons.jpg", 'rb'),
#     caption=text,
#     parse_mode="Markdown",
#     reply_markup=kbr
# )