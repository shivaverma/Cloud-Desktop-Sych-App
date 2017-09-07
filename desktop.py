# Fix the space thing.
import os
import shutil
import random
import filecmp
import chunking
import httplib,urllib
import xml.etree.ElementTree as ET

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
def propfind():
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201","Content-Type":"application/xml"}
    con.request("PROPFIND", "/remote.php/webdav/","",h1)
    response = con.getresponse()
    data=response.read()
    root = ET.fromstring(data)
    all_names=[]
    for child in root:
        s = urllib.unquote(child[0].text[19:])
        if len(s)>0:
            if s[-1]=='/':
                s = s[:-1]
        all_names.append(s)
    all_names.pop(0)
    return all_names
#-------------------------------------------------------------------------------
                       #add a folder to cloud from T Box
#-------------------------------------------------------------------------------
def add_folder(st,name):
    string = st + '/' + name
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201"}
    con.request("MKCOL", "/remote.php/webdav/"+string,'',h1)
    response = con.getresponse()
    response.read()
    print 'folder: ' +string+ ' : ' +str(response.status)
    path = os.path.abspath(a+string)
    file_list = os.listdir(path)
    for i in file_list:
        if os.path.isdir(a+string+'/'+i):
            add_folder(string,i)          
        else:
            media = os.stat(a+'/'+string+'/'+i)
            size = media.st_size/(1024*1024)
            if (size>90):
                chunking.chunking(string,i)
            else:      
                add_file(string+'/'+i)
            
#-------------------------------------------------------------------------------
                   #add a file to cloud from T box folder
#-------------------------------------------------------------------------------
def add_file(name):
    f=open(a +'/'+ name,'rb')
    rand = random.randrange(9999999999)
    request_id = "shiva"+str(rand)+"verma"
    b1=f.read()
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201"}
    con.request("PUT", "/remote.php/webdav/"+name, b1, h1)
    response = con.getresponse()
    response.read()
    print 'file: ' +name+ ' :' +str(response.status)
    f.close()
#-------------------------------------------------------------------------------
                        #delete a file or folder on cloud
#-------------------------------------------------------------------------------
def delete_file(name):
    rand = random.randrange(9999999999)
    request_id = "shiva"+str(rand)+"verma"
    h1 = {"X-RequestId":request_id,"X-UserId":a,"X-SessionId":session_id,"X-DeviceId":"T12111611000201"}
    con.request("DELETE", "/remote.php/webdav/"+name,"",h1)
    response = con.getresponse()
    response.read()
    print 'file: ' +name+ ' : '+str(response.status)
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
    node = Node(a,'node')           #-------------------------------------------
    list1 = node.file_list          # List of files in T Box.
    list2 = propfind()              # List of files in cloud.
    map1,map2 = {'':''},{'':''}     # Dictionaries correspondence to list.
    for i in list1:                 # Creating Dictionaries from list.
        map1[i] = i                 #-------------------------------------------
    for i in list2:
        map2[i] = i                
    file_to_added = []              #-------------------------------------------
    folder_to_added = []            # Files in Desktop but not in cloud
    file_to_deleted = []            # Files in cloud but not in Desktop
    folder_to_deleted = []          # Creating files to be added or deleted  
                                    #------------------------------------------- 
    for i in list1:                 
        if not map2.has_key(i):     
            if os.path.isdir(a+'/'+i):
                folder_to_added.append(i)
            else:    
                file_to_added.append(i)

    for i in list2:
        if not map1.has_key(i):
            if os.path.isdir(a+'/'+i):
                folder_to_deleted.append(i)
            else:
                file_to_deleted.append(i)
    for i in file_to_added: 
        media = os.stat(a+'/'+i)
        size = media.st_size/(1024*1024)
        if (size>90):
            chunking.chunking('',i)
        else:
            add_file(i)
    for i in file_to_deleted:
        delete_file(i)
    for i in folder_to_added:
        add_folder('',i)
    for i in folder_to_deleted:
        delete_file(i)
#-------------------------------------------------------------------------------
if __name__=="__main__":
    main()
