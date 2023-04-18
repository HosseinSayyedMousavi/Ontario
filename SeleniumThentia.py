import sqlite3
from selenium.webdriver import ChromeOptions as Options
from selenium import webdriver
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import win32gui
import json
import time
def enumWindowFunc(hwnd, windowList):
    """ win32gui.EnumWindows() callback """
    text = win32gui.GetWindowText(hwnd)
    #className = win32gui.GetClassName(hwnd)
    #print hwnd, text, className
    if  text.find('chromedriver.exe') != -1:
        windowList.append(hwnd)



browser = webdriver.Chrome('chromedriver.exe')
con = sqlite3.connect('thentiacloudFinal.db')
con2=sqlite3.connect('thentiacloudFinal2.db')
cure2=con2.cursor()

def UpdateDatabase(table):
    profiles=con.execute('select data from '+table).fetchall()

    try:
        cure2.execute("create table %s (data JSON)"%table)
        con2.commit()
    except:
        pass
    i=0
    for data in profiles:
        data = json.loads(data[0])
        try:
            browser.get("https://cvo.ca.thentiacloud.net/webs/cvo/register/#/corporation/5d07ae985420261c56a97ff4")
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(("css selector", ".cvo-profile")))
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(("tag name", "iframe")))
            browser.switch_to.frame(browser.find_element("tag name","iframe"))
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located(("xpath", "//div[@class='google-maps-link']//a")))
            link = browser.find_element("xpath", "//div[@class='google-maps-link']//a").get_attribute("href")
            Coordinates = re.findall(r"ll=([\d\.,-]*)",link)[0]
            Latitude = Coordinates.split(",")[0]
            Longitude = Coordinates.split(",")[1]
            print(Latitude,Longitude)
            data["Location"]["Latitude"] = Latitude
            data["Location"]["Longitude"] = Longitude
        except:
            pass
        finally:
            cure2.execute("insert into %s values (?)"%table,[json.dumps(data)])
            con2.commit()
            i+=1
            print(table , ":",i)

UpdateDatabase("Professional_Corporations")