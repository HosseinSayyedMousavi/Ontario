from datetime import datetime
import json
import sqlite3

con = sqlite3.connect('thentiacloud.db')

profiles=con.execute('select data from Professional_Corporations').fetchall()
con2=sqlite3.connect('thentiacloudFinal.db')
cure2=con2.cursor()
try:
    cure2.execute("create table %s (data JSON)"%"Professional_Corporations")
    con2.commit()
except:
    pass
i=0
for profile in profiles:
    data={
"Name":'',
"Location":{
    "street1": "",
    "street2": "",
    "city": "",
    "province": "",
    "country": "",
    "postalCode": "",
    "Latitude":"",
    "Longitude":""
},
"Contact Information":{
    "Work":"",
    "Email":"",
    "fax": "",
},
"Current Certificate":{
    "Status":"",
    "Expires":"",
    "Certificate History":"",
},
"Managing Director":{
    "Name":"",
    "URL":""
},
"Page URL":""
}
    profile = json.loads(profile[0])

    try:data["Name"] = profile["name"]
    except : pass
    try:data["Location"]["street1"] = profile["street1"]
    except : pass
    try:data["Location"]["street2"] = profile["street2"]
    except : pass
    try:data["Location"]["city"] = profile["city"]
    except : pass
    try:data["Location"]["province"] = profile["province"]
    except : pass
    try:data["Location"]["country"] = profile["country"]
    except : pass
    try:data["Location"]["postalCode"] = profile["postalCode"]
    except : pass
    try:data["Contact Information"]["Email"]= profile["emailAddress"]
    except : pass
    try:data["Contact Information"]["Work"]= profile["telephone"]
    except : pass
    try:data["Contact Information"]["fax"]= profile["fax"]
    except : pass
    try:data["Current Certificate"]["Status"]= profile["corporationStatus"]["name"]
    except : pass
    try:data["Current Certificate"]["Expires"]= datetime.strptime(profile["expiryDate"].split("T")[0], "%Y-%m-%d").date().strftime("%b-%d-%Y")
    except : pass
    try:data["Current Certificate"]["Certificate History"]="First Certificate Issuance Date: " + datetime.strptime(profile["registrationDate"].split("T")[0], "%Y-%m-%d").date().strftime("%b-%d-%Y")
    except : pass
    for holder in profile["shareholders"] :
        if holder["position"]=="Managing Director":
            try:data["Managing Director"]["Name"]=holder["name"] 
            except : pass
            try:data["Managing Director"]["URL"]="https://cvo.ca.thentiacloud.net/webs/cvo/register/#/profile/"+holder["registrantId"] 
            except : pass
            break
    try: data["Page URL"] = "https://cvo.ca.thentiacloud.net/webs/cvo/register/#/corporation/"+profile["id"]
    except: pass
    cure2.execute("insert into Professional_Corporations values (?)",[json.dumps(data)])
    con2.commit()
    i += 1
    print(i)