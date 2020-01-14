import socket
from _thread import start_new_thread
import data_interface as interface
import json

def adaptrcv(c,addr):
    rcv=c.recv(1024).decode()
    print(addr," >> ",rcv)
    data=json.loads(rcv)
    res={"data":{}}
    
    op=data['op']
    arg=data['arg']
    
    if(op=="ping"):
        res={"data":"server online"}
    
    if(op=="list"):
        res={"data":interface.ListEvent()}
        
    if(op=="seats"):
        search_id=arg["EventID"]
        res={"data":{"total":interface.TotalTickets(search_id),"available":interface.AvailableTickets(search_id),"booked":interface.BookedTickets(search_id)}}
        
    if(op=="book"):
        # print("works")
        search_id=arg["EventID"]
        NumberTickets=arg["BookingSeats"]
        try:
            if(interface.BookTickets(NumberTickets, search_id)):
                res={"data":"booking successfull"}
            else:
                res={"data":"booking unsuccessfull try again later"}
        except Exception as e:
            print(e)
            res={"data":"booking unsuccessfull try again later (error occured)"}
            
    if(op=="addEvent"):
        try:
            res={"data":interface.InsertEvent(arg["Name"], arg["MaxTicket"], arg["Phone"], arg["OrgName"])}
        except Exception as e:
            print(e)
            res={"data":"event adding unsuccessfull try chainging parameter (error occured)"}
        
    print(addr," << ",json.dumps(res))
    c.send(json.dumps(res).encode())
    
    c.close()



if __name__ == "__main__":
    port=5000
    host = socket.gethostname()
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    
    sock.bind((host,port))
    sock.listen(5)
    while True:
        c,addr=sock.accept()
        start_new_thread(adaptrcv,(c,addr))
    sock.close()