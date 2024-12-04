import pymysql
import random
from datetime import datetime
import time


# INITIALISATION of database network, cursor, tempfile
db=pymysql.connect(host='localhost',user='root',password='12APRIL2002')
Curry=db.cursor()
tempfile={
    'accesstype':None,
    'logintype':None,
    'username':None,
    'EncPass':None,
    'roomNO':None,
    'roomID':None,
}

'''
APPENDIX.
<comments> All user defined functions here
branch: Haneef
'''

# XOR Encryption/Decryption
def xor_encrypt(password, key):
    key_bytes = key.to_bytes(4, 'big')
    password_bytes = password.encode('utf-8')
    key_repeated = key_bytes * (len(password_bytes) // 4) + key_bytes[:len(password_bytes) % 4]
    encrypted_bytes = bytearray()
    for i in range(len(password_bytes)):
        encrypted_bytes.append(password_bytes[i] ^ key_repeated[i])

    return encrypted_bytes.hex()

def xor_decrypt(encrypted_password, key):
    key_bytes = key.to_bytes(4, 'big')
    encrypted_bytes = bytes.fromhex(encrypted_password)
    key_repeated = key_bytes * (len(encrypted_bytes) // 4) + key_bytes[:len(encrypted_bytes) % 4]
    decrypted_bytes = bytearray()
    for i in range(len(encrypted_bytes)):
        decrypted_bytes.append(encrypted_bytes[i] ^ key_repeated[i])

    return decrypted_bytes.decode('utf-8')

def add(TABLE):
    if TABLE=="ROOMS":
        while True:
            try:
                Room_ID=input("Enter Room ID (3 Numbers/charecters): ")
                Room_Type=input("Enter Room Type (40 Charecters max.): ")
                PricePN=int(input("Enter Price per night (integral) in INR: "))
                Occ=int(input("Enter maximum occupancy (integral): "))
                Amenities=input("Enter available services (700 charecters or less): ")
                Tot=int(input("Enter total no. of rooms (integral): "))
                Curry.execute("SELECT MAX(Beginning_no) FROM ROOMS")
                Tbeg=Curry.fetchone(); Tbeg=Tbeg[0]
                Curry.execute("SELECT Total_Rooms FROM ROOMS WHERE Beginning_no="+str(Tbeg))
                Ttot=Curry.fetchone(); Ttot=Ttot[0]
                Beg=int(Tbeg)+int(Ttot)
                Curry.execute(f"""
                    INSERT INTO ROOMS VALUES(
                        '{Room_ID}','{Room_Type}',{PricePN},{Occ},'{Amenities}',{Tot},{Tot},{Beg},NULL
                    )
                """)
                db.commit()
                break
            except:
                print("<!> Invalid Entry. Kindly retry.")
    elif TABLE=="EXTRAS":
        while True:
            try:
                Service_Code=input("Enter Servic Code (6 characters): ")
                Service_Name=input("Enter Servic Name (50 Numbers/characters): ")
                Cost_Per_Unit=int(input("Enter Cost Per Unit: "))
                Description=input("Enter Description (255 characters max): ")
                Curry.execute(f"""
                    INSERT INTO EXTRAS VALUES(
                        '{Service_Code}','{Service_Name}',{Cost_Per_Unit},'{Description}'
                    )
                """)
                db.commit()
                break
            except:
                print("<!> Invalid Entry. Kindly retry.")
    elif TABLE=="MENU":
        while True:
            try:
                Item_ID=input("Enter Item ID (6 characters): ")
                Item_Name=input("Enter Item Name (50 Numbers/characters): ")
                Category=int(input("Enter Category (30 charecters): "))
                Price=input("Enter Price (integral): ")
                Curry.execute(f"""
                    INSERT INTO MENU VALUES(
                        '{Item_ID}','{Item_Name_Name}','{Category}',{Price}
                    )
                """)
                db.commit()
                break
            except:
                print("<!> Invalid Entry. Kindly retry.")

def show(TABLE):
    Curry.execute("SELECT * FROM", TABLE)
    records=Curry.fetchall()
    header = [desc[0] for desc in Curry.description]
    column_widths = [max(len(str(row[i])) for row in records) if records else 0 for i in range(len(headers))]
    column_widths = [max(len(header), width) for header, width in zip(headers, column_widths)]
    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))
    for record in records:
        row = " | ".join(str(value).ljust(width) for value, width in zip(record, column_widths))
        print(row)

