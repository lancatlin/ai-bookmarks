from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

from bookmark_manager import BookmarkManager


class Visualizer:
    def __init__(self, manager: BookmarkManager):
        self.manager = manager

    def visualize(self):
        pca = PCA(n_components=2)
        self.embeddings_2d = pca.fit_transform(self.manager.embeddings)
        print(self.embeddings_2d.shape)
        cluster_labels = [
            cluster.title
            for cluster in sorted(self.manager.clusters, key=lambda x: x.id)
        ]
        print(cluster_labels)
        colors = plt.cm.rainbow(np.linspace(0, 1, self.manager.n_clusters()))
        print(colors.shape)
        plt.figure(figsize=(10, 8))
        x = self.embeddings_2d[:, 0]
        y = self.embeddings_2d[:, 1]
        color = [colors[bookmark.cluster] for bookmark in self.manager.bookmarks]
        plt.scatter(x, y, color=color)
        # for bookmark, (x, y) in zip(self.manager.bookmarks, self.embeddings_2d):
        #     color = colors[bookmark.cluster]
        #     plt.scatter(x, y, color=color)

        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.title("2D Visualization of Sentence Embeddings")

        cursor = mplcursors.cursor(hover=True)

        @cursor.connect("add")
        def on_add(sel):
            i = sel.target.index
            bookmark = self.manager.bookmarks[i]
            sel.annotation.set_text(bookmark.title)
            print(bookmark.title, bookmark.url)

        plt.show()

    def visualize3d(self):
        pca = PCA(n_components=3)
        self.embeddings_3d = pca.fit_transform(self.manager.embeddings[:100])
        print(self.embeddings_3d.shape)
        colors = plt.cm.rainbow(np.linspace(0, 1, self.manager.n_clusters()))
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
