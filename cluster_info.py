from bookmark_set import BookmarkSet


class ClusterInfo(BookmarkSet):
    def __init__(self, id, bookmarks=None, title="", score=0):
        super().__init__(bookmarks)
        self.id = int(id)
        self.title = title
        self.score = score

    def __str__(self):
        result = f"Cluster {self.id}: {self.title} ({self.score})"
        for bookmark in self.bookmarks[:5]:
            result += f"\n\t{bookmark.title}: {bookmark.url}"
        return result

    def __repr__(self):
        result = f"Cluster {self.id}: {self.title} ({self.score}) - {len(self.bookmarks)} bookmarks"
        return result

    def export(self):
        return {
            "id": self.id,
            "title": self.title,
            "score": self.score,
        }
