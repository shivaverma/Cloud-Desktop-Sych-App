import os
import time
import cloud
import shutil
import random
import desktop
import filecmp
import httplib,urllib
import xml.etree.ElementTree as ET

cloud_index = 0
desktop_index = 0

a = 'bajju7@gmail.com' 
b = 'cloudtron' 
#-------------------------------------------------------------------------------
                      #user authentication processure
#-------------------------------------------------------------------------------
user = '"' + a + '"'
passw = '"' + b + '"'     
rand = random.randrange(9999999999)
request_id = "shiva"+str(rand)+"verma"
b ="{\"requestPayload\":{\"userid\":"+ user + ",\"password\":"+passw+",\"realm\":\"Smartron\"}}"
h =  {"X-RequestId": request_id,"X-MessageType": "userauth ","X-CloudtronProtocolVersion": "1.0","X-DeviceId": "T12111611000201","Content-Type": "application/json"}
con=httplib.HTTPConnection("cloudint.smartron.com")
con.request("POST","/index.php/",b,h)
response = con.getresponse()
data = response.read()
response_id = data[68:98]
session_id = data[201:231]

#-------------------------------------------------------------------------------
def check_update():
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201","Content-Type":"application/xml"}
    con.request("PROPFIND", "/remote.php/webdav/","",h1)
    response = con.getresponse()
    data=response.read()
    root = ET.fromstring(data)
    cloud_number = 0
    for child in root:
        cloud_number+=1
    path = os.path.abspath(a)
    list_ = os.listdir(path)    
    return (cloud_number-1,len(list_))

#-------------------------------------------------------------------------------
                  #create a list of files present on cloud
#-------------------------------------------------------------------------------
if __name__=='__main__':
    index = cloud.main()
    cloud_index = index
    desktop_index = index
    while(1):
        index = check_update()
        if index[0] != cloud_index:
            cloud.main()
            cloud_index = index[0]
            desktop_index = cloud_index
        elif index[1] != desktop_index:
            desktop.main()
            desktop_index = index[1]
            cloud_index = desktop_index
        time.sleep(20) 
        

    
    
    
