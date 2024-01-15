import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from bookmark_manager import BookmarkManager
from cluster_info import ClusterInfo


class LDACluster:
    def __init__(self, manager: BookmarkManager, n_topics=8):
        self.manager = manager
        self.count_vectorizer = CountVectorizer(stop_words="english")
        self.doc_term_matrix = None
        self.n_topics = n_topics
        self.lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
        self.cluster_labels = None

    def fit(self):
        self.doc_term_matrix = self.count_vectorizer.fit_transform(
            self.manager.get_sentences()
        )
        self.lda.fit(self.doc_term_matrix)

    def cluster(self):
        # Transform the doc-term matrix to document-topic matrix
        doc_topic_matrix = self.lda.transform(self.doc_term_matrix)

        # Assign the cluster as the topic with the highest probability
        self.cluster_labels = np.argmax(doc_topic_matrix, axis=1)

        # Return cluster labels
        return self.cluster_labels

    def get_cluster_titles(self, n_top_words=5):
        feature_names = self.count_vectorizer.get_feature_names_out()
        cluster_titles = []
        for topic_idx, topic in enumerate(self.lda.components_):
            top_indices = topic.argsort()[-n_top_words:]
            top_words = [feature_names[i] for i in top_indices]
            title = " ".join(top_words)
            cluster_titles.append(title)
        return cluster_titles

    def get_cluster_sentences(self):
        """
        Optionally, provide a method to retrieve the sentences in each cluster.
        """
        titles = self.get_cluster_titles()
        clusters = {i: ClusterInfo(i, title=titles[i]) for i in range(self.n_topics)}
        for bookmark, label in zip(self.manager.bookmarks, self.cluster_labels):
            clusters[label].add(bookmark)
        return clusters
