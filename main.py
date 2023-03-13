from telebot import TeleBot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
from bs4 import Comment
from time import sleep
import os
import sqlite3
import yaml
import requests


def process_title(item, base_url):
    item_url = base_url + item['href']
    title = f"*{item.get_text(strip=True)}*"
    return item_url, title


def process_news(url): # не используется
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    body_news = soup.find("div", class_="news-detail")
    elements = []
    for child in body_news.children:
        if child.name == "p":
            elements.append(child.get_text(strip=True))
        elif child.name == "ul":
            for li in child.children:
                if li.name == 'li':
                    elements.append('* ' + li.get_text(strip=True))    
    return "\n\n".join(elements)


def get_text_with_url(element, a_tags):
    for a in a_tags:
        a_text =  a.get_text(strip=False)
        if not a_text:
            continue
        if not a['href'].startswith("http"):
            a['href'] = parser["base_url"] + a['href']
        element = element.replace(
            a_text, f" [{a_text}]({a['href']}) "
        )
    return element.replace("\n", " ")

def process_preview(body):
    elements = []
    for child in body.a.div.children:
        if child.get_text(strip=True):
            
            if child.name == "p":
                links = child.find_all("a")
                text = child.get_text(strip=False).strip()
                text = text.replace('*', '\\*')
                text = get_text_with_url(text, links)
                elements.append(text)
            elif child.name == "ul":
                for li in child.children:
                    if li.name == 'li' and li.get_text(strip=True):
                        text = li.get_text(strip=False).strip()
                        text = text.replace('*', '\\*')
                        text = get_text_with_url(text, links)
                        elements.append('🔹 ' + text)
            elif child.name == "ol":
                
                index = 1 # в списке могут быть пустые абзацы 
                for li in child.children:
                    if li.name == 'li' and li.get_text(strip=True):
                        links = li.find_all("a")
                        text = li.get_text(strip=False).strip()
                        text = text.replace('*', '\\*')
                        text = get_text_with_url(text, links)
                        elements.append(f'{index}. ' + text)
                        index += 1
    return "\n\n".join(elements)
    

class DB_worker:
    table_name = "news_ids"
    def __init__(self, path):
        self.new_db = not os.path.exists(path)
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()

        if self.new_db:

            self.curs.execute(f"""
                CREATE TABLE {self.table_name} (
                    id TEXT PRIMARY KEY,
                    title TEXT
                )
            """)
            self.conn.commit()
        
    def add_news(self, news_id, news_title):
        self.curs.execute(
            f"INSERT INTO {self.table_name} (id, title) VALUES ('{news_id}', '{news_title}')"
        )
        self.conn.commit()
    
    def check_news(self, news_id):
        self.curs.execute(
            f"SELECT count(id) FROM {self.table_name} WHERE id='{news_id}'"
        )
        return bool(self.curs.fetchall()[0][0])


if __name__ == "__main__":
    config_path = os.path.dirname(__file__)
    with open(config_path + "/config.yaml") as f:
        CONFIG = yaml.safe_load(f)
    with open(config_path + CONFIG["bot"]["template"]) as f:
        template = f.read()

    bot = TeleBot(CONFIG["bot"]["token"])
    worker = DB_worker(config_path + CONFIG["bot"]["db"])
    
    for parser in CONFIG['parsers']:
        page = requests.get(parser["base_url"] + parser["news_path"])
        soup = BeautifulSoup(page.text, "html.parser")
        
        news_list = soup.findAll("div", class_="news-list__item")

        for news in news_list[:1]:
            item_url, title = process_title(
                news.find("a", class_="news-list__name"),
                parser["base_url"]
            )

            com = news.find(string=lambda text: isinstance(text, Comment))
            anons = BeautifulSoup(com, "html.parser")
            anons = process_preview(anons)

            if worker.check_news(news['id']):
                continue
            elif worker.new_db:
                worker.add_news(news['id'], title)
                continue

            img = news.find("img")
            img_url = parser["base_url"] + img['src']
            sleep(0.5)

            content = title + "\n\n" + anons

            post_text = template.format(
                content=content,
                # url=item_url,
                other_tags=parser["tags"]
            )

            kbr = InlineKeyboardMarkup()
            kbr.add(
                InlineKeyboardButton(
                    text="🌐 Читать на сайте",
                    url=item_url
                )
            )
            # print(post_text)
            if len(post_text) < 1024:
                
                bot.send_photo(
                    chat_id=CONFIG["bot"]["chanel"],
                    photo=img_url,
                    caption=post_text,
                    parse_mode="Markdown",
                    reply_markup=kbr
                )
            else:
                splited_text = post_text.split("\n")
                splited_text [-2] = f"[\u2060]({img_url})"
                post_text = "\n".join(splited_text)
                bot.send_message(
                    chat_id=CONFIG["bot"]["chanel"],
                    text=post_text,
                    parse_mode="Markdown", 
                    reply_markup=kbr
                )
            # print(post_text)
            worker.add_news(news['id'], title)
