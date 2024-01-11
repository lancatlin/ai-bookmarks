import requests
from bs4 import BeautifulSoup

class BookmarkManager:

    def __init__(self, source):

        self.source = source

    def DataBase(self):

        soup = BeautifulSoup(self.source, 'html.parser')
        Atags = soup.find_all('a')
        result = []
        for i in Atags:
            url = i.get('href', '')
            add_date = i.get('add_date', '')
            icon = i.get('icon', '')
            bookmark = Bookmarks(url, add_date, icon)
            result.append(bookmark)
        return result

class Bookmarks:

    def __init__(self, url, date, icon):

        self.url = url
        self.date = date
        self.icon = icon
    
    def getTitle(self):
        try:
            url = "https://medium.com/@quantvc/running-debian-on-android-device-natively-73545c9b0757"
            response = requests.get(url)
            response.encoding = 'utf-8'  # Set the encoding explicitly to UTF-8
            print(response.text)
            
            soup1 = BeautifulSoup(response.text, 'html.parser')
            title = soup1.find('title')

            if title:
                # Encode the title using utf-8 and ignore any characters that can't be encoded
                title_text = title.text.encode('utf-8', 'ignore').decode('utf-8')
                return title_text
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None


    def getDescription(self):

        soup = BeautifulSoup(self.url, 'html.parser')
        description = soup.find()
        
def read_html_file(path):

    with open(path, 'r', encoding='cp950', errors = "ignore") as file:
        return file.read()
    
if __name__ == "__main__":

    html_file_path = 'test.html'
    html_content = read_html_file(html_file_path)
    bookmark_manager = BookmarkManager(html_content)
    bookmarks_list = bookmark_manager.DataBase()
    first_bookmark = bookmarks_list[0]
    first_bookmark.getTitle()