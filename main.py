from telebot import TeleBot 
from bs4 import BeautifulSoup
from time import sleep
import os
import sqlite3
import yaml
import requests


def process_title(item, base_url):
    item_url = base_url + item['href']
    title = f"*{item.get_text(strip=True)}*"
    return item_url, title


def process_news(url):
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
    with open("config.yaml") as f:
        CONFIG = yaml.safe_load(f)
    with open(CONFIG["bot"]["template"]) as f:
        template = f.read()

    bot = TeleBot(CONFIG["bot"]["token"])
    worker = DB_worker(CONFIG["bot"]["db"])
    
    for parser in CONFIG['parsers']:
        page = requests.get(parser["base_url"] + parser["news_path"])
        soup = BeautifulSoup(page.text, "html.parser")
        news_list = soup.findAll("div", class_="news-list__item")

        for news in news_list:
            item_url, title = process_title(
                news.find("a", class_="news-list__name"),
                parser["base_url"]
            )

            if worker.check_news(news['id']):
                continue
            elif worker.new_db:
                worker.add_news(news['id'], title)
                continue

            img = news.find("img")
            img_url = parser["base_url"] + img['src']
            sleep(0.5)
            text = process_news(item_url)
            
            if len(text) < parser["chars_limit"]:
                content = title + "\n\n" + text
            else:
                content = title
            
            post_text = template.format(
                content=content,
                url=item_url,
                other_tags=parser["tags"]
            )

            bot.send_photo(
                chat_id=CONFIG["bot"]["chanel"],
                photo=img_url,
                caption=post_text,
                parse_mode="Markdown",
            )
            worker.add_news(news['id'], title)