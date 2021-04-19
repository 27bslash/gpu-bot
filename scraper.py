from bs4 import BeautifulSoup
import time
from random import uniform
from webbot import Browser
import requests
import traceback
import logging
from logs import configure_log
import json


# def parse_currys(URL, text):
#     checkout_log = logging.getLogger('checkout')
#     driver = Browser
#     start = time.perf_counter()
#     soup = BeautifulSoup(text, 'html.parser')
#     search_result = soup.find('div', {'data-component': 'product-list-view'})
#     gpu_divs = search_result.findAll('article')
#     for item in gpu_divs:
#         try:
#             name = item.find('span', {'data-product': "name"}).text
#             brand = item.find('span', {'data-product': "brand"}).text
#             price_parent = item.find('div', 'amounts')
#             try:
#                 price = price_parent.find(class_='price').text
#             except Exception:
#                 price = price_parent.find('span').text
#             with open('user_details/config.json', 'r') as f:
#                 price = float(price.strip().replace('£', ''))
#                 data = json.load(f)
#                 max_price = data['max_price']
#                 url = item.find('a')
#                 available = item.find(
#                     "li", {"data-availability": "homeDeliveryAvailable"})
#                 if available and 'PNY' not in brand and price < max_price:
#                     currys = Currys(url['href'])
#                     # currys.main()
#                     end = time.perf_counter()
#                     checkout_log.info(f"time taken: {end-start}")
#                     break
#                     # buy gpu
#         except Exception as e:
#             print('not available', '\n', traceback.format_exc())
#             checkout_log.error(f"{traceback.format_exc()}")
#             pass

def parse_currys(url, driver):
    checkout_log = logging.getLogger('checkout')
    driver.switch_to_tab(1)
    driver.new_tab(url)
    driver.switch_to_tab(2)
    start = time.perf_counter()
    soup = BeautifulSoup(driver.get_page_source(), 'html.parser')
    search_result = soup.find('div', {'data-component': 'product-list-view'})
    gpu_divs = search_result.findAll('article')
    for item in gpu_divs:
        try:
            name = item.find('span', {'data-product': "name"}).text
            brand = item.find('span', {'data-product': "brand"}).text
            price_parent = item.find('div', 'amounts')
            try:
                price = price_parent.find(class_='price').text
            except Exception:
                price = price_parent.find('span').text
            with open('user_details/config.json', 'r') as f:
                price = float(price.strip().replace('£', ''))
                data = json.load(f)
                max_price = float(data['max_price'])
                url = item.find('a')
                available = item.find(
                    "li", {"data-availability": "homeDeliveryAvailable"})
                if available and 'PNY' not in brand and price < max_price:
                    end = time.perf_counter()
                    checkout_log.info(f"products available: {len(available)} time taken: {end - start}")
                    currys = Currys(url['href'], driver)
                    currys.main()
                    break
                    # buy gpu
        except Exception as e:
            print('not available', '\n', traceback.format_exc())
            checkout_log.error(f"{traceback.format_exc()}")
            pass
    if driver.get_total_tabs() > 1:
        driver.close_current_tab()


