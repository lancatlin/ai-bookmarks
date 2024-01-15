import csv
import numpy as np

from bookmark import Bookmark
from bookmark_set import BookmarkSet
from cluster_info import ClusterInfo


class BookmarkManager(BookmarkSet):
    def __init__(self):
        super().__init__()
        self.embeddings = None
        # clusters is a dictionary of cluster_id -> ClusterInfo
        self.clusters: list[ClusterInfo] = []

    def load(self, file_name):
        with open(file_name, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bookmark = Bookmark(**row)
                self.add(bookmark)

    def load_clusters(self, file_name):
        with open(file_name, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cluster = ClusterInfo(**row)
                cluster.bookmarks = [
                    bookmark
                    for bookmark in self.bookmarks
                    if bookmark.cluster == cluster.id
                ]
                self.clusters.append(cluster)

    def load_embedding(self, file_name):
        self.embeddings = np.load(file_name)

    def export(self, file_name, condition=lambda x: True):
        with open(file_name, "w") as csvfile:
            fieldnames = ["url", "title", "description", "date", "icon", "cluster"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for bookmark in self.bookmarks:
                if condition(bookmark):
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

    def set_clusters(self, cluster_labels: list[int]):
        for i, label in enumerate(cluster_labels):
            self.bookmarks[i].set_cluster(label)

    def set_cluster_info(self, clusters: list[ClusterInfo]):
        self.clusters = clusters

    def n_clusters(self):
        return len(self.clusters)
