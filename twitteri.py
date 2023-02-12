import selenium, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import json
import urllib
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from PIL import Image

driver = webdriver.Chrome()
usernames = ["marvel_updat3s","Updates4Marvel","DiscussingFilm"]
driver.get("https://twitter.com/marvel_updat3s")
#for i in usernames:
    #driver.get("https://twitter.com/{i}")
    #time.sleep(5)

data = []
image = []
tweetids = set()
time.sleep(10)
#indx=0    

    
def gettweet():
    #url=f'https://twitter.com/{i}'
    #driver.get(url)
    time.sleep(5)
    articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    i=0
    print("data fetching....")
    for article in articles:
        src = []
        #Tweet = article.find_element(By.XPATH,".//div[@data-testid='tweetText']").text
        Tweet = article.find_element_by_xpath(".//div/div/div/div[2]/div[2]/div[2]/div[1]/div").text
        imagee = article.find_element_by_xpath(".//div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/a/div/div[2]/div/img")
        src.append(imagee.get_attribute('src'))
        print(src[0])
        tweet= (Tweet)
        tweetid = ''.join(tweet)
        if tweetid not in tweetids:
            data.append(tweet)
            i=i+1
        
        driver.execute_script('window.scrollTo(0,1000)')
        #driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        print(data)
        articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
        if(i==10):
            break

        
def main():
    j=0
    while(j==0):
        #for i in usernames:
        gettweet()
        time.sleep(10)

if __name__ == '__main__':
    main()
    #print(data)
#(len(articles))

#for article in articles:
    

