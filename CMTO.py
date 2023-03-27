import requests
import json
import sqlite3
headers = {"accept": "application/json, text/plain, */*",
           "accept-encoding": "gzip, deflate, br",
           "accept-language": "en-US,en;q=0.9,fa;q=0.8",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
           "referer": "https://cmto.ca.thentiacloud.net/webs/cmto/register/",
          "sec-fetch-site": "same-origin",
           }

con = sqlite3.connect('Results.db')
cure=con.cursor()
try:
    cure.execute("create table %s ( ProfileName TEXT , data JSON)"%"Persons")
    cure.execute("create table %s ( CorporationName TEXT , data JSON)"%"Corporations")
    con.commit()
except:
    pass
#API format 1 : 
while True:
    try:
        r = requests.get("https://cmto.ca.thentiacloud.net/rest/public/profile/search/?keyword=all&skip=0&take=10&authorizedToPractice=0&acupunctureAuthorized=0&gender=all&registrationStatus=all&city=all&sortOrder=asc&sortField=lastname&_=1679739073295", headers=headers)
        Response = r.json()
    except:
        print("Error Connection")
    else:
        break
resultCount = Response["resultCount"]
pages=round(resultCount/10)

for p in range(0,pages+1):
    p1=10*p
    while True:
        try:
            r = requests.get("https://cmto.ca.thentiacloud.net/rest/public/profile/search/?keyword=all&skip=%s&take=10&authorizedToPractice=0&acupunctureAuthorized=0&gender=all&registrationStatus=all&city=all&sortOrder=asc&sortField=lastname&_=1679739073295"%p1, headers=headers)
            Response = r.json()
        except:
            print("Error Connection")
        else:
            break
    
    Results = Response["result"]
    i=0
    for result in Results:
        i+=1
        print("Persons : " + str(p1+i)+" of "+str(resultCount))
        JsonResult={}
        profileId=result["profileId"]
        JsonResult["practiceLocation"] = result["practiceLocation"]
        JsonResult["firstName"]=result["firstName"]
        JsonResult["lastName"] = result["lastName"]
        ProfileName = result["firstName"] + " " + result["lastName"]
        JsonResult["gender"] = result["gender"]
        JsonResult["commonName"] = result["commonName"]
        JsonResult["city"] = result["city"]
        JsonResult["authorizedToPractice"] = result["authorizedToPractice"]
        JsonResult["publicRegisterAlert"] = result["publicNotices"] #List
        while True:
            try:
                r2 = requests.get("https://cmto.ca.thentiacloud.net/rest/public/profile/get/?id=%s&_=1679750037565"%profileId,headers=headers)
                Response2 = r2.json()
            except:
                print("Error Connection")
            else:
                break
        
        JsonResult["initialRegistrationDate"] = Response2["initialRegistrationDate"]
        JsonResult["classOfRegistration"] = Response2["registrationHistory"][0]["classOfRegistration"]
        JsonResult["Status"] = Response2["registrationHistory"][0]["registrationStatus"]
        JsonResult["electoralDistrict"] = Response2["electoralZone"]
        JsonResult["acupunctureAuthorized"] = Response2["acupunctureAuthorized"]
        JsonResult["Business_Contact_Information"] = Response2["placesOfPractice"] #List
        JsonResult["education"] = Response2["education"]
        JsonResult["Language_Used_In_Practice"]= Response2["languagesOfCare"] # List
        JsonResult["nameHistory"] = Response2["nameHistory"] # List
        cure.execute("insert into Persons values (?, ?)",[ProfileName, json.dumps(JsonResult)])
        con.commit()
# API Format 2:
while True:
    try:
        R=requests.get("https://cmto.ca.thentiacloud.net/rest/public/corporation/search/?keyword=all&skip=0&take=10&active=0&_=1679814511460",headers=headers)
        RESPONSE=R.json()
    except:
        print("Error Connection")
    else:
        break

ResultCount=RESPONSE["resultCount"]
Pages=round(ResultCount/10)

for p in range(0,Pages+1):
    p1=10*p
    while True :
        try:
            R=requests.get("https://cmto.ca.thentiacloud.net/rest/public/corporation/search/?keyword=all&skip=%s&take=10&active=0&_=1679814511460"%p1,headers=headers)
            RESPONSE=R.json()
        except:
            print("Error Connection")
        else:
            break
    
    Results = RESPONSE["result"]
    i=0
    for result in Results:
        i+=1
        print("Corporations : " + str(p1+i)+" of "+str(ResultCount))
        JsonResult={}
        corporationId = result["corporationId"]
        JsonResult["corporationName"] = result["corporationName"]
        CorporationName = result["corporationName"]
        JsonResult["City"] = result["corporationCity"]
        JsonResult["Province"] = result["corporationProvince"]
        JsonResult["Country"] = result["corporationCountry"]
        JsonResult["Registration_Status"] = result["corporationStatus"]
        while True:
            try:
                R2 = requests.get("https://cmto.ca.thentiacloud.net/rest/public/corporation/get/?id=%s&_=1679815905957"%corporationId,headers=headers)
                RESPONSE2 = R2.json()
            except:
                print("Error Connection")
            else:
                break
        try:
            JsonResult["registrationNumber"] = RESPONSE2["registrationNumber"]
            JsonResult["Street_Address"] = RESPONSE2["address1"]
            JsonResult["Postal_Code"] = RESPONSE2["corporationPostalCode"]
            JsonResult["Phone_Number"] = RESPONSE2["phone"]
            JsonResult["faxNumber"] = RESPONSE2["faxNumber"]
            JsonResult["Email"] = RESPONSE2["email"]
            JsonResult["website"] = RESPONSE2["website"]
            JsonResult["shareholders"] = RESPONSE2["shareholder"] #List

        except :
            pass
        cure.execute("insert into Corporations values (?, ?)",[CorporationName, json.dumps(JsonResult)])
        con.commit()
