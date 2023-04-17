import requests
import json
import sqlite3

con = sqlite3.connect('thentiacloud.db')
cure=con.cursor()
try:
    cure.execute("create table %s (name TEXT , data JSON)"%"Professional_Corporations")
    con.commit()
except:
    pass
url = "https://cvo.ca.thentiacloud.net/rest/public/corporation/search/"

payload = "{\"searchBy\":\"2\",\"name\":\"\",\"status\":\"\",\"address\":\"\",\"skip\":0,\"take\":2296}"
headers = {
  'authority': 'cvo.ca.thentiacloud.net',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'content-type': 'application/json;charset=UTF-8',
  'origin': 'https://cvo.ca.thentiacloud.net',
  'referer': 'https://cvo.ca.thentiacloud.net/webs/cvo/register/',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

headers2 = {
  'authority': 'cvo.ca.thentiacloud.net',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'referer': 'https://cvo.ca.thentiacloud.net/webs/cvo/register/',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

#API format 1 : 
while True:
    try:
        r1 =  requests.request("POST", url, headers=headers, data=payload)
        results=r1.json()["result"]
    except:
        print("Error Connection")
    else:
        break


import requests

url = "https://cvo.ca.thentiacloud.net/rest/public/corporation/get/?id=6035b67b355c4667ef6f9c4a"


lenres = len(results)

i=0
for result in results:
    # API Format 2:
    while True:
        try:
            url2 = "https://cvo.ca.thentiacloud.net/rest/public/corporation/get/?id="+result["id"]
            r2 = requests.get(url2, headers=headers2)
            name = r2.json()["name"]
            data = r2.json()
            cure.execute("insert into Professional_Corporations values (?, ? )",[name  , json.dumps(data)])
            con.commit()
            i+=1
            print("\nProfessional_Corporations : " + str(i)+" of " + str(lenres))
        except:
            print("Error Connection")
        else:
            break