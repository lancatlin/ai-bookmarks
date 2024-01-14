from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from bookmark_manager import BookmarkManager


def get_title(documents: list[str]):
    # Create a CountVectorizer for parsing/counting words
    count_vectorizer = CountVectorizer(stop_words="english")
    doc_term_matrix = count_vectorizer.fit_transform(documents)

    # Number of topics
    n_topics = 1

    # Create and fit LDA model
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(doc_term_matrix)

    def get_topics(model, count_vectorizer, n_top_words):
        words = count_vectorizer.get_feature_names_out()
        result = []
        for topic_idx, topic in enumerate(model.components_):
            result.append(
                " ".join([words[i] for i in topic.argsort()[: -n_top_words - 1 : -1]])
            )
        return result

    # Print the topics found by the LDA model
    topics = get_topics(lda, count_vectorizer, n_top_words=5)
    return topics[0]
