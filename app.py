from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples
import numpy as np
import matplotlib.pyplot as plt
import argparse

from titles import titles

from cluster import ClusterModel
from bookmark_manager import BookmarkManager
from lda import get_title


def std_dev(embeddings):
    center = np.mean(embeddings, axis=0)
    print(center.shape)
    distances = np.sqrt(((embeddings - center) ** 2).sum(axis=1))
    print(distances.shape)
    return np.std(distances)


class App:
    def __init__(self, manager: BookmarkManager):
        self.manager = manager
        self.clusterModel = ClusterModel()
        self.embeddings_2d = None
        self.embeddings_3d = None
        self.n_clusters = 0
        self.cluster_labels = None

    def cluster(self):
        self.n_clusters, self.cluster_labels = self.clusterModel.fit(
            self.manager.embeddings
        )
        self.manager.set_cluster(self.cluster_labels)

    def show(self):
        clustered_sentences = {}
        clustered_embeddings = {}
        silhouette_vals = silhouette_samples(
            self.manager.embeddings, self.cluster_labels
        )
        silhouette_result = {}
        for sentence_id, cluster_id in enumerate(self.cluster_labels):
            if cluster_id not in clustered_sentences:
                clustered_sentences[cluster_id] = []
                clustered_embeddings[cluster_id] = []
                silhouette_result[cluster_id] = 0

            clustered_sentences[cluster_id].append(
                self.manager.bookmarks[sentence_id].title
            )
            clustered_embeddings[cluster_id].append(
                self.manager.embeddings[sentence_id]
            )
            silhouette_result[cluster_id] += silhouette_vals[sentence_id]

        for i, cluster in clustered_sentences.items():
            cluster_sentences = self.manager.get_sentences(cluster=i)
            title = get_title(cluster_sentences)
            print(
                f"Cluster {i} {title}: std: {std_dev(clustered_embeddings[i])}, silhouette: {silhouette_result[i] / len(cluster)}"
            )
            print(cluster)
            print("")

    def visualize(self):
        pca = PCA(n_components=2)
        self.embeddings_2d = pca.fit_transform(self.manager.embeddings)
        print(self.embeddings_2d.shape)
        colors = plt.cm.rainbow(np.linspace(0, 1, self.n_clusters))
        print(colors)
        plt.figure(figsize=(10, 8))
        # plt.scatter(self.embeddings_2d[:, 0], self.embeddings_2d[:, 1], alpha=0.5)
        for i, (x, y) in enumerate(self.embeddings_2d):
            plt.scatter(x, y, color=colors[self.cluster_labels[i]])
            # plt.text(
            #     x + 0.01, y + 0.01, self.manager.bookmarks[i].title, fontsize=9
            # )  # Adjust text position and size

        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.title("2D Visualization of Sentence Embeddings")
        plt.show()

    def visualize3d(self):
        pca = PCA(n_components=3)
        self.embeddings_3d = pca.fit_transform(self.manager.embeddings[:100])
        print(self.embeddings_3d.shape)
        colors = plt.cm.rainbow(np.linspace(0, 1, self.n_clusters))
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        for i, (x, y, z) in enumerate(self.embeddings_3d):
            ax.scatter(x, y, z, color=colors[self.cluster_labels[i]])
            # ax.text(
            #     x + 0.01, y + 0.01, z + 0.01, self.sentences[i], fontsize=9
            # )  # Adjust text position and size

        ax.set_xlabel("Component 1")
        ax.set_ylabel("Component 2")
        ax.set_zlabel("Component 3")
        plt.title("3D Visualization of Sentence Embeddings")
        plt.show()


if __name__ == "__main__":
    manager = BookmarkManager()
    manager.load("bookmarks_test.csv")
    manager.load_embedding("embeddings.npy")

    app = App(manager)
    app.cluster()
    manager.export("bookmarks_cluster3.csv")
    app.show()
    # app.visualize3d()
