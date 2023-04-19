import requests 
from pprintpp import pprint
import json
headers = {"Accept": "application/json, text/plain, */*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
"Connection": "keep-alive",
"Host": "hsd.healthconnectontario.health.gov.on.ca",
"Referer": "https://hsd.healthconnectontario.health.gov.on.ca/",
"sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

r=requests.get("https://hsd.healthconnectontario.health.gov.on.ca/fhir-server/Practitioner?include-filter=true&_count=20&language=eng&_revinclude=PractitionerRole%3Apractitioner&_page=1",headers=headers)
Response=r.json()
Total_Pages = Response["meta"]["extension"][1]["extension"][0]["valueInteger"]
ListOut=Response["entry"]
print(len(ListOut))
# for i in range(2,Total_Pages+1):
#     print(str(round(i/Total_Pages*100,2))+"  %")
#     r=requests.get("https://hsd.healthconnectontario.health.gov.on.ca/fhir-server/Practitioner?include-filter=true&_count=20&language=eng&_revinclude=PractitionerRole%3Apractitioner&_page="+str(i),headers=headers)
#     Response=r.json()
#     ListOut.extend(Response["entry"])

with open("test.json", "w") as fp:
    json.dump(Response,fp)
