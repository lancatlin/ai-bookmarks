class Bookmark:
    def __init__(
        self,
        url,
        title="",
        description="",
        date="",
        icon="",
        cluster=-1,
        embedding=None,
    ):
        self.url = url
        self.title = title
        self.description = description
        self.date = date
        self.icon = icon
        self.embedding = embedding
        self.cluster = int(cluster)

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def export(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "date": self.date,
            "icon": self.icon,
            "cluster": self.cluster,
        }

    def set_cluster(self, cluster):
        self.cluster = cluster

    def set_embedding(self, embedding):
        self.embedding = embedding
