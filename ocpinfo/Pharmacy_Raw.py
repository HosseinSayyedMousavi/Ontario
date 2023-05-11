import requests
# from pprintpp import pprint
import sqlite3
import json
url = "https://members.ocpinfo.com/tcpr/public/pr/en/form/ExecuteActionAndReturn"
conn = sqlite3.connect('Pharmacy.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'book.cfi.ir' table with the specified fields
try:
  cursor.execute('''CREATE TABLE Pages (
                  Rawdata JSON
  )''')

  conn.commit()
except:
   pass
payload = "dataTemplateId=0x80000000000003AA&recordId=&formId=0x800000000000002B&formPermission=1110&formUniqueIdentifier=4f1dc3b5df4d47b4bcb507d5c38fb995-0x80000000000003AA-&43382694=&3297376=&37059224=&26942802=&28187036=&__RequestVerificationToken=ewQSRO8xeZVhYy5D8V3_zCpnDelFK0TJCHsZ7Qq9ZOd9YIT2FEHyZTSz9GbvRON9ZcyRaYzVGTLC9u7PYIrGdx3sXgJoLUX3G_1l5-TKqyZOhawrR7Y5tdmS6Er5m2S_4VOter6dvNA9Fjyo6HPeM5ghsLsAXPH-gb_1xQ4KWtk1&formExecuteAction=GetSRL&AdditionnalData=%7B%22Name%22%3A%22%22%2C%22Type%22%3A%22%22%2C%22FriendlyType%22%3A%22%22%2C%22Location%22%3A%22%22%2C%22City%22%3A%22%22%2C%22PostalCode%22%3A%22%22%2C%22Page%22%3A500%2C%22SearchType%22%3A%22place%22%2C%22isAdvancedSeach%22%3Afalse%7D"
headers = {
  'authority': 'members.ocpinfo.com',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'openWindows=; _hjSessionUser_1786836=eyJpZCI6IjNmNmY1ZjBmLWQzNjItNWM2OS04NWIxLTc2ODQyODNhNTQ5NiIsImNyZWF0ZWQiOjE2ODMzOTQxNzMxMjAsImV4aXN0aW5nIjpmYWxzZX0=; _ga_Q9X2L1KB13=GS1.1.1683394169.1.1.1683395721.0.0.0; ASP.NET_SessionId=5nd3rgknzkuoj2dtg05npb4h; _gid=GA1.2.1720290947.1683695903; __RequestVerificationToken_L1RDUFI1=Qy5R3ESBqIa-2-PQi3_OQzTBMOlNDwj6cAXycer5UkguKtFZpdSrg9JRANVoiDSoO5ww6ux6jLP4lUr4fY7RUBABad1oxBb0dw0serDcaykbpewTkJtIrsTGDziEP_-s3Uz47RnkpiO6XaYKmnaZtQ2; _ga=GA1.1.1003426595.1683393951; _gat=1; _ga_PJE82RYKNK=GS1.1.1683695903.3.1.1683696546.0.0.0',
  'origin': 'https://members.ocpinfo.com',
  'referer': 'https://members.ocpinfo.com/tcpr/public/pr/en/',
  'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

# Create a cursor object to execute SQL commands
cursor = conn.cursor()
response = requests.request("POST", url, headers=headers, data=payload)
# pprint(response.json())
NumberOfPage = response.json()['NumberOfPage']

for page in range(615 , 617):
    print(page)
    url = "https://members.ocpinfo.com/tcpr/public/pr/en/form/ExecuteActionAndReturn"

    payload = f"dataTemplateId=0x80000000000003AA&recordId=&formId=0x800000000000002B&formPermission=1110&formUniqueIdentifier=4f1dc3b5df4d47b4bcb507d5c38fb995-0x80000000000003AA-&43382694=&3297376=&37059224=&26942802=&28187036=&__RequestVerificationToken=ewQSRO8xeZVhYy5D8V3_zCpnDelFK0TJCHsZ7Qq9ZOd9YIT2FEHyZTSz9GbvRON9ZcyRaYzVGTLC9u7PYIrGdx3sXgJoLUX3G_1l5-TKqyZOhawrR7Y5tdmS6Er5m2S_4VOter6dvNA9Fjyo6HPeM5ghsLsAXPH-gb_1xQ4KWtk1&formExecuteAction=GetSRL&AdditionnalData=%7B%22Name%22%3A%22%22%2C%22Type%22%3A%22%22%2C%22FriendlyType%22%3A%22%22%2C%22Location%22%3A%22%22%2C%22City%22%3A%22%22%2C%22PostalCode%22%3A%22%22%2C%22Page%22%3A{str(page)}%2C%22SearchType%22%3A%22place%22%2C%22isAdvancedSeach%22%3Afalse%7D"
    headers = {
    'authority': 'members.ocpinfo.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'openWindows=; _hjSessionUser_1786836=eyJpZCI6IjNmNmY1ZjBmLWQzNjItNWM2OS04NWIxLTc2ODQyODNhNTQ5NiIsImNyZWF0ZWQiOjE2ODMzOTQxNzMxMjAsImV4aXN0aW5nIjpmYWxzZX0=; _ga_Q9X2L1KB13=GS1.1.1683394169.1.1.1683395721.0.0.0; ASP.NET_SessionId=5nd3rgknzkuoj2dtg05npb4h; _gid=GA1.2.1720290947.1683695903; __RequestVerificationToken_L1RDUFI1=Qy5R3ESBqIa-2-PQi3_OQzTBMOlNDwj6cAXycer5UkguKtFZpdSrg9JRANVoiDSoO5ww6ux6jLP4lUr4fY7RUBABad1oxBb0dw0serDcaykbpewTkJtIrsTGDziEP_-s3Uz47RnkpiO6XaYKmnaZtQ2; _ga=GA1.1.1003426595.1683393951; _gat=1; _ga_PJE82RYKNK=GS1.1.1683695903.3.1.1683696546.0.0.0',
    'origin': 'https://members.ocpinfo.com',
    'referer': 'https://members.ocpinfo.com/tcpr/public/pr/en/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    cursor.execute("insert into Pages values ( ? )",[ json.dumps(data)])
    conn.commit()