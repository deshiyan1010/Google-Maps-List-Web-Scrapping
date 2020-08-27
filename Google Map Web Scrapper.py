import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
URL = 'https://www.google.com/search?sz=0&tbm=lcl&ei=BxsoX8n2EuGb4-EPlMeG4As&q=poultry+farms+in+tamil+nadu&oq=poultry+farms+in+tamil+nadu&gs_l=psy-ab.3..0j0i22i30k1l8j0i22i10i30k1.297610.299819.0.300936.10.10.0.0.0.0.302.1554.0j3j3j1.7.0....0...1c.1.64.psy-ab..3.7.1550....0.b6UGrj1dkPg#rlfi=hd:;si:;mv:[[12.9864692,78.49227499999999],[10.537696799999999,76.9362495]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2'

name_lst = []
cat = []
place = []
contact = []
open_close = []
rating = []

chrome_options = Options()
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
driver.get(URL)

def scrap(driver): 
    
    soup = BeautifulSoup(driver.page_source, "lxml")

    mydivs = soup.find("div",class_="rlfl__tls")  

    name = mydivs.findAll("div",attrs={"class":"dbg0pd"})
    more_info = mydivs.findAll("span",attrs={"class":"rllt__details"})

    for x,z in zip(more_info,name):
        y = x.findAll("div")
        try:

            con = y[-1].getText().split(" · ")[1]
            oc = y[-1].getText().split(" · ")[0]
            pl = y[-2].getText()
            ra = y[-3].getText().split(" · ")[0]
            ca = y[-3].getText().split(" · ")[1]
            na = z.getText()

            contact.append(con)
            open_close.append(oc)
            place.append(pl)
            rating.append(ra)
            cat.append(ca)
            name_lst.append(na)
        except:
            pass
    return driver

if __name__ == "__main__":

    while 1:
        try:        

            driver = scrap(driver)
            #driver.find_element_by_xpath("//span[text()='Next']").click()
            driver.find_element_by_xpath("//span[contains(@style, 'display:block;margin-left:53px') and text()='Next']").click()
            print("Next Page")
            print(1 if driver.current_url==URL else 0,"\n"*4)
            sleep(5)
            URL = driver.current_url
            driver.get(URL)
        except Exception as e:
            print(e)
            print(len(name_lst),len(cat),len(place),len(contact),len(open_close),len(rating))
            d = {'Name':name_lst,'Category': cat,'Place': place,'Contact': contact,'Open/Close': open_close,'Rating': rating}
            df = pd.DataFrame(data=d)
            df.to_csv("Data.csv")
            #driver.close()
            break
