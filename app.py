from multiprocessing import Process
from time import sleep
from flask import Flask,jsonify
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
# from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from screeninfo import get_monitors
import pygetwindow as gw
import pandas as pd
import re
from config import BASE_URL
from config import KEY_WORDS
from dotenv import load_dotenv
import os
import pymongo
import pyautogui
# from flask_cors import CORS
load_dotenv()
app = Flask(__name__)


def _extracted_from_startScraping_8(chrome_options):
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    ads_collection=client.ads_database.ads
    shopping_collection=client.ads_database.shopping
    
    count=0
    try:
        while True:
            # pyautogui.press('win')  # Press the Windows key to open the Start menu
            # sleep(1)
            # pyautogui.typewrite('Astrill')  # Type the name of the Astrill VPN application
            # sleep(1)
            # pyautogui.press('enter') 
            # sleep(1)
            # astrill_window=gw.getActiveWindow()
            # astrill_window.moveTo(0,0)
            # sleep(1)
            # pyautogui.click(x=200,y=150)
            # for i in range(count):
            #     pyautogui.press("down")
            # sleep(1)
            # pyautogui.press("enter")
            # pyautogui.click(x=120,y=100)
            # sleep(15)
            # pyautogui.click(x=230,y=10)

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=chrome_options,
            )
            for i in range(len(KEY_WORDS)):
                driver.get(f"{BASE_URL}{KEY_WORDS[i]}")
                actions=ActionChains(driver)
                try:
                    accept_button=driver.find_element(By.CSS_SELECTOR,"button[class=\'tHlp8d\']")
                    actions.move_to_element(accept_button).click().perform()
                except Exception as e:
                    sleep(0.01)
                while True:
                    driver.execute_script("window.scrollBy(0, 100)")
                    sleep(1)
                    more_element=None
                    final_element=None
                    try:
                        more_element=driver.find_element(By.CSS_SELECTOR,"span[class=\'RVQdVd\']")
                    except Exception as e:
                        sleep(0.01)
                    if more_element:
                        actions.move_to_element(more_element)
                        sleep(1)
                        actions.click().perform()
                    try:
                        final_element=driver.find_element(By.CSS_SELECTOR, "div[class=\'card-section\']")
                    except Exception as e:
                        sleep(0.01)
                    if final_element:
                        break
                print("successfully loaded")
                shopping_cards=driver.find_elements(By.CSS_SELECTOR,"div[class=\'pla-unit-container\']")
                shopping_datas=[]
                if shopping_cards:
                    for card in shopping_cards:
                        summary=""
                        price=""
                        manufacturer=""
                        image_url=""
                        try:
                            summary=card.find_element(By.CSS_SELECTOR, "span[class=\'pymv4e\']").text
                        except Exception as e:
                            print("there is no summary")
                        try:
                            price=card.find_element(By.CSS_SELECTOR,"div[class=\'T4OwTb\']").find_element(By.TAG_NAME,"span").text
                        except Exception as e:
                            print("There is no price")
                        try:
                            manufacturer=card.find_element(By.CSS_SELECTOR,"div[class=\'LbUacb\']").find_element(By.TAG_NAME,"span").text
                        except Exception as e:
                            print("There is no manufacturer")
                        try:
                            image_url=card.find_element(By.CSS_SELECTOR,"div[class=\'Gor6zc\']").find_element(By.TAG_NAME,"img").get_attribute("src")
                        except Exception as e:
                            print("there is no image url")
                        shopping_datas.append({"summary":summary,"price":price,"manufacturer":manufacturer,"img_url":image_url})
                        print("data appended")
                else:
                    shopping_datas="No advertisments"
                    print("there is no data")
                try:
                    location=driver.find_element(By.CSS_SELECTOR,"div[class=\'eKPi4\']").find_element(By.CSS_SELECTOR,"span[class=\'BBwThe\']").text
                except Exception as e:
                    location=driver.find_element(By.ID,"oFNiHe").find_element(By.CSS_SELECTOR,"span[class=\'BBwThe\']").text
                shopping_collection.insert_one({"brand":KEY_WORDS[i], "device":"desktop", "location":location,"data":shopping_datas})
                ads_cards=driver.find_elements(By.CSS_SELECTOR,"div[class=\'uEierd\']")
                ads_datas=[]
                if ads_cards:
                    for card in ads_cards:
                        summary=""
                        site_url=""
                        title=""
                        ads=[]
                        try:
                            #summary=card.find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"div").find_elements(By.TAG_NAME,"div")[1].find_element(By.TAG_NAME,"div").text
                            summary=card.find_element(By.CSS_SELECTOR,"div.Va3FIb.r025kc.lVm3ye").text
                        except Exception as e:
                            print("There is no summary")
                            
                        try:
                            title=card.find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"div").find_elements(By.TAG_NAME,"div")[0].find_element(By.TAG_NAME,"a").text
                        except Exception as e:
                            print("There is no title")
                        try:
                            #site_url=card.find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"div").find_elements(By.TAG_NAME,"div")[0].find_element(By.TAG_NAME,"a").find_elements(By.TAG_NAME,"div")[1].find_elements(By.TAG_NAME,"span")[0].find_elements(By.TAG_NAME,"span")[1].find_elements(By.TAG_NAME,"span")[1].find_element(By.TAG_NAME,"span").text
                            site_url=card.find_element(By.CSS_SELECTOR,"span.x2VHCd.OSrXXb.ob9lvb").text
                        except Exception as e:
                            print("There is no site_url")
                        try:
                            ads_elements=card.find_elements(By.CSS_SELECTOR, "div[class=\'MhgNwc\']")
                            for ads_element in ads_elements:
                                sub_title=ads_element.find_element(By.TAG_NAME,"h3").text
                                content=ads_element.find_elements(By.TAG_NAME,"div")[-1].text
                                ads.append({"title":sub_title,"content":content})
                        except Exception as e:
                            print("there is no advertisement")
                            ads="No advertisement"
                        ads_datas.append({"summary":summary,"site_url":site_url,"title":title,"ads":ads})
                        print("data appended")
                else:
                    ads_datas="No advertisments"
                    print("there is no data")
                ads_collection.insert_one({"brand":KEY_WORDS[i], "device":"desktop", "location":location,"data":ads_datas})
            count+=1
            if count == 120:
                break
            # pyautogui.press('win')  # Press the Windows key to open the Start menu
            # sleep(1)
            # pyautogui.typewrite('Astrill')  # Type the name of the Astrill VPN application
            # sleep(1)
            # pyautogui.press('enter') 
            # sleep(1)
            # astrill_window=gw.getActiveWindow()
            # astrill_window.moveTo(0,0)
            # sleep(1)
            # pyautogui.click(x=120,y=100)
            driver.close()
            sleep(15)
    except Exception as e:
        print(e)
#Configure the driver options
options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--force-dark-mode")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--proxy-server=181.215.184.42:50100')
chrome_options.add_argument('--proxy-username=denisharsch')
chrome_options.add_argument('--proxy-password=BfGRoAqfug')
try:
    _extracted_from_startScraping_8(chrome_options)
except Exception as e:
        print(e)
