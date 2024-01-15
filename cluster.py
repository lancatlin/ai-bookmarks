from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_samples
import numpy as np

from bookmark_manager import BookmarkManager
from lda import get_title
from cluster_info import ClusterInfo


def std_dev(embeddings):
    center = np.mean(embeddings, axis=0)
    print(center.shape)
    distances = np.sqrt(((embeddings - center) ** 2).sum(axis=1))
    print(distances.shape)
    return np.std(distances)


class ClusterManager:
    def __init__(self, manager: BookmarkManager):
        self.manager = manager
        self.model = AgglomerativeClustering(n_clusters=None, distance_threshold=2)
        # self.clusterModel = ClusterModel()
        self.embeddings_2d = None
        self.embeddings_3d = None
        self.n_clusters = 0
        self.cluster_labels = None

    def fit(self, embeddings):
        self.model.fit(embeddings)
        return self.model.n_clusters_, self.model.labels_

    def cluster(self):
        self.n_clusters, self.cluster_labels = self.fit(self.manager.embeddings)
        self.manager.set_clusters(self.cluster_labels)

        clustered_bookmarks = {}
        silhouette_vals = silhouette_samples(
            self.manager.embeddings, self.cluster_labels
        )
        silhouette_result = {}
        for sentence_id, cluster_id in enumerate(self.cluster_labels):
            if cluster_id not in clustered_bookmarks:
                clustered_bookmarks[cluster_id] = []
                silhouette_result[cluster_id] = 0

            clustered_bookmarks[cluster_id].append(self.manager.bookmarks[sentence_id])
            silhouette_result[cluster_id] += silhouette_vals[sentence_id]

        clusters = []
        for i, bookmarks in clustered_bookmarks.items():
            cluster_sentences = self.manager.get_sentences(cluster=i)
            title = get_title(cluster_sentences)
            silhouette_score = silhouette_result[i] / len(bookmarks)
            clusters.append(
                ClusterInfo(i, bookmarks, title=title, score=silhouette_score)
            )

        clusters.sort(key=lambda x: x.score, reverse=True)
        self.manager.set_cluster_info(clusters)

    def show(self):
        for cluster in self.manager.clusters:
            print(cluster)
            print()
