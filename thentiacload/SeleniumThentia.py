import sqlite3
from selenium import webdriver
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.webdriver import FirefoxOptions                                                                                                                                                   
opts = FirefoxOptions()                                                                             
opts.add_argument("--headless")                                                                     


con = sqlite3.connect('thentiacloudFinal.db')
con2=sqlite3.connect('thentiacloudFinal2.db')
cure2=con2.cursor()

def UpdateDatabase(table):
    browser = webdriver.Firefox(options=opts)
    profiles=con.execute('select data from '+table).fetchall()

    try:
        cure2.execute("create table %s (data JSON)"%table)
        con2.commit()
    except:
        pass
    i=0
    for data in profiles:
        data = json.loads(data[0])
        Latitude = ""
        Longitude = ""
        try:
            browser.get(data["Page URL"])
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(("css selector", ".cvo-profile")))
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(browser, 5).until(EC.visibility_of_element_located(("tag name", "iframe")))
            browser.switch_to.frame(browser.find_element("tag name","iframe"))
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located(("xpath", "//div[@class='google-maps-link']//a")))
            link = browser.find_element("xpath", "//div[@class='google-maps-link']//a").get_attribute("href")
            Coordinates = re.findall(r"ll=([\d\.,-]*)",link)[0]
            Latitude = Coordinates.split(",")[0]
            Longitude = Coordinates.split(",")[1]
            data["Location"]["Latitude"] = Latitude
            data["Location"]["Longitude"] = Longitude
        except:
            pass
        finally:
            cure2.execute("insert into %s values (?)"%table,[json.dumps(data)])
            con2.commit()
            i+=1
            print(table , ":",i)
            print(Latitude,Longitude)


# UpdateDatabase("Veterinarians")
# UpdateDatabase("Veterinary_Practices")
UpdateDatabase("Professional_Corporations")