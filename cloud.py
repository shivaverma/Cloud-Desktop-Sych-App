# Fix the space thing.
import os
import main
import shutil
import random
import filecmp
import httplib,urllib
import xml.etree.ElementTree as ET

#main.LoginApp().run()
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
                  #create a list of files present on cloud
#-------------------------------------------------------------------------------
def propfind(name):
    cut = len(name)
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201","Content-Type":"application/xml"}
    con.request("PROPFIND", "/remote.php/webdav/"+name,"",h1)
    response = con.getresponse()
    data = response.read()
    root = ET.fromstring(data)
    folder=[]
    files=[]
    for child in root:
        s = urllib.unquote(child[0].text[19:])
        if len(s)>0:
            if s[-1]=='/':
                s = s[:-1]
                s = s[cut:]
                folder.append(s)
            else:
                s = s[cut:]        
                files.append(s)
    return (folder,files)
#-------------------------------------------------------------------------------
                            #delete items in T Box
#-------------------------------------------------------------------------------
def delete(i):
    if os.path.isdir(a+'/'+i):
        shutil.rmtree(a+'/'+i)
    else:
        os.remove(a+'/'+i)
#-------------------------------------------------------------------------------
                      #synch a folder from cloud to T Box
#-------------------------------------------------------------------------------
def synch_folder(st,name):
    if not name == '':
        string = st + '/' + name
        os.mkdir(a + string)
        print 'folder: ' +string+ ' created' 
        more_list = propfind(string)
        for i in more_list[0]:
            synch_folder(string,i)
        for i in more_list[1]:
            synch_file(string+'/'+i)
            
#-------------------------------------------------------------------------------
                     #synch a file from cloud to T box folder
#-------------------------------------------------------------------------------
def synch_file(name):
    f=open(a +'/'+ name,'wb')
    rand = random.randrange(9999999999)
    request_id = "shiva"+str(rand)+"verma"
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201"}
    con.request("GET", "/remote.php/webdav/"+name,'', h1)
    response = con.getresponse()
    data = response.read()
    f.write(data)
    print 'file: ' +name+ ' :' +str(response.status)
    f.close()
#-------------------------------------------------------------------------------
                       #class for Desktop T Box folder
#-------------------------------------------------------------------------------
class Node:
    def __init__(self, path, name = ''):
        self.name = name
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)
#-------------------------------------------------------------------------------
                              #main function
#-------------------------------------------------------------------------------
def main():                                   
    node = Node(a,'node')                  
    list1 = node.file_list
    list2 = propfind('')             
    map1,map2 = {'':''},{'':''}    
    for i in list1:                 
        map1[i] = i                 
    for i in list2[0]:                 
        map2[i] = i
    for i in list2[1]:                 
        map2[i] = i 
    file_to_synch = []          
    folder_to_synch = []
    item_to_delete = []

    for i in list2[0]:
        if not map1.has_key(i):
            folder_to_synch.append(i)
    for i in list2[1]:
        if not map1.has_key(i):
            file_to_synch.append(i)
    for i in list1:
        if not map2.has_key(i):
            item_to_delete.append(i)
    cloud_index = len(list2[0])+len(list2[1])
    for i in item_to_delete:
        delete(i)
    for i in folder_to_synch:
        print i
        synch_folder('',i)
    for i in file_to_synch: 
        print i
        synch_file(i)
    return cloud_index    
#-------------------------------------------------------------------------------
if __name__=="__main__":
    main()       
