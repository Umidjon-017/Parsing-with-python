import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class CrawledArticle():
    def __init__(self, title, emoji, content, image):
        self.title = title
        self.emoji = emoji
        self.content = content
        self.image = image
        
class ArticleFetcher():
    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"
        articles = []
        
        while url != "":
            print(url)
            time.sleep(0.5)
            r = requests.get(url)
            doc = BeautifulSoup(r.text, "html.parser")
            
            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text
                content = card.select_one(".card-text").text
                title = card.select(".card-title span")[1].text
                image = urljoin(url, card.select_one("img").attrs["src"])

                crawled = CrawledArticle(title, emoji, content, image)
                articles.append(crawled)
                
            next_button = doc.select_one(".navigation .btn")
            if next_button:
                next_href = next_button.attrs["href"]
                next_href = urljoin(url, next_href)
                url = next_href
            else:
                url = ""
                
        return articles


fetcher = ArticleFetcher()
for article in fetcher.fetch():
    print(article.emoji + ": " + article.title)