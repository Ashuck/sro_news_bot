from telebot import TeleBot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import yaml


text = """Приветствуем, коллеги, на нашем новостном канале для всех причастных к строительному процессу\\.

Здесь мы публикуем:
Статьи про \\#изменениявзаконодательстве
Статьи про \\#стандартыиправила \\#ценообразование \\#закупки
Статьи про \\#проектирование \\#строительство \\#изыскания
Статьи про \\#судебнаяпрактика 
Подкасты \\#проСРО\\_простым\\_языком

Если у вас есть вопросы в сфере строительства или проектирования вам сюда \\- @feedback\\_sro\\_bot

По вопросам сотрудничества вам сюда \\- @marrina\\_sm

Нами был разработан многофункциональный телеграмм бот, получивший название [«Путеводитель СРО»](https://t.me/about_sro_bot) \\- это телеграмм\\-робот для членов и будущих членов саморегулируемых организаций, который поможет:

✔️ проверить наличие членства у организации по ИНН;
✔️ оперативно получить информацию о любом СРО и условиях вступления в нее;
✔️ получить консультацию профильного специалиста и ответ на любой вопрос в области саморегулирования совершенно бесплатно\\.

❗️Сервис сам предварительно рассчитает взносы, самостоятельно соберет информацию и оформит заявку в СРО любого города на территории России\\.

Вы направляете обращение и сразу же получаете звонок от специалиста\\!"""

print(len(text))

config_path = os.path.dirname(__file__)
with open(config_path + "/config.yaml") as f:
    CONFIG = yaml.safe_load(f)
with open(config_path + CONFIG["bot"]["template"]) as f:
    template = f.read()
bot = TeleBot(CONFIG["bot"]["token"])

kbr = InlineKeyboardMarkup()
kbr.add(
    InlineKeyboardButton("Перейти", url="https://t.me/about_sro_bot")
)


bot.send_message(
    chat_id=CONFIG["bot"]["chanel"],
    text=text,
    parse_mode="MarkdownV2", 
    reply_markup=kbr,
)
# bot.send_video(
#     chat_id=CONFIG["bot"]["chanel"],
#     # chat_id='@ashuck210',
#     video=open("./06.mp4", 'rb'),
#     supports_streaming=True,
#     caption=text,
#     parse_mode="MarkdownV2",
#     reply_markup=kbr,
#     # height=720,
#     # width=1280,
# )
# bot.send_photo(
#     chat_id=CONFIG["bot"]["chanel"],
#     photo=open("./anons.jpg", 'rb'),
#     caption=text,
#     parse_mode="Markdown",
#     reply_markup=kbr
# )