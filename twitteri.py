#requred libraries ~
import selenium, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import io
import json
import urllib
import pymongo
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from PIL import Image
from mongoengine import connect,Document,fields

#connection code ~
driver = webdriver.Chrome()
usernames = ["marvel_updat3s","Updates4Marvel","DiscussingFilm"]
driver.get("https://twitter.com/marvel_updat3s")
connect( db='db-name', username='user', password='pass', host='mongodb+srv://ForeverKnight:Captainjay32@cluster0.au5htbm.mongodb.net/?retryWrites=true&w=majority')

#initialized sets and arrays ~
data = []
image = []
tweetids = set()
time.sleep(10)
sarc=[]
fl=[]
cmparr= set()
lnkcomparr = set()
#if not made global it gives assignment error ~
i=0


#image downloader ~
def download_image(url, file_name):
    download_path = "imagis/"
    image_content = requests.get(url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    file_path = download_path + file_name

    with open(file_path, "wb") as file:
        image.save(file, "JPEG")

#databse model as class ~
class post(Document):
    meta = { "collection" : "post"}
    post_text = fields.StringField()
    choice = fields.StringField()
    img_url = fields.StringField()
    file_name = fields.StringField()
    file_loc = fields.StringField()
    #post_img= fields.ImageField()
    #post_status = fields.StringField()

#database incrementar ~
def uploaddata(i_new,tweet_new):
    samvar = sarc[i_new]
    filennm = samvar[28:43]
    post_pointer = post(post_text=tweet_new)
    post_pointer.choice = "nposted"
    post_pointer.file_name = filennm
    post_pointer.file_loc = "imagis/" + filennm + ".jpg"
    post_pointer.img_url = samvar
    post_pointer.save()
    #p_img = open("imagis/" + filennm + ".jpg",'rb')
    #post_pointer.post_img.put(p_img,filename=filennm + ".jpg")

#compares length of both array to avoid out of range errors ~
def compre():
    img_list = len(sarc)
    txt_list = len(data)
    if(img_list>txt_list):
        len_list = txt_list
    else:
        len_list = img_list
    return len_list

#post scraper ~
def gettweet():
    #(saved for later)url=f'https://twitter.com/{i}'
    #(saved for later)driver.get(url)
    time.sleep(5)

    #if not made global it gives assignment error ~
    global i
    articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    imagee = driver.find_elements(By.XPATH,"//img[@alt='Image']")
    for imag in imagee:
        if imag not in sarc:
            sarc.append(imag.get_attribute('src'))
            cutc = imag.get_attribute('src')
            cut = cutc[28:43]
            fl.append(cut)
            #download_image(cutc,cut + ".jpg ")
            #driver.execute_script('window.scrollTo(0,1000)')

    print("data fetching....")
    for article in articles:
        #(alternative)Tweet = article.find_element(By.XPATH,".//div[@data-testid='tweetText']").text
        #/div/div/div[2]/div[2]/div[2]/div
        sweet = article.find_element_by_xpath(".//div/div/div[2]/div[2]/div[2]/div")
        Tweet = sweet.text
        #(alternative)imagee = article.find_element(by=By.XPATH,value="//div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/a/div/div[2]/div/img").get_attribute('src') or article.find_element(by=By.XPATH,value="//div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/a/div/div[2]/div/img").get_attribute('data-src')  #//img[@alt='Image'])
        tweet= (Tweet)   
        tweetid = ''.join(tweet)
        if tweetid not in tweetids:
            if(i!=0):
                data.append(Tweet)
            #uploaddata(i,tweet)
            print(sarc)
            i=i+1
        
        driver.execute_script('window.scrollTo(0,1000)')
        #driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        print(data)
        #manual updater coz selenium sugs ~
        articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
        if(i==10):
            break

#main function ~        
def main():
    apnd=0
    j=0
    while(j==0):
        #(saved for later) for i in usernames:
        gettweet()
        getcmp=compre()
        for g in range(apnd,getcmp):
            if fl[g] not in lnkcomparr:
                if data[g] not in cmparr:
                    uploaddata(g,data[g])
                    cmparr.add(data[g])
                    lnkcomparr.add(fl[g])
                    apnd=apnd+1
        time.sleep(10)

#main func caller ~
if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb+srv://ForeverKnight:Captainjay32@cluster0.au5htbm.mongodb.net/?retryWrites=true&w=majority")
    db = client['jay']
    collection = db['post']
    main()

