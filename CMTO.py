import requests
from pprintpp import pprint
import json
import openpyxl
import sqlite3
headers = {"accept": "application/json, text/plain, */*",
           "accept-encoding": "gzip, deflate, br",
           "accept-language": "en-US,en;q=0.9,fa;q=0.8",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
           "referer": "https://cmto.ca.thentiacloud.net/webs/cmto/register/",
          "sec-fetch-site": "same-origin",
           }
workbook = openpyxl.Workbook()
sheet = workbook.active
con = sqlite3.connect('Results.db')
cure=con.cursor()
cure.execute("create table %s ( profileId TEXT , data JSON)"%"Persons")
cure.execute("create table %s ( corporationId TEXT , data JSON)"%"Corporations")
#API format 1 : 
r = requests.get("https://cmto.ca.thentiacloud.net/rest/public/profile/search/?keyword=all&skip=0&take=10&authorizedToPractice=0&acupunctureAuthorized=0&gender=all&registrationStatus=all&city=all&sortOrder=asc&sortField=lastname&_=1679739073295", headers=headers)
Response = r.json()
resultCount = Response["resultCount"]
pages=round(resultCount/10)

for p in range(0,pages+1):
    p1=10*p
    print("persons:" + str(p1)+"of 10000")
    r = requests.get("https://cmto.ca.thentiacloud.net/rest/public/profile/search/?keyword=all&skip=%s&take=10&authorizedToPractice=0&acupunctureAuthorized=0&gender=all&registrationStatus=all&city=all&sortOrder=asc&sortField=lastname&_=1679739073295"%p1, headers=headers)
    Response = r.json()
    Results = Response["result"]
    for result in Results:
        JsonResult={}
        profileId=result["profileId"]
        JsonResult["practiceLocation"] = result["practiceLocation"]
        JsonResult["firstName"]=result["firstName"]
        JsonResult["lastName"] = result["lastName"]
        JsonResult["gender"] = result["gender"]
        JsonResult["commonName"] = result["commonName"]
        JsonResult["city"] = result["city"]
        JsonResult["authorizedToPractice"] = result["authorizedToPractice"]
        JsonResult["publicRegisterAlert"] = result["publicNotices"] #List
        r2 = requests.get("https://cmto.ca.thentiacloud.net/rest/public/profile/get/?id=%s&_=1679750037565"%profileId,headers=headers)
        Response2 = Response2
        JsonResult["initialRegistrationDate"] = Response2["initialRegistrationDate"]
        JsonResult["classOfRegistration"] = Response2["registrationHistory"][0]["classOfRegistration"]
        JsonResult["Status"] = Response2["registrationHistory"][0]["Status"]
        JsonResult["electoralDistrict"] = Response2["electoralZone"]
        JsonResult["acupunctureAuthorized"] = Response2["acupunctureAuthorized"]
        JsonResult["Business_Contact_Information"] = Response2["placesOfPractice"] #List
        JsonResult["education"] = Response2["education"]
        JsonResult["Language_Used_In_Practice"]= Response2["languagesOfCare"] # List
        JsonResult["nameHistory"] = Response2["nameHistory"] # List
        cure.execute("insert into Persons values (?, ?)",[profileId, json.dumps(JsonResult)])
        con.commit()
# API Format 2:
R=requests.get("https://cmto.ca.thentiacloud.net/rest/public/corporation/search/?keyword=all&skip=0&take=10&active=0&_=1679814511460",headers=headers)
RESPONSE=r.json()
ResultCount=RESPONSE["resultCount"]
Pages=round(ResultCount/10)
for p in range(0,Pages+1):
    p1=10*p
    print("Corporations:" + str(p1)+"of 133")
    R=requests.get("https://cmto.ca.thentiacloud.net/rest/public/corporation/search/?keyword=all&skip=%s&take=10&active=0&_=1679814511460"%p1,headers=headers)
    RESPONSE=r.json()
    Results = RESPONSE["results"]
    for result in Results:
        JsonResult={}
        corporationId = result["corporationId"]
        JsonResult["corporationName"] = result["corporationName"]
        JsonResult["City"] = result["corporationCity"]
        JsonResult["Province"] = result["corporationProvince"]
        JsonResult["Country"] = result["corporationCountry"]
        JsonResult["Registration_Status"] = result["corporationStatus"]
        R2 = requests.get("https://cmto.ca.thentiacloud.net/rest/public/corporation/get/?id=%s&_=1679815905957"%corporationId,headers=headers)
        RESPONSE2 = R2.json()
        JsonResult["registrationNumber"] = RESPONSE2["registrationNumber"]
        JsonResult["Street_Address"] = RESPONSE2["address1"]
        JsonResult["Postal_Code"] = RESPONSE2["corporationPostalCode"]
        JsonResult["Phone_Number"] = RESPONSE2["phone"]
        JsonResult["faxNumber"] = RESPONSE2["faxNumber"]
        JsonResult["Email"] = RESPONSE2["email"]
        JsonResult["website"] = RESPONSE2["website"]
        JsonResult["shareholders"] = RESPONSE2["shareholder"] #List
        cure.execute("insert into Corporations values (?, ?)",[profileId, json.dumps(JsonResult)])
        con.commit()
