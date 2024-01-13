from bookmark_manager import BookmarkManager


def read_html_file(path):
    with open(path, "r", encoding="cp950", errors="ignore") as file:
        return file.read()


def main():
    # html_file_path = "bookmarks_12_30_23.html"
    html_file_path = "test.html"
    html_content = read_html_file(html_file_path)
    bookmark_manager = BookmarkManager()
    bookmark_manager.load(html_content)
    bookmark_manager.retrieve()
    # test = bookmark_manager.bookmarks[0]
    # test.retrieve()
    bookmark_manager.export("bookmarks_test.csv")
    # bookmark_manager.export_failed("bookmarks_failed.csv")


if __name__ == "__main__":
    main()
