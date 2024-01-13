from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from titles import titles
from embedder import EmbeddingModel
from cluster import ClusterModel


class App:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.cluster = ClusterModel()
        self.sentences = []
        self.embeddings = None
        self.embeddings_2d = None
        self.embeddings_3d = None
        self.n_clusters = 0
        self.cluster_labels = None

    def run(self, sentences):
        self.sentences = sentences
        self.embeddings = self.embedder.embed(titles)
        self.n_clusters, self.cluster_labels = self.cluster.fit(
            self.sentences, self.embeddings
        )

    def show(self):
        clustered_sentences = {}
        for sentence_id, cluster_id in enumerate(self.cluster_labels):
            if cluster_id not in clustered_sentences:
                clustered_sentences[cluster_id] = []

            clustered_sentences[cluster_id].append(self.sentences[sentence_id])

        for i, cluster in clustered_sentences.items():
            print("Cluster ", i + 1)
            print(cluster)
            print("")

    def visualize(self):
        pca = PCA(n_components=2)
        self.embeddings_2d = pca.fit_transform(self.embeddings)
        print(self.embeddings_2d.shape)
        colors = plt.cm.rainbow(np.linspace(0, 1, self.n_clusters))
        print(colors)
        plt.figure(figsize=(10, 8))
        # plt.scatter(self.embeddings_2d[:, 0], self.embeddings_2d[:, 1], alpha=0.5)
        for i, (x, y) in enumerate(self.embeddings_2d):
            plt.scatter(x, y, color=colors[self.cluster_labels[i]])
            plt.text(
                x + 0.01, y + 0.01, self.sentences[i], fontsize=9
            )  # Adjust text position and size

        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.title("2D Visualization of Sentence Embeddings")
        plt.show()


def main():
    app = App()
    app.run(titles)
    app.show()
    app.visualize()


if __name__ == "__main__":
    main()
