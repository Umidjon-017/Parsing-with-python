"""Vollständiges Code"""
import requests
from bs4 import BeautifulSoup as bs
from time import sleep

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5.30720"
    }
def get_url():
    
    # bu page dagi malumotlarni olish uchun 
    for count in range(1, 8):   
    #    sleep(3)
        url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'lxml')
        # divni ichidagi barcha malumotlar saqlanadi
        data = soup.find_all('div', class_="col-lg-4 col-md-6 mb-4")

        for info in data:
            card_url = "https://scrapingclub.com" + info.find("a")["href"]
            yield card_url

# pagedagi cardlarni ichidan töliq malumotlarni olish uchun
def array():
    for card_url in get_url():

        response = requests.get(card_url, headers=headers)
        #sleep(3)
        soup = bs(response.text, 'lxml')

        data = soup.find('div', class_="card mt-4 my-4")
        name = data.find("h3").text
        price = data.find("h4").text
        text = data.find("p", class_ = "card-text").text
        image = "https://scrapingclub.com" + data.find('img', class_="card-img-top img-fluid").get('src')
        
        yield name, price, text, image
