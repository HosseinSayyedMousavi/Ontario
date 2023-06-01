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


conn = sqlite3.connect('Pharmacy.db')
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
        OutpuData["Name_of_the_Pharmacy"] =page["Name"]
        OutpuData['FriendlyStatus'] = page['FriendlyStatus']
        OutpuData["Type_of_Pharmacy"] = page["Type"]
        
        href = page["href"]
        href = "https://members.ocpinfo.com/tcpr/public/pr/en/" +href
        OutpuData['Page Link'] = href
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
            
            try:OutpuData['Pharmacy Staff'] = FormParameterList['PharmacyStaff']
            except:pass
            try:OutpuData["Owner/Corporation"] = FormParameterList["Corporation"]
            except:pass
            try:OutpuData["Accreditation_number"] = FormParameterList['AccredNo']
            except:pass
            try:OutpuData["Date_issued"] = soup.select("#OpeningDate")[0].text.strip("\r\n").strip()
            except:pass
            try:OutpuData["Fax"] = soup.select("#FaxSpan")[0].text.strip("\r\n").strip()
            except:pass
            try:OutpuData["Phone"] = soup.select("#PhoneSpan")[0].text.strip("\r\n").strip()
            except:pass
            try:OutpuData["Postal_Code"] = soup.select("#pid45")[0].text.strip("\r\n").strip()
            except:pass
            try:OutpuData["City"] = page['CompanyLocation']
            except:pass
            try:OutpuData["Address"] = page['Address'] +"," +page['CompanyLocation']+","+OutpuData["Postal_Code"]
            except:pass

        except:
          print("Error2")
             
        cursor.execute("insert into FinalData values ( ? )",[ json.dumps(OutpuData)])
        conn.commit()
        j +=1
        print("page: "+str(i) , "element: " + str(j))
