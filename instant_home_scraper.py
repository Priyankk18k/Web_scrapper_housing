from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import io
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By


def get_data(house_containers):
    amount_1 = []
    location_1 = []
    sqft_1 = []
    bhk_1 = []
    price_per_sqft_1 = []
    availability_1 = []
    for index, value in enumerate(house_containers):
        amount = value.find_all('span')[0].text
        #         amount = int(''.join(itertools.takewhile(str.isdigit, amount)))
        print(amount)
        try:
            location = value.find_all("div", class_='lst-loct stub')[0].text
        except IndexError:
            location = value.find_all("div", class_='lst-loct text-ellipsis')[0].text
        print("chl gya ", location)

        try:
            sqft = value.find_all('div', class_='lst-sub-value stub text-ellipsis')[0].text
            sqft = int("".join(itertools.takewhile(str.isdigit, sqft)))
        except IndexError:
            sqft = 'Not Known'
        try:
            bhk = value.find_all('a', class_='lst-title stub')[0].text
            bhk = int("".join(itertools.takewhile(str.isdigit, bhk)))
        except IndexError:
            bhk = value.find_all('div', class_='lst-sub-value lst-config-title text-ellipsis')[0].text
            bhk = int("".join(itertools.takewhile(str.isdigit, bhk)))
        try:
            price_per_sqft = value.find_all('div', class_='lst-sub-value stub text-ellipsis')[1].text
            price_per_sqft = price_per_sqft.split('/')[0]
        except IndexError:
            price_per_sqft = value.find_all('div', class_='lst-sub-title text-ellipsis')[1].text
            price_per_sqft = price_per_sqft.split('/')[0]
        availability = 'Available'
        amount_1.append(amount)
        location_1.append(location)
        sqft_1.append(sqft)
        bhk_1.append(bhk)
        price_per_sqft_1.append(price_per_sqft)
        availability_1.append(availability)

    data = {'Location': location_1, 'bhk': bhk_1, 'availability': availability_1, 'totat_sqft': sqft_1,
            'price_per_sqft': price_per_sqft_1, 'Total_price': amount}

    dataframe = pd.DataFrame(data)
    return dataframe

if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=r'C:\Users\Priyank\PycharmProjects\selenium\chromedriver.exe')
    driver.get("https://housing.com/in/buy/real-estate-new_delhi")
    print(driver.title)
    textField = "keyword"
    properties = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(
        '//*[@id="home-page"]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/input'))
    # city_name = input("Enter the city for which you want to search :-")
    city_name = 'delhi east'
    properties.send_keys(city_name)
    search_button = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(
        '//*[@id="home-page"]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/button'))
    search_button.click()
    time.sleep(15)
    data = driver.page_source
    html_soup = BeautifulSoup(data, 'html.parser')
    house_containers = html_soup.find_all('div', class_="lst-dtls")
    availability = 'Available'
    df = get_data(house_containers)









