
""" 
David Geng
COS 482 
Assignment 1
10/6/24
"""

#importing everything I need probably?
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

service = Service(executable_path=r"C:\Users\dav12\chromedriver-win64\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome(service=service,
                          options=options)
driver.get("https://scholar.google.com/scholar?as_ylo=2022&q=machine+learning&hl=en&as_sdt=0,20")
time.sleep(3)

#url = "https://scholar.google.com/scholar?as_ylo=2022&q=machine+learning&hl=en&as_sdt=0,20"
#response = requests.get(url)

#html = response.content

#Bsoup = BeautifulSoup(html, "lxml")

#Sets up dataframe 
dataframe = pd.DataFrame({'title': pd.Series(dtype = 'string'), 
                          'publication_info': pd.Series(dtype = 'string'),
                          'cited_by': pd.Series(dtype = 'string')})

#new_rows = [['banana', 'test', 'eh'], ['test','test','test']]

#Screen height
screen_height = driver.execute_script("return window.screen.height;")

#loop of scraping and saving to dataframe 
while True:
        try:
            #Sleep to avoid google captcha
            time.sleep(10)
            html = driver.page_source
            Bsoup = BeautifulSoup(html, "lxml")

            #Targets the tags to get the required info and then strip them 
            all_articles = Bsoup.select("#gs_res_ccl_mid div.gs_ri")
            for article in all_articles:
                title_selector = "h3.gs_rt"
                authors_venue_year_selector = "div.gs_a"
                citations_selector = article.find('a', string=lambda x: x and "Cited by" in x)
                title = article.select_one(title_selector)
                title = title.get_text()
                title = title.strip()
                authors_venue_year = article.select_one(authors_venue_year_selector)
                authors_venue_year = authors_venue_year.get_text()
                authors_venue_year = authors_venue_year.strip()
                citations = citations_selector
                citations = citations.get_text()
                citations = citations.strip()
                new_rows = [[title, authors_venue_year, citations]]

                #Adding it to the dataframe
                dataframe = pd.concat([dataframe, pd.DataFrame(new_rows, columns=['title', 'publication_info', 'cited_by'])],
                                      ignore_index=True)
            
            #Scroll and click next page
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(
                 screen_height=screen_height, i=1))
            print('Scroll')

            next_buttons = Bsoup.select(".gs_ico.gs_ico_nav_next")
            next_button = driver.find_element(By.CSS_SELECTOR, ".gs_ico.gs_ico_nav_next")
            next_button.click()
            print('Next Page!')

        except Exception as e:
            print("Error or Done")
            break

#Print and save to csv
print(dataframe)
dataframe.to_csv('ml_articles_info.csv', sep = ',')