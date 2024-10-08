from telebot import TeleBot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import yaml


text = """*СРО простым языком \\- Независимая оценка квалификаций и национальный реестр специалистов\\.*

Сегодня подкаст о том, зачем нужна независимая оценка квалификации, как узнать дату её окончания, и как специалисту избежать исключения из Национального реестра специалистов\\.

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
    InlineKeyboardButton("Вступить в СРО", url="https://t.me/ru_sro_bot"),
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
    video=open("./video.mp4", 'rb'),
    supports_streaming=True,
    caption=text,
    parse_mode="MarkdownV2",
    reply_markup=kbr,
    duration=27,
    height=2160,
    width=3840,
    thumb=open("./preview.jpg", 'rb'),
)
# bot.send_photo(
#     chat_id=CONFIG["bot"]["chanel"],
#     photo=open("./anons.jpg", 'rb'),
#     caption=text,
#     parse_mode="Markdown",
#     reply_markup=kbr
# )