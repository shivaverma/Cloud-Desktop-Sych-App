import httplib,urllib
import random
import time
import chunk
import os

a = 'bajju7@gmail.com' 
b = 'cloudtron' 

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

def chunking(string,name,default_mb = 8):
    media_name = name
    mb = default_mb

    chunk_size = mb*1024*1024
    media = os.stat(a+'/'+string+'/'+media_name)
    size = media.st_size/(1024*1024)
    chunk_count = size/mb + 1
    print ""
    print "size of selected media is: "+str(size)+" mb"
    print "number of chunks are: " +str(chunk_count)
    print ""
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201","OC-Chunked":"1"}
    while 1:
        try:
           f = open(a+'/'+string+'/'+media_name,'rb')
           break
        except IOError:
            print 'wait while media copying..'
            time.sleep(1.5)
    count = 1
    while True:
        data = f.read(chunk_size)
        if data == '':
            break
        rand1 = random.randrange(99999)
        con.request("PUT", "/remote.php/webdav/"+string+'/'+media_name+"-chunking-"+"5668"+"-"+str(chunk_count)+"-"+str(count-1),data,h1)
        response = con.getresponse()
        response.read()
        if response.status == 201:
            print str(mb*count) + 'mb file uploaded uploaded...'
        else:
            print response.status
        count+=1
    f.close()





