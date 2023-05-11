import requests
import sqlite3
import json
url = "https://members.ocpinfo.com/tcpr/public/pr/en/form/ExecuteActionAndReturn"
conn = sqlite3.connect('Pharmacy_professional.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'book.cfi.ir' table with the specified fields

cursor.execute('''CREATE TABLE Pages (
                Rawdata JSON
)''')

# Commit the changes and close the connection
conn.commit()
payload = "dataTemplateId=0x80000000000003AB&recordId=&formId=0x800000000000002C&formPermission=1110&formUniqueIdentifier=4ccbe96b8ec64341b62517af4a9f9455-0x80000000000003AB-&53160447=&55507391=&25507703=&50122992=&35099771=&65243564=&65159742=&v=false&v=false&v=false&8311334=&__RequestVerificationToken=PSExmDKwzUOSdWDI4C6tReFDTPxXH3xiN1jNzrsthV9DlxJZQEf66TaVyPiJI9_N1lo7WMERBNoatXDUCmL-DCo84_MRLv9F_oG-n15JyqHShZnayEgtNMYzxflJl5ChTK7mQX54Ba232iEmNwi4QkU-iB9N0mrMVER1EX3NwL41&formExecuteAction=GetSRL&AdditionnalData=%7B%22Name%22%3A%22%22%2C%22Type%22%3A%22%22%2C%22Location%22%3A%22%22%2C%22Workplace%22%3A%22%22%2C%22City%22%3A%22%22%2C%22PostalCode%22%3A%22%22%2C%22Page%22%3A1%2C%22SearchType%22%3A%22person%22%2C%22isAdvancedSeach%22%3Afalse%7D"
headers = {
  'authority': 'members.ocpinfo.com',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'openWindows=:4051; _hjSessionUser_1786836=eyJpZCI6IjNmNmY1ZjBmLWQzNjItNWM2OS04NWIxLTc2ODQyODNhNTQ5NiIsImNyZWF0ZWQiOjE2ODMzOTQxNzMxMjAsImV4aXN0aW5nIjpmYWxzZX0=; _ga_Q9X2L1KB13=GS1.1.1683394169.1.1.1683395721.0.0.0; ASP.NET_SessionId=5nd3rgknzkuoj2dtg05npb4h; _gid=GA1.2.1720290947.1683695903; __RequestVerificationToken_L1RDUFI1=Qy5R3ESBqIa-2-PQi3_OQzTBMOlNDwj6cAXycer5UkguKtFZpdSrg9JRANVoiDSoO5ww6ux6jLP4lUr4fY7RUBABad1oxBb0dw0serDcaykbpewTkJtIrsTGDziEP_-s3Uz47RnkpiO6XaYKmnaZtQ2; _ga=GA1.1.1003426595.1683393951; _gat=1; _ga_PJE82RYKNK=GS1.1.1683699177.4.1.1683701076.0.0.0',
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

# Connect to the database (create it if it doesn't exist)


# Create the 'book.cfi.ir' table with the specified fields
cursor.execute('''CREATE TABLE Pages (
                Rawdata JSON
)''')

# Commit the changes and close the connection
conn.commit()

NumberOfPage = response.json()['NumberOfPage']

for page in range(1 , NumberOfPage+1):
    print(page)
    url = "https://members.ocpinfo.com/tcpr/public/pr/en/form/ExecuteActionAndReturn"
    payload = f"dataTemplateId=0x80000000000003AB&recordId=&formId=0x800000000000002C&formPermission=1110&formUniqueIdentifier=4ccbe96b8ec64341b62517af4a9f9455-0x80000000000003AB-&53160447=&55507391=&25507703=&50122992=&35099771=&65243564=&65159742=&v=false&v=false&v=false&8311334=&__RequestVerificationToken=PSExmDKwzUOSdWDI4C6tReFDTPxXH3xiN1jNzrsthV9DlxJZQEf66TaVyPiJI9_N1lo7WMERBNoatXDUCmL-DCo84_MRLv9F_oG-n15JyqHShZnayEgtNMYzxflJl5ChTK7mQX54Ba232iEmNwi4QkU-iB9N0mrMVER1EX3NwL41&formExecuteAction=GetSRL&AdditionnalData=%7B%22Name%22%3A%22%22%2C%22Type%22%3A%22%22%2C%22Location%22%3A%22%22%2C%22Workplace%22%3A%22%22%2C%22City%22%3A%22%22%2C%22PostalCode%22%3A%22%22%2C%22Page%22%3A{str(page)}%2C%22SearchType%22%3A%22person%22%2C%22isAdvancedSeach%22%3Afalse%7D"
    headers = {
    'authority': 'members.ocpinfo.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'openWindows=:4051; _hjSessionUser_1786836=eyJpZCI6IjNmNmY1ZjBmLWQzNjItNWM2OS04NWIxLTc2ODQyODNhNTQ5NiIsImNyZWF0ZWQiOjE2ODMzOTQxNzMxMjAsImV4aXN0aW5nIjpmYWxzZX0=; _ga_Q9X2L1KB13=GS1.1.1683394169.1.1.1683395721.0.0.0; ASP.NET_SessionId=5nd3rgknzkuoj2dtg05npb4h; _gid=GA1.2.1720290947.1683695903; __RequestVerificationToken_L1RDUFI1=Qy5R3ESBqIa-2-PQi3_OQzTBMOlNDwj6cAXycer5UkguKtFZpdSrg9JRANVoiDSoO5ww6ux6jLP4lUr4fY7RUBABad1oxBb0dw0serDcaykbpewTkJtIrsTGDziEP_-s3Uz47RnkpiO6XaYKmnaZtQ2; _ga=GA1.1.1003426595.1683393951; _gat=1; _ga_PJE82RYKNK=GS1.1.1683699177.4.1.1683701076.0.0.0',
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