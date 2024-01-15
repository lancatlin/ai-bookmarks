from bs4 import BeautifulSoup
from sanitizer import sanitize_output


class Parser:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    @sanitize_output
    def get_title(self):
        try:
            meta = self.soup.find("meta", {"property": "og:title"})
            if meta:
                return meta["content"]

            title = self.soup.find("title")
            if title:
                return title.text
            return ""
        except Exception as err:
            print("Error", err)
            return ""

    @sanitize_output
    def get_description(self):
        try:
            meta = self.soup.find("meta", {"property": "og:description"})
            if meta:
                return meta["content"]

            meta = self.soup.find("meta", {"name": "description"})
            if meta:
                return meta["content"]
            return ""
        except TypeError:
            return ""


if __name__ == "__main__":
    html = ""
    with open("ResNet.html", "r") as f:
        html = f.read()

    parser = Parser(html)
    print(parser.get_title())
    print(parser.get_description())
