from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ListProperty
import requests
import json
from kivy.clock import Clock
from random import randint
from kivy.config import Config
import webbrowser

from kivy.utils import *
 
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

url = ('https://newsapi.org/v2/everything?q=bitcoin&apiKey=857b2c2ecda74a40a2aeb94dd3436410')


def getNews():
    response = requests.get(url)
    # if status code is ok, then save in file
    # and return this response
    # else return last file
    if response.status_code == 200:
        news = response.json()
        with open('news.json', 'w') as f:
            json.dump(news, f, indent=4)
        return news

    else:
        with open('news.json', 'r') as f:
            return f.read()


class NewsList(Widget):
    news = getNews()
    iterator = NumericProperty(0)

    articles = ListProperty()
    articles = news['articles']

    max_news = NumericProperty(0)
    max_news = news['totalResults']
    if max_news > 100:
        max_news = 100

    image_url = StringProperty(' ')
    header = StringProperty(' ')
    url = StringProperty(' ')
    rgb = StringProperty('#00000')

    def update(self, dt):
        self.articles = self.news['articles']
        self.header = self.articles[self.iterator]['title']
        self.image_url = self.articles[self.iterator]['urlToImage']
        self.url = self.articles[self.iterator]['url']

    def update_news(self):
        self.news = getNews()

    def prev_news(self):
        if self.iterator == 0:
            self.iterator = 0
        else:
            self.iterator -= 1

    def next_news(self):
        print(self.iterator)
        if self.iterator == self.max_news:
            self.iterator = self.max_news
        else:
            self.iterator += 1

    def open_url_news(self):
        webbrowser.open(self.url, new=0, autoraise=True)


class NewsApp(App):
    def build(self):
        app = NewsList()
        Clock.schedule_interval(app.update, 1.0 / 60.0)
        return app


if __name__ == '__main__':
    NewsApp().run()
