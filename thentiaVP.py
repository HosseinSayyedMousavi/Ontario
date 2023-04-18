
import json
import sqlite3

con = sqlite3.connect('thentiacloud.db')

profiles = con.execute('select data from Veterinary_Practices').fetchall()
con2 = sqlite3.connect('thentiacloudFinal.db')
cure2 = con2.cursor()
try:
    cure2.execute("create table %s (data JSON)" % "Veterinary_Practices")
    con2.commit()
except:
    pass
i = 0
for profile in profiles:
    data = {
        "Name": '',
        "Location": {
            "street1": "",
            "street2": "",
            "street3": "",
            "city": "",
            "province": "",
            "country": "",
            "postalCode": "",
            "Latitude": "",
            "Longitude": ""
        },
        "Practice Status": "",
        "Contact Information": {
            "Work": "",
            "Email": "",
        },

        "Director": {
            "Name": "",
            "URL": ""
        },
        "Facilities": {},
        "Page URL": ""
    }
    profile = json.loads(profile[0])

    try:
        data["Name"] = profile["name"]
    except:
        pass
    try:
        data["Location"]["street1"] = profile["street1"]
    except:
        pass
    try:
        data["Location"]["street2"] = profile["street2"]
    except:
        pass
    try:
        data["Location"]["street3"] = profile["street3"]
    except:
        pass
    try:
        data["Location"]["city"] = profile["city"]
    except:
        pass
    try:
        data["Location"]["province"] = profile["province"]
    except:
        pass
    try:
        data["Location"]["country"] = profile["country"]
    except:
        pass
    try:
        data["Location"]["postalCode"] = profile["postalCode"]
    except:
        pass
    try:
        data["Practice Status"] = profile["organizationType"]
    except:
        pass
    try:
        data["Contact Information"]["Email"] = profile["emailAddress"]
    except:
        pass
    try:
        data["Contact Information"]["Work"] = profile["telephone"]
    except:
        pass
    try:
        data["Director"]["Name"] = profile["employmentDetails"]["registrant"]["name"]
    except:
        pass
    try:
        data["Director"]["URL"] = "https://cvo.ca.thentiacloud.net/webs/cvo/register/#/profile/" + \
            profile["employmentDetails"]["registrant"]["id"]
    except:
        pass
    try:
        j=0
        for facility in profile["facilityDetails"] :
            j+=1
            data["Facilities"]["Facility "+str(j)] = {}
            data["Facilities"]["Facility "+str(j)]["Name"]=facility["category"]
            data["Facilities"]["Facility "+str(j)]["Certificate Expires on"] = facility["expiryDate"]
            for notice in profile["noticeDetails"]:
                if notice["facilityId"]== facility["id"]:
                    data["Facilities"]["Facility "+str(j)][notice["publicNoticeType"]] = notice["decisionReasons"]
    except:
        pass
    try:
        data["Page URL"] = "https://cvo.ca.thentiacloud.net/webs/cvo/register/#/organization/"+profile["id"]
    except:
        pass
    cure2.execute("insert into Veterinary_Practices values (?)",
                  [json.dumps(data)])
    con2.commit()
    i += 1
    print(i)
