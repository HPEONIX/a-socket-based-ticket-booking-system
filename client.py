import socket
import json

def commuicate(host, port,message):
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    # print(message)
    client_socket.send(message.encode())
    response=client_socket.recv(1024).decode()
    client_socket.close() # close the connection
    return response

def ping(host, port):
    req={
        "op":"ping",
        "arg":{}
        }
    res=json.loads(commuicate(host, port,message=json.dumps(req)))
    res_dat=res['data']
    print(res_dat,end="\n\n")
    
def get_all_event(host,port):
    req={
        "op":"list",
        "arg":{}
        }
    res=json.loads(commuicate(host, port,message=json.dumps(req)))
    res_dat=res['data']
    return res_dat

def get_no_of_seat(host,port,event_id):
    req={
        "op":"seats",
        "arg":{"EventID":event_id}
        }
    res=json.loads(commuicate(host, port,message=json.dumps(req)))
    res_dat=res['data']
    return res_dat

def book_ticket(host,port,event_id,seats_to_book):
    req={
        "op":"book",
        "arg":{"EventID":event_id,"BookingSeats":seats_to_book}
        }
    res=json.loads(commuicate(host, port,message=json.dumps(req)))
    res_dat=res['data']
    return res_dat

def add_event_to_list(host,port,EventName,Number_Of_Seats,Host_Phone,Org_Name):
    req={
        "op":"addEvent",
        "arg":{"Name":EventName,"MaxTicket":Number_Of_Seats,"Phone":Host_Phone,"OrgName":Org_Name}
        }
    res=json.loads(commuicate(host, port,message=json.dumps(req)))
    res_dat=res['data']
    return res_dat

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    message="ping"
    ping(host, port)
    
    while message.strip().lower()!="0":
        
        print("""
        option (Enter Number)
        ===================
        1 => book tickets
        2 => show events
        3 => create events
        0 => exit
        ===================
        """)
        
        message = input("input -> ")  # take input
        
        if message.lower().strip()=='1':
            
            #print("todo: show list of events")
            
            res_dat=get_all_event(host,port)
            
            print("""
                  Index \t Id \t\t Name
                  ======\t====\t\t=====
                  """)
            for i,v in enumerate(res_dat):
                print("\t",i," \t ",v[0]," \t ",v[1])
                
            print()
            index=input("enter Index of event you want to book for or enter -ve to exit\n->")
            
            while( int( (index.strip().split())[0] ) >= len(res_dat)):
                index=input("invalid input: value should be less than " + str(len(res_dat)) +"\nenter Index of event you want to book for or enter -ve to exit\n->")
            if( int( (index.strip().split())[0] ) <0):
                print("\nexiting\n")
            else:
                selected=res_dat[ int( (index.strip().split())[0] ) ]
                event_id=selected[0]
                seat_counts=get_no_of_seat(host,port,event_id)
                print("""
                  Total \t Available \t Booked
                  ===== \t ========= \t ======
                """)
                print("\t",seat_counts["total"],seat_counts["available"],seat_counts["booked"],sep="\t",end="\n\n")
                
                # check no of seats from user
                
                bookin_seats=input("enter no of seats you want to book (enter 0 or lesser to exit)\n->")
                
                seat_counts=get_no_of_seat(host,port,event_id)
                
                while( int( (bookin_seats.strip().split())[0] ) > seat_counts["available"]):
                    
                    print("invalid input: value should be less than"+seat_counts["available"],end="\n\n")
                    print("""
                      Total \t Available \t Booked
                      ===== \t ========= \t ======
                      """)
                    print("\t",seat_counts["total"],seat_counts["available"],seat_counts["booked"],sep="\t")
                
                    bookin_seats=input("enter no of seats you want to book (enter 0 or lesser to exit)\n->")
                    seat_counts=get_no_of_seat(host,port,event_id)
                    
                if(int( (bookin_seats.strip().split())[0] ) <= 0):
                    print("\nexiting\n")
                else:
                    # print("book no of tickets")
                    success=book_ticket(host,port,event_id,seats_to_book=bookin_seats)
                    print(success)
                
        if message.lower().strip()=='2':
            
            #print("todo: show list of events")
            res_dat=get_all_event(host,port)
            
            print(""""
                  Index \t Id \t\t Name"
                  ======\t====\t\t=====
                  """)
            for i,v in enumerate(res_dat):
                print(i," \t ",v[0]," \t ",v[1])
            print()
            
        if message.lower().strip()=='3':
            
            # print("todo: get details and create event")
            org_name=input("\nenter organization name\n->")
            while(org_name.strip()==""):
                org_name=input("\nenter organization name (white spaces not accepted)\n->")
                
            phone=input("\nenter organization phone number\n->")
            while(phone.strip()=="" or not phone.isdigit()):
                phone=input("\nenter organization phone number (white spaces not accepted)\n->")
                
            event_name=input("\nenter event name\n->")
            while(event_name.strip()==""):
                event_name=input("\nenter event name (white spaces not accepted)\n->")
                
            max_ticket=input("\nenter maximum number of tickets\n->")
            while(max_ticket.strip()=="" or not max_ticket.isdigit()):
                max_ticket=input("\nenter maximum number of tickets (white spaces not accepted)\n->")
            
            print("\ncode:",add_event_to_list(host, port, EventName=event_name, Number_Of_Seats=max_ticket, Host_Phone=phone, Org_Name=org_name),end="\n\n")
            
        
    


if __name__ == '__main__':
    client_program()
