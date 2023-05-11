from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3

maxtry = 4
def urlCreator(href):
  table = href.split("table=")[1].split("&")[0]
  recordId = href.split("table=")[1].split("&")[1].strip("record=")
  form = href.split("table=")[1].split("&")[2].strip("form=")
  url = f"https://members.ocpinfo.com/tcpr/public/pr/en/form/new?table={table}&form={form}&recordId={recordId}"
  return url

headers = {
  'authority': 'members.ocpinfo.com',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'cookie': '_hjSessionUser_1786836=eyJpZCI6IjNmNmY1ZjBmLWQzNjItNWM2OS04NWIxLTc2ODQyODNhNTQ5NiIsImNyZWF0ZWQiOjE2ODMzOTQxNzMxMjAsImV4aXN0aW5nIjpmYWxzZX0=; _ga_Q9X2L1KB13=GS1.1.1683394169.1.1.1683395721.0.0.0; _gid=GA1.2.1720290947.1683695903; ASP.NET_SessionId=sc5kwl4f1vot2crdpr00gntm; __RequestVerificationToken_L1RDUFI1=kXv149W0ad29QMdTMziYoK4PHnui2OAqaOmMgyC8X_aHw7A7xZHk3qYu3DP9bYVvCRJisQ2ICjEv-1BKH5uv2-D2ZzhYl8UZazZFAZPvalwYFiWJXt2N6xtV1m-G9zqOIoNu7V61fLrxRGe8Y7kdgw2; _gat=1; _ga_PJE82RYKNK=GS1.1.1683796067.11.1.1683796135.0.0.0; _ga=GA1.2.1003426595.1683393951',
  'referer': 'https://members.ocpinfo.com/tcpr/public/pr/en/',
  'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}


conn = sqlite3.connect('Pharmacy_professional.db')
cursor = conn.cursor()
try:
  cursor.execute('''CREATE TABLE FinalData (
                  Data JSON
  )''')

  conn.commit()
except:
   pass

cursor.execute("SELECT * FROM Pages")
j = 0
Pages = cursor.fetchall()
for i in range(0,len(Pages)):
    for page in json.loads(Pages[i][0])["SRL"]:
        OutpuData={}
        OutpuData["Name"] =page["Name"]
        OutpuData['FriendlyStatus'] = page['FriendlyStatus']
        OutpuData["Type"] = page["Type"]
        href = page["href"]
        href = "https://members.ocpinfo.com/tcpr/public/pr/en/" +href
        url = urlCreator(href)
        mytry=0
        while mytry < maxtry:
          try:
            Content = requests.get(url , headers=headers , timeout=20).json()['centerContent']
          except:
            mytry += 1
            print("Error1")
          else:
            break
          
        else:
           j+=1
           OutpuData["Error"] = "This Page Not Open!"
           cursor.execute("insert into FinalData values ( ? )",[ json.dumps(OutpuData)])
           conn.commit()
           print(f"element {str(j)} Not Open!")
           continue
        try:
            FormParameterList = json.loads(re.findall(r"FormParameterList =(.*})",Content.replace("\\",""))[0])
            soup = BeautifulSoup(Content,"html.parser")
            OutpuData['Page Link'] = href
            OutpuData['WorkPlaces'] = FormParameterList['WorkPlaces']
            OutpuData["EducationList"] = FormParameterList["EducationList"]
            OutpuData["LanguageCareList"] = FormParameterList['LanguageCareList']
            OutpuData["InjectionTrainingList"] = FormParameterList['InjectionTrainingList']
            OutpuData["Registration number"] = soup.select("#pid22")[0].text.strip("Registration number:").strip()
            OutpuData["Page Content"] = Content
        except:
          print("Error2")
             
        cursor.execute("insert into FinalData values ( ? )",[ json.dumps(OutpuData)])
        conn.commit()
        j +=1
        print("page: "+str(i) , "element: " + str(j))

