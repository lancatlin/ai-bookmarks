from sklearn.cluster import AgglomerativeClustering

from bookmark_manager import BookmarkManager


class ClusterModel:
    def __init__(self):
        self.model = AgglomerativeClustering(n_clusters=None, distance_threshold=2)

    def fit(self, embeddings):
        self.model.fit(embeddings)
        return self.model.n_clusters_, self.model.labels_