def delete(TABLE):
    if TABLE=="ROOMS":
        try:
            PrimaryID=input("Kindly enter the Room_ID TO BE DELETED")
            Curry.execute("DELETE FROM ROOMS WHERE Room_ID="+str(PrimaryID))
            db.commit()
        except:
            print("<!> Action could not be proceeded with. Kindly check the ID/Code entered.")
    elif TABLE=="CUSTOMERS":
        try:
            PrimaryID=input("Kindly enter the Customer_ID TO BE DELETED")
            Curry.execute("SELECT Room_ID FROM CUSTOMERS WHERE Customer_ID="+str(PrimaryID))
            rec=Curry.fetchone[0]
            Curry.execute(f"SELECT * FROM CUSTOMERS WHERE Customer_ID={PrimaryID}")
            Prec=Curry.fetchone()
            Curry.execute(f"INSERT INTO PREVCUSTOMERS VALUES {Prec}")
            db.commit()
            Curry.execute("DELETE FROM CUSTOMERS WHERE Customer_ID="+str(PrimaryID))
            Curry.execute("UPDATE ROOMS SET Available_Rooms=Available_Rooms+1 WHERE Room_ID="+str(rec))
            Curry.execute("SELECT Beginning_no, Latest_used_no FROM ROOMS WHERE Room_ID="+str(rec))
            Trec=Curry.fetchone()
            if Trec[0]==Trec[1]:
                Curry.execute("UPDATE ROOMS SET Latest_used_no=NULL WHERE Room_ID="+str(rec))
            else:
                Curry.execute("UPDATE ROOMS SET Latest_used_no=Latest_used_no-1 WHERE Room_ID="+str(rec))
            db.commit()
        except:
            print("<!> Action could not be proceeded with. Kindly check the ID/Code entered.")
    elif TABLE=="EXTRAS":
        try:
            PrimaryID=input("Kindly enter the Service_Code TO BE DELETED")
            Curry.execute("DELETE FROM EXTRAS WHERE Service_Code="+str(PrimaryID))
            db.commit()
        except:
            print("<!> Action could not be proceeded with. Kindly check the ID/Code entered.")
    elif TABLE=="MENU":
        try:
            PrimaryID=input("Kindly enter the Item_ID TO BE DELETED")
            Curry.execute("DELETE FROM MENU WHERE Item_ID="+str(PrimaryID))
            db.commit()
        except:
            print("<!> Action could not be proceeded with. Kindly check the ID/Code entered.")

def edit(TABLE):
    if TABLE=="ROOMS":
        while True:
            try:
                Curry.execute(f"DESCRIBE {TABLE}")
                desc=Curry.fetchall()
                print("column name, column parameter (type)")
                for col in desc:
                    print(col[0],",",col[1],", NULL:",col[2])
                Atr=input("Enter the name of the column to be changed: ")
                show(TABLE)
                rID=input("Enter the Room_ID of the record to be changed (Enter 'all' if all records are to be altered): ")
                if rID.lower()!="all":
                    Curry.execute(f"SELECT {Atr} FROM ROOMS WHERE Room_ID={rID}")
                    print("Old value:",Curry.fetchone())
                for col in desc:
                    if "int" in col[1]:
                        alt=int(input("Enter new value (integral): "))
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE ROOMS SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE ROOMS SET {Atr}={alt} WHERE Room_ID={rID}")
                    elif "varchar" in col[1]:
                        alt=input(f"Enter new value (maximum {col[1][8:][:-1]} charecters): ")
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE ROOMS SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE ROOMS SET {Atr}={alt} WHERE Room_ID={rID}")
                    else:
                        alt=input(f"Enter new value (exactly {col[1][5:][:-1]} charecters): ")
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE ROOMS SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE ROOMS SET {Atr}={alt} WHERE Room_ID={rID}")
                db.commit()
                print("Successfully updated!")
                break
            except:
                print("<!> Invalid Entry. Kindly retry.")
    elif TABLE=="EXTRAS":
        while True:
            try:
                Curry.execute(f"DESCRIBE {TABLE}")
                desc=Curry.fetchall()
                print("column name, column parameter (type)")
                for col in desc:
                    print(col[0],",",col[1],", NULL:",col[2])
                Atr=input("Enter the name of the column to be changed: ")
                show(TABLE)
                eID=input("Enter the Service_Code of the record to be changed (Enter 'all' if all records are to be altered): ")
                if eID.lower()!='all':
                    Curry.execute(f"SELECT {Atr} FROM EXTRAS WHERE Service_Code={eID}")
                    print("Old value:",Curry.fetchone())
                for col in desc:
                    if "int" in col[1]:
                        alt=int(input("Enter new value (integral): "))
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE EXTRAS SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE EXTRAS SET {Atr}={alt} WHERE Service_Code={eID}")
                    elif "varchar" in col[1]:
                        alt=input(f"Enter new value (maximum {col[1][8:][:-1]} charecters): ")
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE EXTRAS SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE EXTRAS SET {Atr}={alt} WHERE Service_Code={eID}")
                    else:
                        alt=input(f"Enter new value (exactly {col[1][5:][:-1]} charecters): ")
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE EXTRAS SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE EXTRAS SET {Atr}={alt} WHERE Service_Code={eID}")
                db.commit()
                print("Successfully updated!")
                break
            except:
                print("<!> Invalid Entry. Kindly retry.")
    if TABLE=="MENU":
        while True:
            try:
                Curry.execute(f"DESCRIBE {TABLE}")
                desc=Curry.fetchall()
                print("column name, column parameter (type)")
                for col in desc:
                    print(col[0],",",col[1],", NULL:",col[2])
                Atr=input("Enter the name of the column to be changed: ")
                show(TABLE)
                iID=input("Enter the Item_ID of the record to be changed (Enter 'all' if all records are to be altered): ")
                if iID.lower()!="all":
                    Curry.execute(f"SELECT {Atr} FROM MENU WHERE Item_ID={iID}")
                    print("Old value:",Curry.fetchone())
                for col in desc:
                    if "int" in col[1]:
                        alt=int(input("Enter new value (integral): "))
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE MENU SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE MENU SET {Atr}={alt} WHERE Item_ID={iID}")
                    elif "varchar" in col[1]:
                        alt=input(f"Enter new value (maximum {col[1][8:][:-1]} charecters): ")
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE MENU SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE MENU SET {Atr}={alt} WHERE Item_ID={iID}")
                    else:
                        alt=input(f"Enter new value (exactly {col[1][5:][:-1]} charecters): ")
                        if rID.lower()=="all":
                            Curry.execute(f"UPDATE MENU SET {Atr}={alt}")
                        else:
                            Curry.execute(f"UPDATE MENU SET {Atr}={alt} WHERE Item_ID={iID}")
                db.commit()
                print("Successfully updated!")
                break
            except:
                print("<!> Invalid Entry. Kindly retry.")


