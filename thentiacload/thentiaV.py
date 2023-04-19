import requests
import json
import sqlite3

con = sqlite3.connect('thentiacloud.db')

profiles=con.execute('select data from Veterinarians').fetchall()
con2=sqlite3.connect('thentiacloudFinal.db')
cure2=con2.cursor()
try:
    cure2.execute("create table %s (data JSON)"%"Veterinarians")
    con2.commit()
except:
    pass
i=0
for profile in profiles:
    data={
"Name":'',
"Summary":{
    "Languages":"",
    "Patient Group":"",
    "Patient Type":"",
},
"Location":{
    "Name of the Hospital":"",
    "Address":"",
    "ZipCode":"",
    "Latitude":"",
    "Longitude":""
},
"Contact Information":{
    "Work":"",
    "Email":"",
},
"Current Licence Information":{
    "Licence Type":"",
    "Current Status":"",
    "Active Until":"",
    "Conditions & Limitations":""
},
"Professional Activities":{
    "Works in":"",
    "Type of Practice":""
},
"Degree":{
    "Undergraduate Veterinary Degree":""
},
"Specialty Board Certification":"",
"Hearings":"",
"Page URL":""
}
    profile = json.loads(profile[0])
    try:data["Name"] = profile["salutationName"]
    except : pass
    try:data["Summary"]["Languages"] = profile["language"]
    except : pass
    try:data["Summary"]["Patient Group"] = profile["professionalActivity"]["patientGroups"]
    except : pass
    try:data["Summary"]["Patient Type"] = profile["professionalActivity"]["patientTypes"]
    except : pass
    try:data["Location"]= profile["searchaddress"]
    except : pass
    try:data["Location"]["Name of the Hospital"] = profile["primarypractice"]["name"]
    except : pass
    try:data["Contact Information"]["Email"]= profile["primarypractice"]["email"]
    except : pass
    try:data["Contact Information"]["Work"]= profile["primarypractice"]["telephone"]
    except : pass
    try:data["Current Licence Information"]["Licence Type"] = profile["classOfRegistration"]["name"]
    except : pass
    try:data["Current Licence Information"]["Current Status"] = profile["registrationStatus"]["name"]
    except : pass
    try:data["Current Licence Information"]["Active Until"] = profile["expirationRegistrationDate"]
    except : pass
    try:
        for notice in profile["publicNotices"]:
            if notice["noticeType"]["name"] == "Condition\/Limitation" :
                data["Current Licence Information"]["Conditions & Limitations"] = notice["summary"]
                break
    except : pass
    try:data["Professional Activities"]["Works in"] = profile["professionalActivity"]["employmentType"]
    except : pass
    try:data["Professional Activities"]["Type of Practice"] = profile["professionalActivity"]["employmentFunction"]
    except : pass
    try:data["Degree"]["Undergraduate Veterinary Degree"] = profile["education"]["graduationYear"]+"-"+profile["education"]["name"]
    except:  pass
    try: data["Specialty Board Certification"] = profile["education"]["certificateDate"]+"-"+profile["education"]["name"]
    except: pass
    try: 
        for notice in profile["publicNotices"]:
            if notice["noticeType"]["name"] == "Hearing" :
                data["Hearing"] = notice["summary"]
                break
    except: pass
    try: data["Page URL"] = "https://cvo.ca.thentiacloud.net/webs/cvo/register/#/profile/"+profile["id"]
    except: pass
    cure2.execute("insert into Veterinarians values (?)",[json.dumps(data)])
    con2.commit()
    i += 1
    print(i)

