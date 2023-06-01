import requests
import json
import sqlite3
import math
from datetime import datetime
con = sqlite3.connect('crpo_thentiacloud.db')
STATUS ={
    "REGISTER_PROFILE_STATUS_QUALIFYING": "Authorized to practise as a Qualifying registrant"
    ,"REGISTER_PROFILE_STATUS_WORKING_TOWARDS": "Authorized to practise while working toward independent practice"
    ,"REGISTER_PROFILE_STATUS_INDEPENDENT": "Authorized for independent practice"
    ,"REGISTER_PROFILE_STATUS_TEMPORARY": "Authorized to practise as a Temporary registrant"
    ,"REGISTER_PROFILE_STATUS_INACTIVE": "Not currently practising as a Registered Psychotherapist in Ontario"
    ,"REGISTER_PROFILE_STATUS_NOT_REGISTRANT": "No longer registered with CRPO"
    ,"REGISTER_PROFILE_STATUS_UNAUTHORIZED": "Unauthorized to practise as a Registered Psychotherapist in Ontario"
}
cure=con.cursor()
try:
    cure.execute("create table data (firstName TEXT , lastName TEXT , data JSON)")
    con.commit()
except:
    pass

url = "https://crpo.ca.thentiacloud.net/rest/public/registrant/search/?keyword=all&skip=0&take=20&lang=en"

headers = {
  'authority': 'crpo.ca.thentiacloud.net',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'referer': 'https://crpo.ca.thentiacloud.net/webs/crpo/register/',
  'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


headers2 = {
  'authority': 'crpo.ca.thentiacloud.net',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': '_ga=GA1.2.576689152.1683816468; _gid=GA1.2.669470426.1683816468',
  'referer': 'https://crpo.ca.thentiacloud.net/webs/crpo/register/',
  'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
#API format 1 : 
while True:
    try:
        r1 = requests.get(url, headers=headers)
        resultCount=r1.json()["resultCount"]
    except:
        print("Error Connection")
    else:
        break

i=0
for pagenum in range(0,math.floor(int(resultCount)/20)):
    pagenum = 20*pagenum
    url = f"https://crpo.ca.thentiacloud.net/rest/public/registrant/search/?keyword=all&skip={str(pagenum)}&take=20&lang=en"
    #API format 1 : 
    while True:
        try:
            r1 = requests.get(url, headers=headers)
            results=r1.json()["result"]
        except:
            print("Error Connection")
        else:
            break

    for result in results:
        # API Format 2:
        while True:
            try:
                data={}
                url2 = f"https://crpo.ca.thentiacloud.net/rest/public/registrant/get/?id={result['id']}&lang=en"
                r2 = requests.get(url2, headers=headers2)
                profile = r2.json()
                try:firstName = profile["commonFirstName"]
                except:pass
                try:lastName = profile["commonLastName"]
                except:pass
                data["Name"] = {}
                try:data["Name"]["firstName"] = profile["firstName"]
                except:pass
                try:data["Name"]["middleName"] = profile["middleName"]
                except:pass
                try:data["Name"]["lastName"] = profile["lastName"]
                except:pass
                data["Other Name"] = {}
                try:data["Other Name"]["Commonly Used First Name"] = profile["commonFirstName"]
                except:pass
                try:data["Other Name"]["Commonly Used Last Name"] = profile["commonLastName"]
                except:pass
                try:data["Registration Number"] = profile["registrationNumber"]
                except:pass
                try:data["Category"]=profile["registrationCategory"]
                except:pass
                if "registrationStatus" in profile.keys():
                    try:data["Status"] = STATUS[profile["registrationStatus"]]
                    except:data["Status"] = profile["registrationStatus"]
                try:data["Date of Initial Registration"] = datetime.strptime(profile["initialRegistrationDate"].split("T")[0], "%Y-%m-%d").date().strftime("%b-%d-%Y")
                except:pass
                try:data["E-mail Address"] = profile["email"]
                except:pass
                try:data["Practice Sites"] = profile["placesOfPractice"]
                except:pass
                try:data["Languages of Care"] = profile["language"]
                except:pass
                try:data["Current Registration with Other Statutory Regulatory Bodies"] = profile["otherRegistrations"]
                except:pass
                try:data["Page Link"] = "https://crpo.ca.thentiacloud.net/webs/crpo/register/#/profile/all/0/20/"+profile["id"]
                except:pass
                cure.execute("insert into data values (?, ? , ?)",[firstName , lastName , json.dumps(data)])
                con.commit()
                i+=1
                print("data : " + str(i))
            except:
                print("Error Connection")
            else:
                break