def register():
    CustomerName=input("Enter vistor name: ")
    while True:
        try:
            PhoneNo=int(input("Enter phone number: "))
            if len(str(PhoneNo))==10:
                break
            else:
                print("<!> Invalid Phone number.")
        except:
            print("<!> Invalid Phone number.")
    Email=input("Enter email: ")
    Curry.execute("SELECT * FROM ROOMS")
    ROOMS=Curry.fetchall()
    RoomID=[]
    print("\n================= Available Rooms =================\n")
    for room in ROOMS:
        room_id, room_type, price, max_occupancy, amenities = room
        RoomID.append(room_id)

        print(f"Room ID:           {room_id}")
        print(f"Room Type:         {room_type}")
        print(f"Price per Night:   ₹{price}")
        print(f"Max Occupancy:     {max_occupancy} Person(s)")
        print(f"Amenities:         {amenities}")
        print("\n" + "-" * 50 + "\n")
    while True:
        try:
            roomID=int(input("Enter room ID of room of choice: "))
            if roomID in RoomID:
                break
            else:
                print("<!> RoomID is invalid.")
        except:
            print("<!> RoomID is invalid.")
    tempfile['roomID']=roomID
    while True:
        try:
            NON=int(input("Enter number of nights of stay: "))
            break
        except:
            print("<!> Invalid, kindly use integers only.")
    Curry.execute("SELECT Customer_ID FROM CUSTOMERS")
    CIDs=Curry.fetchall()
    while True:
        CID='C'+str(random.randint(10000, 99999))
        for i in CIDs:
            for j in i:
                if j==CID:
                    break
            else:
                break
        else:
            break
    Curry.execute("SELECT * FROM ROOMS WHERE Room_ID="+str(roomID))
    CROOM=Curry.fetchall()
    tempfile['username']=CID
    if CROOM[0][8]==None:
        roomNO=CROOM[0][7]
    else:
        roomNO=CROOM[0][8]+1
    tempfile['roomNO']=roomNO
    Curry.execute("UPDATE ROOMS SET Available_Rooms=Available_Rooms-1, Latest_used_no="+str(roomNo)+" WHERE RoomID="+str(roomID))
    db.commit()
    room_bill=int(CROOM[2])*NON

    Curry.execute("SELECT * FROM EXTRAS")
    extras = Curry.fetchall()
    print("=" * 25 + " Available Extras " + "=" * 25)
    for extra in extras:
        print(f"Service Code:    {extra[0]}")
        print(f"Service Name:    {extra[1]}")
        print(f"Cost per Unit:   ₹{extra[2]}")
        print(f"Description:     {extra[3]}")
        print("-" * 50)
    service_dict = {}
    for service in extras:
        service_dict[service[0]]=int(service[2])
    codeschosen = input("Enter service codes separated by commas (e.g., SVC004, SVC006): ")
    entered_codes = []
    for code in codeschosen.split(","):
        entered_codes.append(code.strip())
    valid_codes = []
    extra_costs = 0
    for code in entered_codes:
        if code in service_dict:
            valid_codes.append(code)
            extra_costs += service_dict[code]
        else:
            print(f"Invalid service code: {code}")
    valid_codes_string = ", ".join(valid_codes)

    # FINALLY!!!! TIME TO INSERT THE CUSTOMER, IT WAS SO CUMBERSOME!!!!!!!!
    Curry.execute("INSERT INTO CUSTOMERS VALUES ("+str(CID)+", "+CustomerName+", "+str(PhoneNo)+", "+Email+", "+str(roomID)+", "+str(CROOM[1])+", "+str(roomNO)+", CURDATE(), DATE_ADD(CURDATE(), INTERVAL "+str(NON)+" DAY), "+str(NON)+", "+str(room_bill)+", "+str(extra_costs)+", "+str(room_bill+extra_costs)+", "+valid_codes_string+")")
    db.commit()

