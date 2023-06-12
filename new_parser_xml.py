"""Vollständiges Code"""
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import xlsxwriter
from scraping import array

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5.30720"
    }

def download(url):
    reps = requests.get(url, stream=True)
    r = open(r"D:\Python-darslar\programm doks\Parsing\dayfuku" + url.split("/")[-1], "wb")
    for value in reps.iter_content(1024*1023):
        r.write(value)
    r.close()

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
        download(image)
        yield name, price, text, image



def writer(parameter):
    book = xlsxwriter.Workbook(r"D:\Python-darslar\programm doks\Parsing\data.xlsx")
    page = book.add_worksheet("Товар")


    row = 0 # row = строка
    column = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 50)
    page.set_column("D:D", 50)


    for item in parameter():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        page.write(row, column+3, item[3])
        row += 1

    book.close()

writer(array)

