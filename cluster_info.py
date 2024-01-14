class ClusterInfo:
    def __init__(self, id, bookmarks=[], title="", score=0):
        self.id = id
        self.bookmarks: list[Bookmark] = bookmarks
        self.title = title
        self.score = score

    def __str__(self):
        result = f"Cluster {self.id}: {self.title} ({self.score})"
        for bookmark in self.bookmarks:
            result += f"\n\t{bookmark.title}: {bookmark.url}"
        return result

    def export(self):
        return {
            "id": self.id,
            "title": self.title,
            "score": self.score,
        }
