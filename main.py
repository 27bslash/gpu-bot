from scraper import parse_currys
import random
import logging
from logs import configure_log
from shutdown import shutdown
import sys
from setup.setup import setup
from bs4 import BeautifulSoup
import time
import re
from pathlib import Path
from webbot import Browser
debug = False
URL = 'https://www.currys.co.uk/gbuk/search-keywords/xx_xx_30343_xx_ba00013562-bv00314002/3060/1_15/price-asc/xx_xx_xx_xx_0-1-4-7-criteria.html'
if debug:
    URL = 'https://www.currys.co.uk/gbuk/mouse-surfaces/gaming-accessories/gaming-mice/635_4807_32589_xx_ba00013728-bv00313713/1_20/price-asc/xx-criteria.html'


# def currys_stock_check():
#     scrape_log = logging.getLogger('scrape')
#     shutdown()
#     headers = {
#         'pragma': 'no-cache',
#         'cache-control': 'no-cache',
#         'dnt': '1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'sec-fetch-site': 'none',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-dest': 'document',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     }
#     file = Path('brought_products.txt')
#     if file.is_file():
#         scheduler.shutdown(wait=False)
#         scrape_log.warning('PRODUCT BROUGHT STOPPING SCRAPING')
#         return
#     time.sleep(random.uniform(0, 4))
#     strt = time.perf_counter()
#     try:
#         req = requests.get(URL, headers=headers)
#     except Exception as e:
#         scrape_log.warning(f'cannot get site {e}')
#     if req.status_code != 200:
#         scrape_log.warning(f"{req.status_code} cannot get website")
#         time.sleep(60)
#         return
#     root = fromstring(req.content)
#     if len(root.xpath("//h1[contains(text(),'3060')]")) == 0:
#         scrape_log.error(f'{req.status_code} cannot get website')
#         time.sleep(60)
#         return
#     available = root.xpath('//li[@class="available"]')
#     end = time.perf_counter()
#     if len(available) > 0:
#         scrape_log.info(
#             f"products available: {len(available)} time taken: {end - strt}")
#         parse_currys(URL, req.text)
#         return


def parse_stock_informer():
    scrape_log = logging.getLogger('scrape')
    file = Path('brought_products.txt')
    if file.is_file():
        scrape_log.warning('PRODUCT BROUGHT STOPPING SCRAPING')
        return
    soup = BeautifulSoup(driver.get_page_source(), 'html.parser')
    title = soup.findAll('td', text=re.compile("3060"))
    if len(title) == 0:
        scrape_log.error('cannot get stock checker')
        print('whoops')
    if file.is_file():
        scrape_log.warning('PRODUCT BROUGHT STOPPING SCRAPING')
        return
    for i in title:
        if 'Ti' in i.text:
            continue
        wrapper = i.parent.parent
        rows = wrapper.findAll('tr')
        for row in rows:
            try:
                img = row.find('img')
                seller = None if img == None else row.find('img')['alt']
                if seller == 'Currys':
                    cells = row.findAll(
                        'span', text=re.compile('In Stock'))
                    if len(cells) > 0:
                        scrape_log.info(f"{seller} stock found")
                        parse_currys(URL, driver)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                pass
    print(f'Heartbeat: {driver.get_current_url()}')


if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        setup()
    scrape_log = configure_log.create_log(
        'scrape', 'scrape.log', 'INFO', mode='w')
    checkout_log = configure_log.create_log(
        'checkout', 'checkout.log', 'INFO', mode='a')
    try:
        file = Path('brought_products.txt')
        if not file.is_file():
            driver = Browser()
            driver.go_to(
                'https://www.stockinformer.co.uk/checker-nvidia-geforce-rtx-3080-3070-3090')
            scrape_log.warning('Starting Gpu scraping')
            while True:
                parse_stock_informer()
                time.sleep(10)
    except Exception as e:
        print(e, e.__class__)
