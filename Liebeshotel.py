import pymysql
import requests
import datetime
import time

# INITIALISATION of database network, cursor, tempfile
db=pymysql.connect(host='localhost',user='root',password='12APRIL2002')
Curry=db.cursor()
tempfile={
    'accesstype':None
}

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
            Beginnt INT NOT NULL,
            Neueste INT
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
            Cost_Per_Unit VARCHAR(20) NOT NULL,
            Description VARCHAR(255)
        )
    """)
    
    Curry.execute("""
        CREATE TABLE ORDERS (
            Order_ID CHAR(6) PRIMARY KEY,
            Customer_ID CHAR(8),
            Room_No INT,
            Item_ID CHAR(6) NOT NULL,
            Quantity INT NOT NULL,
            Order_Date DATE NOT NULL,
        );
    """)





"""
Curry.execute("SHOW TABLES")
print(Curry.fetchall())
"""