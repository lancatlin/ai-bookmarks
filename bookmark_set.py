from bookmark import Bookmark


class BookmarkSet:
    def __init__(self, bookmarks=[]):
        self.bookmarks: list[Bookmark] = bookmarks
        self.bookmarks_set: set[Bookmark] = set(bookmarks)

    def add(self, bookmark: Bookmark):
        if bookmark not in self.bookmarks_set:
            self.bookmarks_set.add(bookmark)
            self.bookmarks.append(bookmark)

    def get_sentences(self):
        sentences = []
        for bookmark in self.bookmarks:
            sentences.append(f"{bookmark.title} {bookmark.description}")
        return sentences
