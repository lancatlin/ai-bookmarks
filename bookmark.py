from parser import Parser
import requests


class Bookmark:
    def __init__(
        self,
        url,
        title="",
        description="",
        date="",
        icon="",
        cluster=-1,
        embedding=None,
    ):
        self.url = url
        self.title = title
        self.description = description
        self.date = date
        self.icon = icon
        self.embedding = embedding
        self.cluster = int(cluster)

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def crawl(self, timeout=15):
        response = requests.get(self.url, timeout=timeout)
        response.encoding = "utf-8"
        return response.text

    def retrieve(self):
        print("Accessing", self.url)
        try:
            html = self.crawl()
            parser = Parser(html)
            self.title = parser.get_title()
            self.description = parser.get_description()
            if self.title == "" or self.description == "":  # needs selenium:
                # call selenium
                # crawler.crawl(self.url)
                pass

        except Exception as e:
            print(f"Error fetching URL: {e}")

    def export(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "date": self.date,
            "icon": self.icon,
            "cluster": self.cluster,
        }

    def set_cluster(self, cluster):
        self.cluster = cluster

    def set_embedding(self, embedding):
        self.embedding = embedding