def login():
    while True:
        print("\n"*2)
        tYPE=input("<𝑳> Enter login type (A:Admin, C:Customer): ").upper()
        if tYPE in ['A','C']:
            break
        else:
            print("<!> Invalid type. Use 'A' or 'C' ONLY.")
    tempfile['accesstype']=tYPE
    if tYPE=='A':
        while True:
            name=input("Enter adminID: ")
            Curry.execute("SELECT Admin_ID FROM ADMINS")
            Names=list(Curry.fetchall())
            if "('"+name+"',)" in Names:
                break
            else:
                print("<!> Invalid. Admin with name",name,"does not exist.")
        tempfile['username']=name
        Curry.execute("SELECT EncPass from ADMINS WHERE Admin_ID="+name)
        result=Curry.fetchone()
        tempfile['EncPass']=result[0]
        seclock=5
        while True:
            if seclock==0:
                Curry.close()
                exit()
            password=input("Enter password: ")
            passkey=input("Enter key: ")
            try:
                DecPass = xor_decrypt(tempfile['EncPass'],int(passkey))
                if password == DecPass:
                    print("<#> Successful login!")
                    break
                else:
                    print("<!> Invalid Passkey and/or password.",seclock-1,"attemps left.")
            except:
                print("<!> Invalid Passkey and/or password.",seclock-1,"attemps left.")
            seclock-=1
    elif tYPE=='C':
        while True:
            loginType=input("Login(L)/Register(R)? ").upper()
            if loginType in ['L','R']:
                break
        tempfile['logintype']=loginType
        if loginType=='L':
            while True:
                name=input("Enter userID: ")
                Curry.execute("SELECT Customer_ID FROM CUSTOMERS")
                Names=list(Curry.fetchall())
                if "('"+name+"',)" in Names:
                    print("<#> Successful login!")
                    break
                else:
                    print("<!> Invalid. Visitor with ID",name,"does not exist.")
            tempfile['username']=name
            Curry.execute("SELECT Customer_ID FROM PREVCUSTOMERS")
            Names=list(Curry.fetchall())
            if "('"+name+"',)" in Names:
                print("Welcome Back!",name)
        else:
            register()

