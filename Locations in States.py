import csv

import openpyxl
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selectolax.parser import HTMLParser
from fake_useragent import UserAgent
import time

#  DECLARATION
OUTPUT_FILE_NAME = 'Location_links.csv'


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    ua = UserAgent()
    userAgent = ua.random  # THIS IS FAKE AGENT IT WILL GIVE YOU NEW AGENT EVERYTIME
    # print(userAgent)
    # add the argument and make the browser Headless.
    # chrome_options.add_argument("--headless")  # if you don't want to see the display on chrome just uncomment this
    chrome_options.add_argument(f'user-agent={userAgent}')  # useragent added
    chrome_options.add_argument("--log-level=3")  # removes error/warning/info messages displayed on the console
    chrome_options.add_argument("--disable-notifications")  # disable notifications
    chrome_options.add_argument(
        "--disable-infobars")  # disable infobars ""Chrome is being controlled by automated test software"  Although is isn't supported by Chrome anymore
    chrome_options.add_argument("start-maximized")  # will  chrome screen
    # chrome_options.add_argument('--disable-gpu')  # disable gmaximizepu (not load pictures fully)
    chrome_options.add_argument("--disable-extensions")  # will disable developer mode extensions
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)             #we have disabled pictures (so no time is wasted in loading them)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)  # you don't have to download chromedriver it will be downloaded by itself and will be saved in cache
    return driver


def RunScrapper():
    start_time = time.time()
    df = pd.read_excel('States.xlsx')
    # Access a specific column in the DataFrame
    Links = df['Links'].tolist()
    # get to the website
    count1 = 1
    for link in Links:
        count = 1
        print("*************************", count1, "*************************")
        driver.get(link)
        # Get the page source
        html_source = driver.page_source
        # Use Selectolax to parse the HTML
        root = HTMLParser(html_source)
        # Page Value Checker
        links = root.css("nav[class ='locations'] li [href*='/']")
        for link in links:
            # Remove .. from href
            link = link.attributes.get('href').replace('../', '').replace('/directory/', '')
            link = 'https://us-business.info/directory/' + link
            # Write to the file
            output_result = [link]
            write_to_file([output_result])
            print(count, "):", link)
            count += 1
        count1 += 1
        # time.sleep(0.1)
    # give time taken to execute everything
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


def write_to_file(rows):
    file = open(OUTPUT_FILE_NAME, 'a', encoding='utf-8-sig', newline="")
    writer = csv.writer(file)
    writer.writerows(rows)
    file.close()


if __name__ == '__main__':
    # Run Scraper
    driver = configure_driver()
    RunScrapper()
    # close the driver.
    # driver.close()
