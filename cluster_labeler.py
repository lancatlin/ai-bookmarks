from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from cluster_info import ClusterInfo


def get_topics(cluster: ClusterInfo, n_top_words=10):
    # Create a CountVectorizer for parsing/counting words
    count_vectorizer = CountVectorizer(stop_words="english")
    doc_term_matrix = count_vectorizer.fit_transform(cluster.get_sentences())

    # Number of topics
    n_topics = 1

    # Create and fit LDA model
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(doc_term_matrix)

    words = count_vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [words[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        topics.append(top_words)

    return topics[0]