def CustomerDashboard(CID):
    Curry.execute("SELECT Customer_ID FROM PREVCUSTOMERS")
    Pervs=Curry.fetchall()
    if f'({CID},)' in Pervs:
        print(f"\n------------------- Billing Information ---------------------")
        print(f"Room Bill:            ₹{customer[10]}")
        print(f"Extra Costs:          ₹{customer[11]}")
        print(f"Total Bill:           ₹{customer[12]}")
        print("\nKindly Note that all payments must be made under 30 days of cancellation. Thank you for choosing us!")
        Curry.execute("DELETE FROM CUSTOMERS WHERE Customer_ID="+str(CID))
        Curry.execute("UPDATE ROOMS SET Available_Rooms=Available_Rooms+1 WHERE Room_ID="+str(customer[4]))
        Curry.execute("SELECT Beginning_no, Latest_used_no FROM ROOMS WHERE Room_ID="+str(customer[4]))
        Trec=Curry.fetchone()
        if Trec[0]==Trec[1]:
            Curry.execute("UPDATE ROOMS SET Latest_used_no=NULL WHERE Room_ID="+str(customer[4]))
        else:
            Curry.execute("UPDATE ROOMS SET Latest_used_no=Latest_used_no-1 WHERE Room_ID="+str(customer[4]))
        db.commit()
    while True:
        Curry.execute("SELECT * FROM CUSTOMERS WHERE Customer_ID="+str(CID))
        customer=Curry.fetchone()
        now = datetime.now()
        formatted_date = now.strftime("%A, %d %B, %Y")
        print("\n"*10)
        print(f"{'Customer Dashboard':<50}{formatted_date:>50}",end='\n\n')
        print("CUSTOMER ID:",user[0])
        print(f"--------------------- Customer Information --------------------")
        print(f"Name:                 {customer[1]}")
        print(f"Contact Number:       {customer[2]}")
        print(f"Email:                {customer[3]}")
        print(f"\n------------------- Room Information ------------------------")
        print(f"Room ID:              {customer[4]}")
        print(f"Room Number:          {customer[6]}")
        print(f"Room Type:            {customer[5]}")
        print(f"Check-in Date:        {customer[7]}")
        print(f"Check-out Date:       {customer[8]}")
        print(f"Number of Nights:     {customer[9]}")
        print(f"\n------------------- Billing Information ---------------------")
        print(f"Room Bill:            ₹{customer[10]}")
        print(f"Extra Costs:          ₹{customer[11]}")
        print(f"Total Bill:           ₹{customer[12]}")
        print(f"\n------------------- Services --------------------------------")
        print(f"Services Used:        {customer[13]}")

        while True:
            ask=input("\n\nActions:\n1:Resturant Orders\n2:Log-out\n3:Quit\n4:Cancellation(No refund)\n\n<?> ")
            if ask in ['1','2','3','4']:
                break
            else:
                print("<!> Invalid action, try again.")
        if ask=='2':
            break
        elif ask=='3':
            Curry.close()
            exit()
        elif ask=='4':
            Conf=input("NO REFUND POLICY: Please note that all payments made for bookings, services, and products are non-refundable. Once\na transaction has been completed, no refunds will be issued, regardless of any changes to your plans or circumstances.\nThank you for your understanding.\n\nAre you sure you want to proceed with cancellation?(Y/N) ").upper()
            if Conf=='Y':
                print(f"\n------------------- Billing Information ---------------------")
                print(f"Room Bill:            ₹{customer[10]}")
                print(f"Extra Costs:          ₹{customer[11]}")
                print(f"Total Bill:           ₹{customer[12]}")
                print("\nKindly Note that all payments must be made under 30 days of cancellation. Thank you for choosing us!")
                Curry.execute("DELETE FROM CUSTOMERS WHERE Customer_ID="+str(CID))
                Curry.execute("UPDATE ROOMS SET Available_Rooms=Available_Rooms+1 WHERE Room_ID="+str(customer[4]))
                Curry.execute("SELECT Beginning_no, Latest_used_no FROM ROOMS WHERE Room_ID="+str(customer[4]))
                Trec=Curry.fetchone()
                if Trec[0]==Trec[1]:
                    Curry.execute("UPDATE ROOMS SET Latest_used_no=NULL WHERE Room_ID="+str(customer[4]))
                else:
                    Curry.execute("UPDATE ROOMS SET Latest_used_no=Latest_used_no-1 WHERE Room_ID="+str(customer[4]))
                Curry.execute(f"INSERT INTO PREVCUSTOMERS VALUES {customer}")
                db.commit()

        else:
            Curry.execute("SELECT * FROM MENU")
            menu_items = cursor.fetchall()
            print("=========== MENU ===========")
            for item in menu_items:
                print(f"Item ID: {item[0]}")
                print(f"Item Name: {item[1]}")
                print(f"Category: {item[2]}")
                print(f"Price: ₹{item[3]}")
                print("----------------------------")

            num_items = int(input("How many items would you like to order? "))
            total_price = 0
            for i in range(num_items):
                while True:
                    item_id = input(f"Enter the Item_ID for item {i+1}: ")
                    cursor.execute("SELECT * FROM MENU WHERE Item_ID = %s", (item_id,))
                    item = cursor.fetchone()

                    if item:
                        print(f"Item Name: {item[1]}")
                        print(f"Price: ₹{item[3]}")
                        quantity = int(input(f"How many of {item[1]} would you like to order? "))
                        total_price += item[3] * quantity

                        Curry.execute("SELECT Order_ID FROM ORDERS")
                        OIDs=Curry.fetchall()
                        while True:
                            OID='O'+str(random.randint(10000, 99999))
                            for i in OIDs:
                                for j in i:
                                    if j==OID:
                                        break
                                else:
                                    break
                            else:
                                break
                        Curry.execute("INSERT INTO ORDERS VALUES ("+str(OID)+", "+str(CID)+", "+str(customer[6])+", "+item_id+", "+str(quantity)+", CURDATE())")
                        db.commit()
                        break
                    else:
                        print("Invalid Item ID. Please try again.")

            Curry.execute("UPDATE CUSTOMERS SET Extra_Costs="+str(total_price)+" WHERE Customer_ID="+str(CID))
            db.commit()
            print(f"\nTotal Price: ₹{total_price}")
            print("Thank you for your order!")

