from telebot import TeleBot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import yaml


text = """[ЭКОСИСТЕМА](https://t.me/sro_lk_bot) в Telegram!

📱В Telegram запущен  сервис-бот, с помощью которого в несколько кликов можно получить необходимую информацию о членстве в СРО российских строительных, проектных и изыскательных организаций!  

🤔Вам необходимо получить актуальную информацию о подрядчике? Членство в СРО/страхование/проверки/сведения о наличии права/информация о КФ/обязательства по договорам❓
[«ЭКОСИСТЕМА»](https://t.me/sro_lk_bot) справится с этим за несколько секунд❗️

👨‍💻Зайдите на канал [СРО News](https://t.me/sro_news), нажмите в закрепе кнопку [«ЭКОСИСТЕМА»](https://t.me/sro_lk_bot), выберите поиск по ИНН, если организация является членом СРО, telegram- bot бесплатно выдаст результат. 

👉 Переходите по ссылке внизу сообщения, скачивайте карточку организации или смотрите информацию в соответствующих разделах!"""

print(len(text))

config_path = os.path.dirname(__file__)
with open(config_path + "/config.yaml") as f:
    CONFIG = yaml.safe_load(f)
with open(config_path + CONFIG["bot"]["template"]) as f:
    template = f.read()
bot = TeleBot(CONFIG["bot"]["token"])

kbr = InlineKeyboardMarkup()
kbr.add(
    InlineKeyboardButton("ЭКОСИСТЕМА", url="https://t.me/sro_lk_bot")
)


# bot.send_message(
#     chat_id=CONFIG["bot"]["chanel"],
#     text=text,
#     parse_mode="Markdown", 
#     reply_markup=kbr
# )
bot.send_photo(
    chat_id=CONFIG["bot"]["chanel"],
    photo=open("./anons.jpg", 'rb'),
    caption=text,
    parse_mode="Markdown",
    reply_markup=kbr
)