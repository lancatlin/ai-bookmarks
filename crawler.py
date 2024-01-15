import gevent
from gevent import monkey

monkey.patch_all()

from bs4 import BeautifulSoup
from bookmark_manager import BookmarkManager
from bookmark import Bookmark

from parser import Parser
import requests


class Crawler:
    def __init__(self, manager: BookmarkManager):
        self.manager = manager

    def crawl(self, url):
        return "<p>Hello World!</p>"

    def parse(self, file_name: str):
        with open(file_name, "r") as file:
            document = file.read()
            soup = BeautifulSoup(document, "html.parser")
            Atags = soup.find_all("a")
            for i in Atags:
                url = i.get("href", "")
                add_date = i.get("add_date", "")
                icon = i.get("icon", "")
                bookmark = Bookmark(url, date=add_date, icon=icon)
                self.manager.add(bookmark)

    def retrieve(self):
        tasks = [
            gevent.spawn(self.retrieveBookmark, bookmark)
            for bookmark in self.manager.bookmarks
        ]
        results = gevent.joinall(tasks)
        print("Completed")

    def crawl(self, url: str, timeout=15):
        response = requests.get(url, timeout=timeout)
        response.encoding = "utf-8"
        return response.text

    def retrieveBookmark(self, bookmark: Bookmark):
        print("Accessing", bookmark.url)
        try:
            html = self.crawl(bookmark.url)
            parser = Parser(html)
            bookmark.title = parser.get_title()
            bookmark.description = parser.get_description()
        except Exception as e:
            print(f"Error fetching URL: {e}")