def AdminDashboard(AID):
    Actions={
        1:'Show Rooms',
        2:'Add Room',
        3:'Edit Room',
        4:'Delete Room',
        5:'Show Customers',
        6:'Delete Customers',
        7:'Show Previous Customers',
        8:'Show Extras',
        9:'Add Extra',
        10:'Edit Extra',
        11:'Delete Extra',
        12:'Show Menu',
        13:'Add Menu',
        14:'Edit Menu',
        15:'Delete Menu',
        16:'Show Orders',
        17:'Add Admin',
        18:'Change Password',
        19:'Custom operations',
        20:'Log-out',
        21:'Quit'
    }
    while True:
        print("Actions:")
        for act in Actions:
            print(" "*5,end='')
            print(act)
        while True:
            try:
                act=int(input("<?> Enter choice: "))
                if act in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]:
                    break
                else:
                    print("Invalid choice. Try again.")
            except:
                print("Invalid choice. Try again.")
        #All "Show" actions
        if act==1:
            show("ROOMS")
        elif act==5:
            show("CUSTOMERS")
        elif act==7:
            show("PREVCUSTOMERS")
        elif act==8:
            show("EXTRAS")
        elif act==12:
            show("MENU")
        elif act==16:
            show("ORDERS")

        #All "Delete" actions
        elif act==4:
            delete("ROOMS")
        elif act==6:
            delete("CUSTOMERS")
        elif act==11:
            delete("EXTRAS")
        elif act==15:
            delete("MENU")

        #All "Add" actions except admin
        elif act==2:
            add("ROOMS")
        elif act==9:
            add("EXTRAS")
        elif act==13:
            add("MENU")

        #All "Edit" actions
        elif act==3:
            edit("ROOMS")
        elif act==10:
            edit("EXTRAS")
        elif act==14:
            edit("MENU")

        #Everything else
        elif act==17:
            while True:
                try:
                    Curry.execute("SELECT Admin_ID FROM ADMINS")
                    Admin_IDs=Curry.fetchall()
                    while True:
                        Admin_Num=input("Enter admin number chosen: ")
                        Admin_ID='ADM'+Admin_Num
                        for i in Admin_IDs:
                            for j in i:
                                if j==Admin_ID:
                                    break
                            else:
                                break
                        else:
                            break
                    print("Your Admin_ID:",Admin_ID)
                    password=input("Enter password: ")
                    dkey=random.randint(1000,10000)
                    print("Your key, REQUIRED for LOGIN:",dkey)
                    tempfile['EncPass']=xor_encrypt(password, dkey)
                    Curry.execute(f"INSERT INTO ADMINS VALUES ({Admin_ID},{tempfile['EncPass']})")
                    db.commit()
                    break
                except:
                    print("<!> Invalid! Try again!")
        elif act==18:
            while True:
                try:
                    while True:
                       try:
                            Admin_ID=input("Enter Admin_ID: ")
                            Curry.execute("SELECT Admin_ID FROM ADMINS")
                            Admin_IDs=Curry.fetchall()
                            if f'({Admin_ID},)' not in Admin_IDs:
                                break
                       except:
                            print("<!> Something went wrong.")
                    password=input("Enter password: ")
                    dkey=random.randint(1000,10000)
                    print("Your key, REQUIRED for LOGIN:",dkey)
                    tempfile['EncPass']=xor_encrypt(password, dkey)
                    Curry.execute(f"UPDATE ADMINS SET EncPass={tempfile['EncPass']} WHERE Admin_ID={Admin_ID}")
                    db.commit()
                    break
                except:
                    print("<!> Invalid action, please retry!")
        elif act==19:
            custom=input("Enter custom prompt (put chareters under ''): ")
            try:
                Curry.execute(custom)
            except:
                print("<!> Invalid action! Learn MySQL then try again.")
        elif act==20:
            break
        elif act==21:
            exit()


