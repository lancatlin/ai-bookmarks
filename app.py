from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import argparse

from titles import titles

from embedder import EmbeddingModel
from cluster import ClusterModel


class App:
    def __init__(self):
        self.clusterModel = ClusterModel()
        self.sentences = []
        self.embeddings = None
        self.embeddings_2d = None
        self.embeddings_3d = None
        self.n_clusters = 0
        self.cluster_labels = None

    def run(self, sentences):
        self.sentences = sentences
        embedder = EmbeddingModel()
        self.embeddings = embedder.embed(titles)

    def save(self, file_name):
        np.savez(file_name, sentences=self.sentences, embeddings=self.embeddings)

    def load(self, file_name):
        data = np.load(file_name)
        self.sentences = data["sentences"]
        self.embeddings = data["embeddings"]

    def cluster(self):
        self.n_clusters, self.cluster_labels = self.clusterModel.fit(
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

    def visualize3d(self):
        pca = PCA(n_components=3)
        self.embeddings_3d = pca.fit_transform(self.embeddings)
        print(self.embeddings_3d.shape)
        colors = plt.cm.rainbow(np.linspace(0, 1, self.n_clusters))
        print(colors)
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        for i, (x, y, z) in enumerate(self.embeddings_3d):
            ax.scatter(x, y, z, color=colors[self.cluster_labels[i]])
            ax.text(
                x + 0.01, y + 0.01, z + 0.01, self.sentences[i], fontsize=9
            )  # Adjust text position and size

        ax.set_xlabel("Component 1")
        ax.set_ylabel("Component 2")
        ax.set_zlabel("Component 3")
        plt.title("3D Visualization of Sentence Embeddings")
        plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--embedding", help="Recalculate the embedding", action="store_true"
    )
    args = parser.parse_args()
    file_name = "embeddings.npz"
    app = App()
    if args.embedding:
        app.run(titles)
        app.save(file_name)
    else:
        app.load(file_name)
    app.cluster()
    app.show()
    app.visualize3d()


if __name__ == "__main__":
    main()
