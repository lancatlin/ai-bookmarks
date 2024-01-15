from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_samples
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from bookmark_manager import BookmarkManager
from cluster_info import ClusterInfo
from embedder import Embedder
from cluster_labeler import get_topics


def std_dev(embeddings):
    center = np.mean(embeddings, axis=0)
    print(center.shape)
    distances = np.sqrt(((embeddings - center) ** 2).sum(axis=1))
    print(distances.shape)
    return np.std(distances)


class ClusterManager:
    def __init__(self, manager: BookmarkManager, embedder: Embedder):
        self.manager = manager
        self.embedder = embedder
        self.model = AgglomerativeClustering(n_clusters=None, distance_threshold=2)
        self.n_clusters = 0
        self.cluster_labels = None

    def cluster(self):
        self.n_clusters, self.cluster_labels = self.fit(self.manager.embeddings)
        self.manager.set_clusters(self.cluster_labels)

        clustered_bookmarks = self.cluster_bookmarks()
        silhouette_scores = self.silhouette_scores()

        clusters = []
        for i, bookmarks in clustered_bookmarks.items():
            score = silhouette_scores[i]
            cluster = ClusterInfo(i, bookmarks, score=score)
            cluster.title = self.select_title(cluster)
            clusters.append(cluster)

        clusters.sort(key=lambda x: x.score, reverse=True)
        self.manager.set_cluster_info(clusters)

    def fit(self, embeddings):
        self.model.fit(embeddings)
        return self.model.n_clusters_, self.model.labels_

    def cluster_bookmarks(self):
        clustered_bookmarks = {i: [] for i in range(self.n_clusters)}
        for sentence_id, cluster_id in enumerate(self.cluster_labels):
            clustered_bookmarks[cluster_id].append(self.manager.bookmarks[sentence_id])
        return clustered_bookmarks

    def silhouette_scores(self):
        silhouette_vals = silhouette_samples(
            self.manager.embeddings, self.cluster_labels
        )
        silhouette_result = {i: 0 for i in range(self.n_clusters)}
        silhouette_counts = {i: 0 for i in range(self.n_clusters)}
        for sentence_id, cluster_id in enumerate(self.cluster_labels):
            silhouette_result[cluster_id] += silhouette_vals[sentence_id]
            silhouette_counts[cluster_id] += 1

        for cluster_id in silhouette_result:
            silhouette_result[cluster_id] /= silhouette_counts[cluster_id]
        return silhouette_result

    def show(self):
        for cluster in self.manager.clusters:
            print(cluster)
            print()

    def select_title(self, cluster: ClusterInfo):
        topics = get_topics(cluster)
        print("topics", topics)
        vectors = self.manager.embeddings[self.cluster_labels == cluster.id]
        mean = np.mean(vectors, axis=0)
        topic_vectors = self.embedder.embed(topics)
        similarities = cosine_similarity([mean], topic_vectors)[0]
        closest_topic = np.argmax(similarities)
        return topics[closest_topic]
