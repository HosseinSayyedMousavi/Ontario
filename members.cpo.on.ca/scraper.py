from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sqlite3
import json
# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('member_cpo.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE Member_List (
                    data JSON
    )''')
    conn.commit()
except:
    pass
maxtry = 4
browser = webdriver.Chrome("chromedriver.exe")
browser.get("https://members.cpo.on.ca/public_register/create?city=&first_name=&last_name=&page=1&per_page=50&postal=&tab=mem")
numberOfPages = int(browser.find_elements("xpath" , "//div[@id='tab1']/div[@class='pagination']/a[@href]")[-2].text)
j=0
i=1
while i < numberOfPages:
    try:
        url = f"https://members.cpo.on.ca/public_register/create?city=&first_name=&last_name=&page={str(i)}&per_page=50&postal=&tab=mem"
        browser.get(url)
        Waiter = WebDriverWait(browser, 20)
        Waiter.until(EC.visibility_of_element_located(("xpath" , "//div[@id='tab1']//td[1][@class='alignTop' and @style='vertical-align: top']/a[@class='teal-color']")))
    except:
        print("Error1")
    else:
        i+=1
        profiles = browser.find_elements("xpath" , "//div[@id='tab1']//td[1][@class='alignTop' and @style='vertical-align: top']/a[@class='teal-color']")
        profiles1 = []
        for profile in profiles:
            profiles1.append(profile.get_attribute("href"))
        tryer = 0
        for Page_link in profiles1:
                browser.get(Page_link)
                try:Waiter.until(EC.visibility_of_element_located(("class name", 'content-holder')))
                except:pass
                data = {}
                data["Page Link"] = Page_link
                data["Information"] = {}
                try:data["Information"]['Last Name'] = browser.find_element("xpath" , "//div[@class='content-holder']//td[contains(text(), 'Last Name')]/following-sibling::td[1]").text
                except:print("Last Name Not Found")
                try:data["Information"]['First Name'] = browser.find_element("xpath" , "//div[@class='content-holder']//td[contains(text(), 'First Name')]/following-sibling::td[1]").text
                except:print("First Name Not Found")
                try:data["Information"]['Middle Name'] = data["Information"]['First Name'].split()[1]
                except:print("Middle Name Not Found")
                try:data["Information"]['Preferred Given'] = browser.find_element("xpath" , "//div[@class='content-holder']//td[contains(text(), 'Preferred')]/following-sibling::td[1]").text
                except:print("Preferred Given Not found")
                try:data["Information"]['Previous Name'] = browser.find_element("xpath" , "//div[@class='content-holder']//td[contains(text(), 'Previous')]/following-sibling::td[1]").text
                except:print("Previous Name Not found")
                data['Registration Information'] = {}
                try:data['Registration Information']['Certificate of Registration'] = browser.find_element("xpath" , "//table[@class='table']//td[contains(text(), 'Certificate of Registration')]/following-sibling::td[1]").text
                except:print("Certificate Not found")
                try:data['Registration Information']['Description'] = browser.find_element("xpath" , "//table[@class='table']//td[contains(text(), 'Description')]/following-sibling::td[1]").text
                except:print("Description Not Found")
                data["Business Contacts"] = []
                try:
                    for element in browser.find_elements("xpath","//li[@class='pr-work-address']"):
                        business_contact = {}
                        business_contact["Business Address"]=re.findall(".*?\n",element.text)[0]
                        business_contact["City"] = element.find_element("xpath" , "//span[@class='address']/span[@class='address']").text.split(",")[0].strip()
                        business_contact["State"] = element.find_element("xpath" , "//span[@class='address']/span[@class='address']").text.split(",")[1].strip()
                        business_contact["Postal Code"] = element.find_element("xpath" , "//span[@class='address']/span[@class='address']").text.split(",")[2].strip()
                        business_contact["Phone"] = re.findall("phone.*[-\dx]+",element.text.lower())[0].replace("phone","").replace(":","").strip()
                        business_contact["Email"] = re.findall("email.*[\w@\.]+",element.text.lower())[0].replace("email","").replace(":","").strip()
                        data["Business Contacts"].append(business_contact)
                except:print("Business Contacts Not Found")
                    
                data["Authorized Areas of Practices"] = []
                try:
                    for element in browser.find_elements("xpath" , "//th[contains(text(), 'Authorized Areas of Practice')]/parent::*/following-sibling::tr[1]//ul[@class='tab_lists']/li"):
                        data["Authorized Areas of Practices"].append(element.text)
                except:print("Authorized Areas of Practices Not Found")
                    

                data["Authorized Client Populations"] = []
                try:
                    for element in browser.find_elements("xpath" , "//th[contains(text(), 'Authorized Client Population')]/parent::*/following-sibling::tr[1]//ul[@class='tab_lists']/li"):
                        data["Authorized Client Populations"].append(element.text)
                except:print("Authorized Client Populations Not Found")
                    

                data["Languages in which services are provided"] = []

                try:
                    for element in browser.find_elements("xpath" , "//th[contains(text(), 'Languages in which services')]/parent::*/following-sibling::tr[1]//ul[@class='tab_lists']/li"):
                        data["Languages in which services are provided"].append(element.text)
                except : print("Languages not found")
                browser.find_element("id" , 'tab-registration').click()

                try:Waiter.until(EC.visibility_of_element_located(("xpath", "//*[contains(text(), 'Concurrent Registrations')]")))
                except:pass
                data["Highest Degree"]={}
                try:
                    Highest = browser.find_element("xpath" , "//th[contains(text(), 'Highest Degree')]/parent::*/following-sibling::tr[1]").text
                    data["Highest Degree"]["Highest Degree"] = re.findall("[hH]ighest [dD]egree.*:(.*)?\n",Highest)[0].strip()
                    data["Highest Degree"]["Year Awarded"] = re.findall("[yY]ear [aA]warded.*:(.*)?\n",Highest)[0].strip()
                    data["Highest Degree"]["Institution"] = re.findall("[Ii]nstitution.*:(.*)?$",Highest)[0].strip()
                except:
                    print("Highest Degree not found")

                data["Concurrent Registrations"] = []
                try:
                    for element in browser.find_elements("xpath" , "//th[contains(text(), 'Concurrent Registrations')]/parent::*/following-sibling::tr[1]"):
                        data["Concurrent Registrations"].append(element.text)
                except:print("Concurrent Registrations Not Found")
                
                try:
                    browser.find_element("id" , "tab-discipline").click()
                    Waiter.until(EC.visibility_of_element_located(("xpath", "//div[@aria-labelledby='tab-discipline']//tbody")))
                except:print("Tab Discipline Not Found")
                
                try:data["Discipline & Other Proceedings"] = browser.find_element("xpath", "//div[@aria-labelledby='tab-discipline']//tbody").text
                except:print("Discipline & Other Proceedings Not Found")
                cursor.execute("insert into Member_List values ( ? )",[ json.dumps(data)])
                conn.commit()
                j+=1
                print("Profile: "+str(j))
