from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def foo(driver):
    driver.get('https://www.agoda.com/en-in/')
    sleep(5)

    search = driver.find_element_by_css_selector("[data-selenium=textInput]")
    search.send_keys('Bangkok')
    search.send_keys(Keys.RETURN)
    sleep(5)
    driver.find_element_by_class_name("ab-close-button").click()
    sleep(5)
    searchButton = driver.find_element_by_css_selector("[data-selenium=searchButton]")
    # searchButton.click()

def getHotelURLs(url, driver): 
    driver.get(url)
    sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    lst = driver.find_elements_by_css_selector("[data-selenium=hotel-item]")

    hotelURLs = []

    for i in lst:
        hotelURLs.append(i.find_element_by_tag_name("a").get_attribute('href'))
    
    return hotelURLs

def getRatings(url, driver):

    driver.get(url)
    
    return driver.find_element_by_class_name('Review__ReviewFormattedScore').text

def getReviews(url, driver):

    driver.get(url)
    sleep(2)
    more_reviews = driver.find_element_by_class_name('Review-paginator-button')
    more_reviews.click()
    sleep(3)

    reviewsHelper = driver.find_elements_by_class_name('Review-comment')
    reviews = []

    for review in reviewsHelper:
        title = review.find_element_by_class_name('Review-comment-bodyTitle').text
        comment = review.find_element_by_class_name('Review-comment-bodyText').text
        rating = review.find_element_by_class_name('Review-comment-leftScore').text
        reviews.append((rating, title, comment))
        # print(title, comment)

    print(len(reviews), reviews[0])
    


driver = webdriver.Chrome()

queryURL = "https://www.agoda.com/en-in/search?checkin=2022-05-03&los=1&city=9395&adults=2&children=0&rooms=1&cid=1891461&tag=3cda3586-9ec8-88d2-2819-7b1e8bb3ad04"

eghotelURL = "https://www.agoda.com/en-in/grande-centre-point-hotel-ratchadamri/hotel/bangkok-th.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1891461&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2022-05-3&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=-1&showReviewSubmissionEntry=false&currencyCode=INR&isFreeOccSearch=false&tag=3cda3586-9ec8-88d2-2819-7b1e8bb3ad04&flexibleDateSearchCriteria=[object%20Object]&isCityHaveAsq=true&tspTypes=-1,-1&los=1&searchrequestid=26b91b3b-2cb1-4c62-a600-7fa28aa08f0f"

eghotelRatingURL = "https://www.agoda.com/en-in/grande-centre-point-hotel-ratchadamri-sha-extra-plus/reviews/bangkok-th.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1891461&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2022-05-3&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=-1&showReviewSubmissionEntry=false&currencyCode=INR&isFreeOccSearch=false&tag=3cda3586-9ec8-88d2-2819-7b1e8bb3ad04&flexibleDateSearchCriteria=%5bobject%2520Object%5d&isCityHaveAsq=true&tspTypes=-1%2c-1&los=1&searchrequestid=26b91b3b-2cb1-4c62-a600-7fa28aa08f0f"

getReviews(eghotelRatingURL, driver)

driver.close()
driver.quit()