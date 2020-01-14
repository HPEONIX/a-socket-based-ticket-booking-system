import mysql.connector as connector
database = connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="booking"
)

def InsertEvent(EventName,Number_Of_Seats,Host_Phone,Org_Name):
    cursor=database.cursor()
    cursor.execute("Insert into event_list(event_name,phone,search_id,org_name) values(%s,%s,%s,%s)",(EventName,str(Host_Phone),str(Host_Phone)+EventName+Org_Name,Org_Name))
    cursor.execute("Insert into seats(search_id,total_seats,seats_booked) values(%s,%s,%s)",(str(Host_Phone)+EventName+Org_Name,Number_Of_Seats,0))
    search_id=str(Host_Phone)+EventName+Org_Name
    database.commit()
    print('done')
    return search_id
    
def AvailableTickets(search_id):
    cursor=database.cursor()
    cursor.execute("select total_seats,seats_booked from seats where search_id = %s",(search_id,))
    result=cursor.fetchone()
    return int(result[0])-int(result[1])

def TotalTickets(search_id):
    cursor=database.cursor()
    cursor.execute("select total_seats,seats_booked from seats where search_id = %s",(search_id,))
    result=cursor.fetchone()
    return result[0]

def BookedTickets(search_id):
    cursor=database.cursor()
    cursor.execute("select total_seats,seats_booked from seats where search_id = %s",(search_id,))
    result=cursor.fetchone()
    return result[1]

def BookTickets(NumberTickets,search_id):
    
    remaining=AvailableTickets(search_id)
    
    cursor=database.cursor()
    
    if (int(remaining)>=int(NumberTickets)):
        cursor.execute("update seats set seats_booked = %s where search_id = %s",( int(BookedTickets(search_id)) + int(NumberTickets) , search_id ) )
        database.commit()
        return True
    else:
        # print("no enough seats for",search_id)
        return False
    
    return False

def FindId(EventName,Host_Phone,Org_Name):
    cursor=database.cursor()
    cursor.execute("select search_id from event_list where event_name=%s and phone=%s and org_name=%s",(EventName,Host_Phone,Org_Name))
    
    return cursor.fetchall()

def ListEvent():
    cursor=database.cursor()
    cursor.execute("select search_id,event_name from event_list")
    return cursor.fetchall()
    

if __name__ == "__main__":
    EventName="TV"
    Number_Of_Seats=50
    Host_Phone="1234567890"
    Org_Name="Nuller"
    search_id=str(Host_Phone)+EventName+Org_Name
    NumberTickets=0
    
    #Event_id=InsertEvent(EventName,Number_Of_Seats,Host_Phone,Org_Name)
    print(ListEvent())
    