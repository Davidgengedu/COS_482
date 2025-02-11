"""
David Geng
COS 482
12/20/2024
Final Project: Scraper
"""
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

#Setting path for chromedriver and setup for driver
chromedriver_path = r"C:\Users\dav12\Desktop\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
options = Options()
service = Service(executable_path=chromedriver_path)
drive = webdriver.Chrome(service=service, options=options)

#Function to find all reviews from html page
def get_revis(pagehtml: str):
    soup = BeautifulSoup(pagehtml, "lxml")
    reviews = soup.find_all("div", {"class": "a-section celwidget"})
    return reviews

#Function to get the details of the review
def get_details(soup_ob: BeautifulSoup):
    try:
        review_text = soup_ob.find("span", {"class": "a-size-base review-text review-text-content"}).get_text(strip=True)
        date = soup_ob.find("span", {"class": "review-date"}).get_text(strip=True)
        stars = soup_ob.find("span", {"class": "a-icon-alt"}).get_text(strip=True)
        word_count = len(review_text.split())
        return {
            "Text": review_text,
            "Location/Date": date,
            "Stars": stars,
            "Word Count": word_count
        }
    except AttributeError:
        return None  


# Main function to scrape all reviews
def scrape(driver, url):
    all_results = []

    #Dealing with Captcha
    Captchalog = True 

    while True:
        driver.get(url)
        if Captchalog:
            sleep(40)  # Captcha solving and logining into Amazon account
            Captchalog = False
        else:
            sleep(10)  # Delay to look less bot like

        html = driver.page_source
        reviews = get_revis(html)

        # Get details for each review and append to the results list
        for review in reviews:
            details = get_details(review)
            if details:
                all_results.append(details)

        try:
            # Find and click next button
            next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
            next_url = next_button.get_attribute("href")  
            if next_url:
                url = next_url  
                next_button.click()  
            else:
                break  
        except Exception as e:
            print("Error:", e)
            break

    return all_results


# Main section
if __name__ == "__main__":
    #List of links 
    #https://www.amazon.com/Kraft-Original-Macaroni-Microwaveable-Packets/product-reviews/B005ECO3H0/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/Kraft-Deluxe-Cheddar-Macaroni-Cheese/product-reviews/B00X6Y5UH0/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/Kraft-Macaroni-Cheese-Dinner-Cartoon/product-reviews/B00DVXV00W/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=
    #https://www.amazon.com/Amazon-vibrant-helpful-routines-Charcoal/product-reviews/B09B8V1LZ3/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/All-new-Echo-Show-5/product-reviews/B09B2SBHQK/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/All-New-release-Designed-parental-controls/product-reviews/B09B9CD1YB/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/Crest-Professional-Whitestrips-Whitening-Treatments/product-reviews/B00AHAWWO0/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/Crest-White-Luminous-Whitening-Toothpaste/product-reviews/B09F8FZ18G/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    #https://www.amazon.com/Crest-Protection-Toothpaste-children-toddlers/product-reviews/B07ZK1573S/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1
    amazon_url = "https://www.amazon.com/WAG-Treats-Chicken-Waffle-Bites/product-reviews/B07V7G181F/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
    all_reviews = scrape(drive, amazon_url)

    results_df = pd.DataFrame(all_reviews)
    results_df.to_csv("AmazonReviewsDog.csv", index=False)
    drive.quit()
