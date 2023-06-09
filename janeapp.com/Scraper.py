import requests
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import logging
from selenium.webdriver import ChromeOptions as Options
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urlunparse
import sqlite3
import os
Response = ""
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'}

conn = sqlite3.connect('janeapp.db')
cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE janeapp (data JSON
    )''')
    conn.commit()
except:
    pass
def get_sub_and_domain(url):
    parsed_url = urlparse(url)
    subdomain = parsed_url.netloc.split(".")[0]
    domain = parsed_url.netloc.split(".")[-2] + "." + parsed_url.netloc.split(".")[-1]
    new_url = urlunparse((parsed_url.scheme, f"{subdomain}.{domain}", "", "", "", ""))
    return new_url


def clean_file_name(file_name, max_length=255):
    # Remove illegal characters
    clean_file_name = re.sub(r'[\\/*?:"<>|]', '', file_name)
    
    # Trim file name if it exceeds the maximum length for Windows
    file_name_root, file_extension = os.path.splitext(clean_file_name)
    if len(file_name_root) > max_length:
        clean_file_name = file_name_root[:max_length] + file_extension
        
    return clean_file_name


def page_type(domain):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")        
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
    browser.get(domain)
    resp = "NOT EXISTS!" 
    
    if len(browser.find_elements("css selector","div > div.discipline-container")) > 0:
        resp = "Corporation"
    if len(browser.find_elements("css selector",".nav-slide-container:not(slide)")) > 0:
        resp = "Branch"
    if len(browser.find_elements("css selector",".nav-slide-container.slide")) > 0 :
        resp = "Person"

    browser.close()
    return resp


def Corporation_Scraper(browser ,domain , i):
    Corporation={}
    Corporation["Practice Location"]=[]
    Corporation["Page Link"] = domain
    browser.get(domain)
    Corporation_Logo = f'{("000"+str(i))[-4:]}.jpg'
    try:
        logo = browser.find_element("css selector","p.logo_or_name picture image").get_attribute("src")
        response = requests.get(logo,headers=headers,timeout=5)
        with open("image/"+clean_file_name(Corporation_Logo), 'wb') as f :
            f.write(response.content)
    except:pass
    else: Corporation["Logo"] = Corporation_Logo
    BranchEls = browser.find_elements("xpath","//div[@class='discipline-container']/section[@class='row row-bordered']")
    for branchEl in BranchEls :
        branch = {}
        branch["name"] = branchEl.find_element("xpath","div[@class='col-sm-7']/h2[@class='flush-top']").text
        Blink =  branchEl.find_element("xpath","div[@class='col-sm-7']/h2[@class='flush-top']/a").get_attribute("href")
        
        try:
            PLinks = branchEl.find_elements("xpath",".//a[@class='photo']")
            branch["Persons"]=[]
            for z in range(0,len(PLinks)):
                PLinks[z] = PLinks[z].get_attribute("href")
            browser2 = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
            for PLink in PLinks:
                imagename=( "000"+str(i))[-4:]+"-B-"+branch["name"]+"-P-"
                Person = Person_Scraper(browser2,PLink,imagename)
                branch["Persons"].append(Person)
            browser2.close()
        except:
            pass
        if page_type(Blink) == "Branch":
            browser3 = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
            branch["branch"] = Branch_Scraper(browser3,Blink,i)
            browser3.close()

        Corporation["Practice Location"].append(branch)
    return Corporation


def Branch_Scraper(browser,link,i):
    browser.get(link)
    print("Branch :    " , link)
    Branch={}
    Branch["Treatment Categories"] = []
    try:WebDriverWait(browser, 10).until(EC.visibility_of_element_located(('css selector',"div.discipline-container section")))
    except:pass
    Treatment_Category_els=browser.find_elements("css selector","div.discipline-container section")
    try:logo_or_name = browser.find_element("css selector","p.logo_or_name")
    except:pass
    try:logo_link = logo_or_name.find_element("css selector","a picture img").get_attribute("src")
    except:pass
    try:Branch["Description of the Clinic"] = browser.find_element("xpath","//div[class='well']").text
    except:pass
    try:Branch["Website"]= logo_or_name.find_element("css selector","a").get_attribute("href")
    except:pass
    Branch["Name of the Treatment"] = re.findall("(\w*)\.janeapp",link)[0].strip().replace("\n","")
    try:
        Branch["Name of the Treatment"]=browser.find_element("css selector","div.page-header h1.pull-left small").text.strip().replace("\n","")
    except:pass
    try:
        Branch_Logo = f'{("000"+str(i))[-4:]+"-B-"+Branch["Name of the Treatment"]}.jpg'
        response = requests.get(logo_link,headers=headers,timeout=5)
        with open("image/"+clean_file_name(Branch_Logo), 'wb') as f :
            f.write(response.content)
    except:pass
    else: Branch["Logo"] = Branch_Logo

    try:Branch["Phone Number"]=browser.find_element("xpath","//a[contains(@href,'tel')]").text
    except: pass
    try:Branch["mail"] = browser.find_element("xpath","//a[contains(@href,'mailto')]").text
    except: pass

    k=0
    for Treatment_Category_el in Treatment_Category_els:
        k+=1
        Treatment_Category={}
        Treatment_Category["Name"] = str(k)
        try:Treatment_Category["Name"] =Treatment_Category_el.find_element("css selector","h3.discipline-name").text
        except:pass
        try:Treatment_Category["Description"] = BeautifulSoup(Treatment_Category_el.find_element("css selector","div.long").get_attribute('innerHTML'),"html.parser").text.strip()
        except:pass
        try:Treatment_els = Treatment_Category_el.find_elements("xpath",".//div[@class='expandable-scroll-container']/ul/li")
        except:pass
        Treatment_Category["Treatments"]=[]
        for treatment_el in Treatment_els:
            treatment={}
            try:treatment["name"] = treatment_el.find_element("xpath","a/strong").text
            except:pass
            try:treatment_el.find_element("xpath","a/i")
            except:treatment["Virtual/In-person"]="In-person"
            else:treatment["Virtual/In-person"]="Virtual"
            try:sub_name = treatment_el.find_element("xpath","a/small").text
            except:pass
            try:treatment["minutes"] = re.findall("\d*\s*[mM]in",sub_name)[0]
            except: pass
            try:treatment["price"] = re.findall("\$\d*",sub_name)[0]
            except: pass
            try:treatment["Doctors name"]=re.findall("ffered by(.*)",sub_name)[0].split(",")
            except:pass
            Treatment_Category["Treatments"].append(treatment)
        Treatment_Category["Book by Practitioner"]=[]
        browser2 = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
        try:
            PLinks = Treatment_Category_el.find_elements("xpath",".//a[@class='photo']")
            for z in range(0,len(PLinks)):
                PLinks[z] = PLinks[z].get_attribute("href")
            for Plink in PLinks:
                imagename=( "000"+str(i))[-4:]+"-B-"+Branch["Name of the Treatment"]+Treatment_Category["Name"]+"-P-"
                Treatment_Category["Book by Practitioner"].append(Person_Scraper(browser2,Plink,imagename))
            browser2.close()
        except:pass
        
        Branch["Treatment Categories"].append(Treatment_Category)
    try:
        Location_url = browser.find_element("xpath","//a[contains(text(), 'Directions & Map')]").get_attribute("href")
        r = requests.get(Location_url,headers=headers,timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
    except:pass

    try:Branch["Phone Number"]=soup.select_one("i.icon-phone + a").text
    except: pass
    try:Branch["mail"] = soup.select_one("i.icon-envelope + a").text
    except: pass
    try:
        Branch["Website"] = soup.select_one("address + p a").attrs["href"]
    except: pass
    try:
        Branch["Address"]={}
        element =soup.select_one("address")
        address = element.text.replace(element.select_one("div").text,"").strip()
        Branch["Address"]["Ful Address"] = address
        Branch["Address"]["City"] = address.split(",")[-3]
        Branch["Address"]["Postal Code"] = address.split(",")[-1]
        GoogleLink = soup.select_one("a[href*='maps.google']").attrs["href"]
        browser.get(GoogleLink)
        try:browser.find_element("css selector","button.VfPpkd-LgbsSe").click()
        except:pass
        soup = BeautifulSoup(browser.find_element("xpath","//head").get_attribute("innerHTML"),"html.parser")
        Coordinates = soup.select_one("meta[itemprop='image']").attrs["content"]
        Branch["Address"]["Longitude"] = re.findall(r"C([-\d\.]+)&",Coordinates)[0].strip()
        Branch["Address"]["Latitude"] = re.findall(r"center=([-\d\.]+)",Coordinates)[0].strip()
        print("Longitude:" , Branch["Address"]["Longitude"])
        print("Latitude:" , Branch["Address"]["Latitude"])
    except:pass

    return Branch


def Person_Scraper(browser,link,imgname):
    Person = {}
    Person["Page Link"] = link

    browser.get(link)
    imagexpath = "//div[@class='profile']/div[@class='thumbnail']/picture/img"
    link = browser.current_url+"/bio"
    browser.get(link)
    print("Person :    " , link)
    try:imagelink = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(('xpath',imagexpath))).get_attribute("src")
    except:pass
    try:element = browser.find_element("xpath" , "//div[@class='profile']/h2[@class='staff-name']")
    except:pass
    try:Person["Specialty/ Expertise/ Position"] = element.find_element("xpath","small").text
    except:pass
    try:Person["Name"] = element.get_attribute('textContent').strip().replace("\n","")
    except:pass
    try:Person["Name"]=Person["Name"].replace(Person["Specialty/ Expertise/ Position"], '').strip().replace("\n","")
    except:pass
    try:Person["Phone Number"]=browser.find_element("xpath","//a[contains(@href,'tel')]").text
    except: pass
    try:Person["mail"] = browser.find_element("xpath","//a[contains(@href,'mailto')]").text
    except: pass
    try:
        Person_Image = f'{imgname}{Person["Name"]}.jpg'
        response = requests.get(imagelink,headers=headers,timeout=5)
        with open("image/"+clean_file_name(Person_Image), 'wb') as f:
            f.write(response.content)
    except:pass
    else: Person["Image"] = Person_Image
    try:Person["Description"] = browser.find_element("css selector" , "div#bio").text
    except:pass
    

    Person["Treatments"]={}
    try:treatment_titles = browser.find_elements("xpath" , "//nav[@aria-labelledby='treatment_navigation']/p[@class = 'discipline-title']")
    except:pass
    j=1
    for treatment_title in treatment_titles:
        Person["Treatments"][treatment_title.text] = []
        Treatment_els = browser.find_elements("xpath" , f"//nav[@aria-labelledby='treatment_navigation']/ul[{str(j)}][contains(@class,'discipline')]/li")
        for treatment_el in Treatment_els:
            treatment={}
            try:treatment["name"] = treatment_el.find_element("xpath","a/strong").text
            except:pass
            try:treatment_el.find_element("xpath","a/i")
            except:treatment["Virtual/In-person"]="In-person"
            else:treatment["Virtual/In-person"]="Virtual"
            try:sub_name = treatment_el.find_element("xpath","a/small").text
            except:pass
            try:treatment["minutes"] = re.findall("\d*\s*[mM]in",sub_name)[0]
            except: pass
            try:treatment["price"] = re.findall("\$\d*",sub_name)[0]
            except: pass
            Person["Treatments"][treatment_title.text].append(treatment)
        j+=1
    try:
        Location_url = browser.find_element("xpath","//a[contains(text(), 'Directions & Map')]").get_attribute("href")
        r = requests.get(Location_url,headers=headers,timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
    except:pass
    
    try:Person["Phone Number"]=soup.select_one("i.icon-phone + a").text
    except: pass
    try:Person["mail"] = soup.select_one("i.icon-envelope + a").text
    except: pass
    try:
        Person["Website"] = soup.select_one("address + p a").attrs["href"]
    except: pass
    try:
        Person["Address"]={}
        element =soup.select_one("address")
        address = element.text.replace(element.select_one("div").text,"").strip()
        Person["Address"]["Ful Address"] = address
        Person["Address"]["City"] = address.split(",")[-3]
        Person["Address"]["Postal Code"] = address.split(",")[-1]
        GoogleLink = soup.select_one("a[href*='maps.google']").attrs["href"]
        browser.get(GoogleLink)
        try:browser.find_element("css selector","button.VfPpkd-LgbsSe").click()
        except:pass
        soup = BeautifulSoup(browser.find_element("xpath","//head").get_attribute("innerHTML"),"html.parser")
        Coordinates = soup.select_one("meta[itemprop='image']").attrs["content"]
        Person["Address"]["Longitude"] = re.findall(r"C([-\d\.]+)&",Coordinates)[0].strip()
        Person["Address"]["Latitude"] = re.findall(r"center=([-\d\.]+)",Coordinates)[0].strip()
        print("Longitude:" , Person["Address"]["Longitude"])
        print("Latitude:" , Person["Address"]["Latitude"])
    except:pass

    return Person

    
with open('janeapp.json') as f:
    sub_domains = json.load(f)["result"]["records"]

i=0
for sub in sub_domains:
    Data = {}
    i+=1
    domain = "https://"+sub["domain"]
    try:
        print(i,") "+sub["domain"])

        Response = page_type(domain)
        print(Response)
    except: 
        print("NOT OPENNED")
        Response="NOT OPENNED"


    if Response== "Corporation":
        browser = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
        Data = Corporation_Scraper(browser,domain, i)
        Data["Type"] = "Corporation"
    elif Response== "Branch":
        Data["Practice Location"]=[]
        browser = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
        Data["Practice Location"].append({"branch":Branch_Scraper(browser,domain, i)})
        Data["Type"] = "Branch"
        Data["Page Link"] = domain
    elif Response== "Person":
        Data["Practice Location"]=[]
        browser = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options)
        imgname = ("000"+str(i))[-4:]+"-P-"
        Data["Practice Location"].append({"Persons":[Person_Scraper(browser,domain, imgname)]})
        Data["Type"] = "Person"
        Data["Page Link"] = domain
    elif Response== "NOT OPENNED":
        Data["Type"] = "Not Openned"
        Data["Page Link"] = domain
    elif Response== "NOT EXISTS!":
        Data["Type"] = "Page Is Empty!"
        Data["Page Link"] = domain

    cursor.execute("insert into janeapp values ( ? )",[json.dumps(Data)])
    conn.commit()