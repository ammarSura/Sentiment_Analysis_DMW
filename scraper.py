from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from time import sleep


def getHotelURLs(url, driver): 
    #gets urls of all hotels from query page
    driver.get(url)
    sleep(10)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(10)

    lst = driver.find_elements(By.CSS_SELECTOR, "[data-selenium=hotel-item]")
    
    hotelURLs = []
    
    for i in range(len(lst)):
        hotelURLs.append(lst[i].find_element(By.TAG_NAME, "a").get_attribute('href'))
    
    return hotelURLs

def getReviewsURL(url, driver):
    #gets reviews url from hotel page

    driver.get(url)
    sleep(5)
    ele = False
    try:
        ele = driver.find_element(By.CSS_SELECTOR, '[data-selenium=review-basedon]')
    except:
        pass
    
    if ele:
        try:
            return ele.find_element(By.TAG_NAME, "a").get_attribute('href')
        except:
            pass
    
    return False
    
    

def getReviews(url, driver):
    # gets reviews from hotel review page

    driver.get(url)
    sleep(2)
    hotel_name = driver.find_element(By.CSS_SELECTOR, '[data-selenium=hotel-header-name]').text
    hotel_address = driver.find_element(By.CSS_SELECTOR, '[data-selenium=hotel-address-map]').text
    
    overall_rating = False
    try:
        overall_rating = driver.find_element(By.CLASS_NAME, "ReviewScore-Number ReviewScore-Number--line-height").text
    except:
        pass

    if not overall_rating:
        try:
            overall_rating = driver.find_element(By.CLASS_NAME, "Review__ReviewFormattedScore").text
        except:
            pass

    if not overall_rating:
        try:
            overall_rating = driver.find_element(By.CLASS_NAME,"Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography ").text
        except:
            pass


    more_reviews = False
    for i in range(5):
        try:
            more_reviews = driver.find_element(By.CLASS_NAME, "Review-paginator-button")
        except:
            break
        if more_reviews:
            more_reviews.click()
            sleep(3)

    reviewsHelper = driver.find_elements(By.CLASS_NAME, 'Review-comment')
    if len(reviewsHelper) < 100:
        return False

    reviews = []
    

    for i in range(100):
        title = reviewsHelper[i].find_element(By.CLASS_NAME, 'Review-comment-bodyTitle').text
        comment = reviewsHelper[i].find_element(By.CLASS_NAME, 'Review-comment-bodyText').text
        rating = reviewsHelper[i].find_element(By.CLASS_NAME, 'Review-comment-leftScore').text
        reviews.append({
            "review_rating" : rating,
            "review_title" : title,
            "review_comment" : comment 
        })

    hotel = {
            "name" : hotel_name[:-8],
            "address" : hotel_address,
            "overall_rating" : overall_rating,
            "reviews" : reviews
        }


    return hotel

def scraper(queryURL, driver):
    lst = []

    hotelsURLS = getHotelURLs(queryURL, driver)
    count = 1
    for url1 in hotelsURLS:
        url2 = getReviewsURL(url1, driver)
        if url2:
            hotel = getReviews(url2, driver)
            if hotel:
                print("Hotel", str(count) + ": ", hotel["name"])
                count = count + 1
            
                lst.append(hotel)
            if count > 20:
                break

    return lst

    
driver = webdriver.Chrome()

queryURL = input("Input Query String: ")


lst = scraper(queryURL, driver)
dic = { "hotels": lst }
json_object = json.dumps(dic, indent = 4)
  
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)


driver.close()
driver.quit()