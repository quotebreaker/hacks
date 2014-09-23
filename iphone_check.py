import urllib2
import json
import smtplib
import sys

FROM = "team@quotebreaker.com"
TO = ["user1@gmail.com","user2@gmail.com"]
username = "<gmail account username>"
password = "<gmail account password>"
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)

TYPE = sys.argv[1]

zip = "94085"
part = "MGAV2LL/A" #This means ATT iPhone 6 Plus Silver 64 GB
url = "http://store.apple.com/us/retailStore/availabilitySearch?parts.0="+part+"&zip="+zip

response = urllib2.urlopen(url).read().decode("utf-8")
resJson = json.loads(response)

resBody = resJson["body"]
stores = resBody["stores"]
availableStores = []
found = False
for store in stores:
        storeName = store["storeName"]
        phoneObj = store["partsAvailability"]
        phone = phoneObj[part]
        available = phone["storeSelectionEnabled"]
        if available:
                found = True
                message = storeName + "- Phone available"
                availableStores.append("\n***"+message+"***\n")
        else:
                message = storeName + "- Phone not available"
                availableStores.append(message)
TEXT = "\n".join(availableStores)
if found:
        SUBJECT = "ACT FAST: Found Phone 6 plus 64GB Silver"
else:
        SUBJECT = "iPhone 6 plus 64GB Silver - Availability status"

EMAIL_CONTENT = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

if TYPE == "0":
        if found:
                server.sendmail(FROM, TO,EMAIL_CONTENT)
        else:
                print "iPhone not available in your search area"
else:
        server.sendmail(FROM, TO,EMAIL_CONTENT)

server.quit()