class Currys():
    def __init__(self, url, driver):
        self.url = url
        self.product_brought = False
        self.payment_type = 'card'
        with open('user_details/config.json', 'r') as f:
            self.user_details = json.load(f)
        self.driver = driver
        self.checkout_log = logging.getLogger('checkout')
        print('log: ', self.checkout_log)

    def accept_cookies(self):
        self.driver.click(id="onetrust-accept-btn-handler")
        print('accept cookies')

    def enter_email(self, email):
        self.driver.type(email, into='email')

    def enter_pw(self, pw):
        self.driver.type(pw, into='password')
        self.driver.press(self.driver.Key.ENTER)

    def login(self):
        self.driver.go_to(
            'https://www.currys.co.uk/gbuk/s/authentication.html')
        # go to auth page
        self.accept_cookies()
        time.sleep(random_delay(0, 1))

        self.enter_email(self.user_details['currys_email'])
        time.sleep(random_delay(1, 1.5))

        self.enter_pw(self.user_details['currys_password'])
        time.sleep(random_delay(1, 1.5))

        self.enter_pw(self.user_details['currys_password'])
        self.checkout_log.info(self.driver.get_current_url())

        if 'account' in self.driver.get_current_url():
            self.driver.go_to(self.url)
            print('logged in', self.url)
            self.checkout_log.info(self.driver.get_current_url())

    def add_to_basket(self):
        time.sleep(2)
        add_to_basket_clicked = False
        for i in range(5):
            if not add_to_basket_clicked:
                try:
                    self.checkout_log.info(f"Retrys: {i+1}")
                    self.driver.click(
                        xpath="//button[data-component='add-to-basket-wrapper']/button")
                    add_to_basket_clicked = True
                    time.sleep(1)
                except Exception as e:
                    self.checkout_log.error(
                        f"add to basket error {e} {e.__class__}")
                    self.checkout_log.error(f"\n retrys: {i+1}")
            else:
                if 'basket' in self.driver.get_current_url():
                    print('bask')
                    self.driver.go_to('https://www.currys.co.uk/app/checkout')
                else:
                    try:
                        self.driver.click(text='Continue to basket')
                        if len(self.driver.errors) > 0:
                            continue
                    except Exception as e:
                        self.checkout_log.error(
                            f"continue to basket error {e} {e.__class__}")
                        self.checkout_log.error(f"\n retrys: {i+1}")
            if 'checkout' in self.driver.get_current_url():
                self.checkout_log.info('Checkout Reached')
                break

    def checkout(self):
        del_button_clicked = False
        time.sleep(5)
        self.checkout_log.info(self.driver.get_current_url())
        for i in range(10):
            try:
                self.driver.click(text='Free')
                print(self.driver.errors)
                time.sleep(1)
                if len(self.driver.errors) > 0:
                    continue
            except Exception as e:
                self.checkout_log.warning(
                    f"Cannot click button in checkout: delivery retrys: {i + 1}")
            try:
                if self.payment_type == 'paypal':
                    self.driver.click(
                        xpath='//div[@data-component="PayPalPayment"]/button')
                    time.sleep(3)
                    break
                else:
                    time.sleep(random_delay(0.5, 2))
                    self.driver.click(text='Card')
                    break
            except Exception as e:
                self.checkout_log.warning(
                    f"Cannot click button in checkout: payment retrys: {i + 1}")

    def paypal(self):
        email_entered = False
        for i in range(10):
            if not email_entered:
                try:
                    email = WebDriverWait(self.driver, 3).until(
                        EC.visibility_of_element_located((By.ID, 'email')))
                    time.sleep(random_delay(0, 1))
                    email.send_keys(self.user_details['paypal_email'])
                    email.submit()
                    time.sleep(1)
                    email_entered = True
                except Exception as e:
                    self.checkout_log.error(
                        f"paypal email error {e} {e.__class__}")
                    self.checkout_log.error(f"\n retrys: {i+1}")
            else:
                try:
                    password = WebDriverWait(self.driver, 3).until(
                        EC.visibility_of_element_located((By.ID, 'password')))
                    time.sleep(random_delay(3, 5))
                    password.send_keys(self.user_details['paypal_password'])
                    password.submit()
                    time.sleep(random_delay(2, 7))
                    print('pw entered')
                    self.product_brought = True
                    break
                except Exception as e:
                    print('retrys', i)
                    self.checkout_log.error(
                        f"paypal password error {e} {e.__class__}")
                    self.checkout_log.error(f"\n retrys: {i+1}")

        # paynow = find_button(By.ID, 'payment-submit-btn')
        # paynow.click()
        # self.product_brought = True

    def card_checkout(self):

        while 'payments' not in self.driver.get_current_url():
            time.sleep(1)

        self.driver.type(self.user_details['card_number'], id='cardNumber')
        time.sleep(random_delay(1, 4))

        self.driver.type(
            self.user_details['card_holder_name'], id='cardholderName')
        time.sleep(random_delay(1, 4))

        self.driver.type(
            self.user_details['card_expiry_month'], id='expiryMonth')
        time.sleep(random_delay(1, 4))

        self.driver.type(
            self.user_details['card_expiry_year'], id='expiryYear')
        time.sleep(random_delay(1, 4))

        self.driver.type(self.user_details['security_code'], id='securityCode')
        time.sleep(random_delay(1, 4))

        self.driver.press(self.driver.Key.ENTER)
        if 'payments' not in self.driver.get_current_url():
            self.product_brought = True
        else:
            self.checkout_log.warning(
                f"could not purchase product: {self.url}")

    def main(self):
        self.login()
        if len(self.driver.errors) > 0:
            self.checkout_log.error(f"login errors: {self.driver.errors}")
        else:
            self.checkout_log.info('logged in')
            self.add_to_basket()
        if len(self.driver.errors) > 0:
            self.checkout_log.error(
                f"add to basket errors: {self.driver.errors}")
        else:
            self.checkout_log.info('product added to basket')
            self.checkout()
        if len(self.driver.errors) > 0:
            self.checkout_log.error(f"checkout errors: {self.driver.errors}")
        else:
            self.checkout_log.info('product checked out')
            if self.payment_type == 'paypal':
                self.paypal()
                pass
            else:
                self.checkout_log.info('card checkout reached')
                self.card_checkout()
                if len(self.driver.errors) > 0:
                    self.checkout_log.error(
                        f"card checkout errors: {self.driver.errors}")
                pass
            if self.product_brought:
                self.checkout_log.info(f"product brought {self.url}")
                with open('brought_products.txt', 'w') as f:
                    f.write(self.url)
        time.sleep(10)
        self.driver.close_current_tab()


def random_delay(a, b):
    return uniform(a, b)


if __name__ == "__main__":
    parse_currys('https://www.currys.co.uk/gbuk/search-keywords/xx_xx_30343_xx_ba00013562-bv00314002/3060/1_15/price-asc/xx_xx_xx_xx_0-1-4-7-criteria.html', Browser())
    # parse_currys(
    #     'https://www.currys.co.uk/gbuk/search-keywords/xx_xx_30343_xx_ba00013562-bv00314002/3060/1_15/price-asc/xx_xx_xx_xx_0-1-4-7-criteria.html')#
    # currys.main()
    # random_delay()
    # write_details_to_file()
    # checkout()
