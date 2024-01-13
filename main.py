import gevent
from gevent import monkey

monkey.patch_all()

import asyncio
import requests
from bs4 import BeautifulSoup


class BookmarkManager:
    def __init__(self):
        self.bookmarks = []

    def load(self, source):
        soup = BeautifulSoup(source, "html.parser")
        Atags = soup.find_all("a")
        for i in Atags:
            url = i.get("href", "")
            add_date = i.get("add_date", "")
            icon = i.get("icon", "")
            bookmark = Bookmarks(url, add_date, icon)
            self.bookmarks.append(bookmark)

    def retrieve(self):
        tasks = [gevent.spawn(bookmark.retrieve) for bookmark in self.bookmarks]
        results = gevent.joinall(tasks)
        for result in results:
            print("Completed access", result.value)


class Bookmarks:
    def __init__(self, url, date, icon):
        self.url = url
        self.date = date
        self.icon = icon
        self.title = ""
        self.description = ""

    def retrieve(self):
        print("Accessing", self.url)
        try:
            response = requests.get(self.url, timeout=15)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                meta = soup.find("meta", {"property": "og:title"})
                self.title = meta["content"]
                print(self.title)
            except TypeError:
                self.title = self.url
            try:
                meta = soup.find("meta", {"property": "og:description"})
                self.description = meta["content"]
                print(self.description)
            except TypeError:
                self.description = self.title
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return None


def read_html_file(path):
    with open(path, "r", encoding="cp950", errors="ignore") as file:
        return file.read()


def main():
    html_file_path = "test.html"
    html_content = read_html_file(html_file_path)
    bookmark_manager = BookmarkManager()
    bookmark_manager.load(html_content)
    bookmark_manager.retrieve()
    # test = bookmark_manager.bookmarks[0]
    # test.retrieve()


if __name__ == "__main__":
    main()