'''
I. INITIALISATION of DATABASES > TABLES > INSERTION OF SAMPLE DATA
branch: Haneef, Vasu, Radhe
'''



# INITIALISATION of TABLE ROOMS, CUTOMERS, EXTRAS, PREVCUSTOMERS
Curry.execute("SHOW DATABASES")
CurrentDBS = list(Curry.fetchall())
if ('Liebeshotel',) not in CurrentDBS:
    Curry.execute("CREATE DATABASE Liebeshotel")
    Curry.execute("USE Liebeshotel")
    Curry.execute("""
        CREATE TABLE ROOMS (
            Room_ID CHAR(3) PRIMARY KEY,
            Room_Type VARCHAR(40) NOT NULL,
            Price_Per_Night INT NOT NULL,
            Max_Occupancy INT NOT NULL,
            Amenities VARCHAR(700) NOT NULL,
            Available_Rooms INT NOT NULL,
            Total_Rooms INT NOT NULL,
            Beginning_no INT NOT NULL,
            Latest_used_no INT
        )
    """)
    Curry.execute("""
        CREATE TABLE CUSTOMERS (
            Customer_ID CHAR(7) PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Contact_No CHAR(10) NOT NULL,
            Email VARCHAR(100),
            Room_ID CHAR(3) NOT NULL,
            Room_No INT NOT NULL,
            Room_Type VARCHAR(40) NOT NULL,
            Checkin_Date DATE NOT NULL,
            Checkout_Date DATE NOT NULL,
            No_of_Nights INT NOT NULL,
            Room_Bill INT NOT NULL,
            Extra_Costs INT DEFAULT 0,
            Total_Bill INT NOT NULL,
            Service_Codes VARCHAR(255)
        )
    """)
    Curry.execute("""
        CREATE TABLE PREVCUSTOMERS (
            Customer_ID CHAR(7) PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Contact_No CHAR(10) NOT NULL,
            Email VARCHAR(100),
            Room_ID CHAR(3) NOT NULL,
            Room_No INT NOT NULL,
            Room_Type VARCHAR(40) NOT NULL,
            Checkin_Date DATE NOT NULL,
            Checkout_Date DATE NOT NULL,
            No_of_Nights INT NOT NULL,
            Room_Bill INT NOT NULL,
            Extra_Costs INT DEFAULT 0,
            Total_Bill INT NOT NULL,
            Service_Codes VARCHAR(255)
        )
    """)
    Curry.execute("""
        CREATE TABLE EXTRAS (
            Service_Code CHAR(6) NOT NULL,
            Service_Name VARCHAR(50) NOT NULL,
            Cost_Per_Unit INT NOT NULL,
            Description VARCHAR(255)
        )
    """)
    Curry.execute("""
        CREATE TABLE MENU (
            Item_ID CHAR(6) PRIMARY KEY,
            Item_Name VARCHAR(50) NOT NULL,
            Category VARCHAR(30) NOT NULL,
            Price INT NOT NULL
        )
    """)
    Curry.execute("""
        CREATE TABLE ORDERS (
            Order_ID CHAR(6) PRIMARY KEY,
            Customer_ID CHAR(8),
            Room_No INT,
            Item_ID CHAR(6) NOT NULL,
            Quantity INT NOT NULL,
            Order_Date DATE NOT NULL
        )
    """)
    Curry.execute("""
        CREATE TABLE ADMINS (
            Admin_ID CHAR(6) PRIMARY KEY,
            EncPass VARCHAR(50) NOT NULL
        )
    """)
    
    # SAMPLE DATA Specifically for you~~
    Curry.execute("""
    INSERT INTO ROOMS
    VALUES
        ('101', 'Single Room', 2000, 1, 'Wi-Fi, TV, Desk, Mini-Bar', 20, 20, 1, NULL),
        ('102', 'Standard Twin Room', 3000, 2, 'Wi-Fi, TV, Desk, Wardrobe, Mini-Bar', 15, 15, 21, NULL),
        ('201', 'Deluxe Double Room', 5000, 2, 'Wi-Fi, TV, Desk, Wardrobe, Mini-Bar, Coffee Machine, Seating Area', 10, 10, 36, NULL),
        ('301', 'Junior Suite', 8000, 3, 'Wi-Fi, TV, Desk, Wardrobe, Sofa, Premium Decor, Bath and Shower, Mini-Bar', 5, 5, 46, NULL),
        ('401', 'Presidential Suite', 20000, 4, 'Wi-Fi, TV, Desk, Wardrobe, Jacuzzi, Butler Service, Smart Devices, Mini-Bar', 3, 3, 51, NULL)
    """)
    Curry.execute("""
    INSERT INTO EXTRAS
    VALUES
        ('SVC001', 'Minifridge Access', '200', 'Access to minibar items (snacks, drinks) in the room.'),
        ('SVC003', 'Playroom Card Access', '150', 'Access to the hotel playroom for recreational use.'),
        ('SVC004', 'Spa Services', '1500', 'Access to spa treatments, massages, sauna, beauty services.'),
        ('SVC005', 'Transportation', '1250', 'Airport transfers, taxi services, or guided tours.'),
        ('SVC006', 'Laundry Service', '300', 'Wash, dry, and fold services for clothes.'),
        ('SVC007', 'Parking Fees', '300', 'Access to hotel parking space.')
    """)
    Curry.execute("""
    INSERT INTO MENU
    VALUES
        ('ITM001', 'Margherita Pizza', 'Main Course', 500),
        ('ITM002', 'Caesar Salad', 'Appetizer', 250),
        ('ITM003', 'Chocolate Lava Cake', 'Dessert', 300),
        ('ITM004', 'Mango Smoothie', 'Beverage', 150),
        ('ITM005', 'Grilled Chicken', 'Main Course', 600)
    """)
    db.commit()
