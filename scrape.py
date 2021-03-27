import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup, NavigableString, Tag
import re
from notify import create_notification
from win10toast import ToastNotifier
import webbrowser

toaster = ToastNotifier()
def get_request():
    # print(cfscrape)'
    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-fetch-site': 'none',
               'sec-fetch-mode': 'navigate',
               'sec-fetch-dest': 'document',
               'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    text = requests.get(
        'https://www.amazon.co.uk/s?k=rtx+3060&i=computers&rh=n%3A430500031%2Cp_36%3A-40000', headers=headers).text
    return text


def parse_html():
    with open('test.xml', 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
        divs = soup.findAll('div', {"data-component-type": "s-search-result"})
        for item in divs:
            try:
                atag = item.h2.a
                description = atag.text.strip()
                url = atag.get('href')
                aUrl = 'http://amazon.co.uk' + url
                name = item.find(text=re.compile('RTX 3060'))
                price_parent = item.find('span', 'a-price')
                price = price_parent.find('span', 'a-offscreen').text.strip()
                price = re.sub('£', '',price)
                # print(name,price)
                if name is not None and price is not None:
                    if float(price) < 4000:
                        def open_link():
                            webbrowser.open(aUrl)
                        def create_notification():
                            toaster.show_toast(
                            	'AMZ',
                            	name,
                            	'path/to/image/file/icon.png',
                            	duration=5,
                                callback_on_click=open_link
                            )                        
                        create_notification()
            except Exception as e:
                # print(e,e.__class__)
                pass



if __name__ == "__main__":
    # get_request()
    pass
    