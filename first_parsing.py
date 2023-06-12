import requests
from bs4 import BeautifulSoup as bs

def get_books(content):
    soup = bs(content, 'html.parser')
    
    # bu yerda title, img, limk lar joylashga röyxatga kirib olinyapti
    # yoki bizga  kerakli li ni bölimiga kirish uchun qilinyapti
    ol = soup.find('ol', attrs = {'class': 'row'})
    books = ol.select('li')
    
    books_data = []
    for book in books:
        image = 'http://books.toscrape.com/catalogue/' + book.find('div', attrs = {'class': 'image_container'}).find('img')['src']
        title = book.find('h3').find('a')['title']
        price = book.find('p', attrs={'class': 'price_color'}).text
        
        books_dict = {
            'image': image,
            'title': title,
            'price': price
        }
        
        books_data.append(books_dict)
    return books_data

    def get_naxt_page(content):
    soup = bs(content, 'html.parser')
    try:
        next_page = 'http://books.toscrape.com/catalogue/'+soup.find('li', attrs={'class':'next'}).find('a')['href']
        return next_page
    except:
        pass

    final_data = []
page_number = 1
url = 'http://books.toscrape.com/catalogue/page-1.html'
get_html = requests.get(url)
if get_html.status_code == 200:
    while True:
        books = get_books(get_html.content)
        print(f"Polucheno {len(books)} s {page_number} ctranitsi")
        final_data += books
        
        next_page = get_naxt_page(get_html.content)
        if next_page:
            page_number += 1
            get_html = requests.get(next_page)
            if get_html.status_code == 200:
                print(f"Parsing boshlandi: {page_number}")
        else:
            break
print(f"Malumotlar qabul qilindi: {page_number} sahifa, {len(final_data)} ta kitob")
len(final_data)
final_data[100]