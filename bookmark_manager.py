import gevent
from gevent import monkey

monkey.patch_all()

from bs4 import BeautifulSoup
import csv
import numpy as np

from bookmark import Bookmark
from cluster_info import ClusterInfo


class BookmarkManager:
    def __init__(self):
        self.bookmarks: list[Bookmark] = []
        self.bookmarks_set: set[Bookmark] = set()
        self.embeddings = None
        self.clusters: list[ClusterInfo] = []

    def append(self, source):
        soup = BeautifulSoup(source, "html.parser")
        Atags = soup.find_all("a")
        for i in Atags:
            url = i.get("href", "")
            add_date = i.get("add_date", "")
            icon = i.get("icon", "")
            bookmark = Bookmark(url, date=add_date, icon=icon)
            if bookmark not in self.bookmarks_set:
                self.bookmarks_set.add(bookmark)
                self.bookmarks.append(bookmark)

    def retrieve(self):
        tasks = [gevent.spawn(bookmark.retrieve) for bookmark in self.bookmarks]
        results = gevent.joinall(tasks)
        for result in results:
            print("Completed access", result.value)

    def load(self, file_name):
        with open(file_name, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bookmark = Bookmark(**row)
                if bookmark not in self.bookmarks_set:
                    self.bookmarks_set.add(bookmark)
                    self.bookmarks.append(bookmark)

    def load_clusters(self, file_name):
        with open(file_name, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cluster = ClusterInfo(**row)
                self.clusters.append(cluster)

    def load_embedding(self, file_name):
        self.embeddings = np.load(file_name)

    def export(self, file_name):
        with open(file_name, "w") as csvfile:
            fieldnames = ["url", "title", "description", "date", "icon", "cluster"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for bookmark in self.bookmarks:
                if bookmark.title != "" and bookmark.description != "":
                    writer.writerow(bookmark.export())
            print("Done")

    def export_clusters(self, file_name):
        with open(file_name, "w") as csvfile:
            fieldnames = ["id", "title", "score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for cluster in self.clusters:
                writer.writerow(cluster.export())
            print("Done")

    def export_failed(self, file_name):
        with open(file_name, "w") as csvfile:
            fieldnames = ["url", "title", "description", "date", "icon"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for bookmark in self.bookmarks:
                if bookmark.title == "" or bookmark.description == "":
                    writer.writerow(bookmark.export())
            print("Done")

    def get_sentences(self, cluster=-1):
        sentences = []
        for bookmark in self.bookmarks:
            if cluster == -1 or bookmark.cluster == cluster:
                sentences.append(f"{bookmark.title} {bookmark.description}")
        return sentences

    def set_clusters(self, cluster_labels: list[int]):
        for i, label in enumerate(cluster_labels):
            self.bookmarks[i].set_cluster(label)

    def set_cluster_info(self, clusters: list[ClusterInfo]):
        self.clusters = clusters
