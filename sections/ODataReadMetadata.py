import urllib2, base64
username = "user_name_here"
password = "password_here"
request = urllib2.Request("https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/$metadata")

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

content = result.read()

print(content)
