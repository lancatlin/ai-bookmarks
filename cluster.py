from sklearn.cluster import AgglomerativeClustering


class ClusterModel:
    def __init__(self):
        self.model = AgglomerativeClustering(n_clusters=None, distance_threshold=1.5)

    def fit(self, sentences, embeddings):
        self.model.fit(embeddings)
        return self.model.n_clusters_, self.model.labels_