else:
    Curry.execute("USE Liebeshotel")

# Add an ADMIN, if NO ADMIN EXISTS
Curry.execute("SELECT * FROM ADMINS")
print(Curry.fetchall())
if len(Curry.fetchall())==0:
    dkey=4269
    password='07JAN2009@X'
    tempfile['EncPass']=xor_encrypt(password, dkey)
    print(tempfile['EncPass'])
    Curry.execute(f"INSERT INTO ADMINS VALUES ('ADM001','{tempfile['EncPass']}')")
    db.commit()



'''
II. Main interface
<comments> LOOP starts after this, this won't display again, so don't include
information that needs to be displayed again.
branch: Haneef, Vasu
'''

# Main interafce
print("\n"*30)
txt=[
    '    L         IIIIIII   EEEEEEE   BBBBBBB    EEEEEEE   SSSSSSS    H     H    OOOOO   TTTTTTT   EEEEEEE   L\n    L            I      E         B      B   E        S           H     H   O     O     T      E         L\n    L            I      EEEE      BBBBBBB    EEEE      SSSSSSS    HHHHHHH   O     O     T      EEEE      L\n    L            I      E         B      B   E                S   H     H   O     O     T      E         L\n    LLLLLLL   IIIIIII   EEEEEEE   BBBBBBB    EEEEEEE   SSSSSSS    H     H    OOOOO      T      EEEEEEE   LLLLLLL\n\n',
    '\n\n\n𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑳𝑰𝑬𝑩𝑬𝑺𝑯𝑶𝑻𝑬𝑳'+"   "*24+'Version 1.0',
    "\n\n\nLiebeshotel is a Hotel Management interface, it has an in-built resturant for it's customers. Experience luxury\nand comfort at Liebeshotel, your home away from home. Our hotel offers world-class hospitality and modern amenities\nto ensure a memorable stay for every guest. Whether you're traveling for business, leisure, or a family vacation,\nwe provide a perfect blend of elegance and convenience. It offers a range of rooms and serivces including parking\nand transport to the user, also admin has full control over the interface, regarding deletion, and other authorities,\nthe account is protected via encryption.\n\n© Liebeshotel 2024. A program developed by Haneef Rahman, Radhe Nabi, Vasu Garg.\n\n\n\n<#> Press <ENTER> to continue..."
]

for i in txt[0]:
    print(i, end='')
    time.sleep(0)
for i in txt[1]:
    print(i, end='')
    time.sleep(0)
for i in txt[2]:
    print(i, end='')
    time.sleep(0)

'''
III. The While loop
branch: Haneef, Radhe
'''

while True:
    Curry.execute("SELECT * FROM CUSTOMERS")
    allcust=Curry.fetchall()
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    for cust in allcust:
        if cust[8]==formatted_date:
            Curry.execute(f"INSERT INTO PREVCUSTOMERS VALUES {cust}")
            db.commit()
    login()
    if tempfile['accesstype']=='C':
        CustomerDashboard(tempfile['username'])
    elif tempfile['accesstype']=='A':
        AdminDashboard(tempfile['username'])
