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
        CREATE TABLE MENU (
            Item_ID CHAR(6) PRIMARY KEY,
            Item_Name VARCHAR(50) NOT NULL,
            Category VARCHAR(30) NOT NULL,
            Price INT NOT NULL,
        );

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


# SAMPLE DATA Specifically for you~~
Curry.execute("""
INSERT INTO ROOMS
VALUES
    ('101', 'Single Room', 2000, 1, 'Wi-Fi, TV, Desk, Mini-Bar', 20, 1, NULL),
    ('102', 'Standard Twin Room', 3000, 2, 'Wi-Fi, TV, Desk, Wardrobe, Mini-Bar', 15, 21, NULL),
    ('201', 'Deluxe Double Room', 5000, 2, 'Wi-Fi, TV, Desk, Wardrobe, Mini-Bar, Coffee Machine, Seating Area', 10, 36, NULL),
    ('301', 'Junior Suite', 8000, 3, 'Wi-Fi, TV, Desk, Wardrobe, Sofa, Premium Decor, Bath and Shower, Mini-Bar', 5, 46, NULL),
    ('401', 'Presidential Suite', 20000, 4, 'Wi-Fi, TV, Desk, Wardrobe, Jacuzzi, Butler Service, Smart Devices, Mini-Bar', 3, 51, NULL)
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

"""
Curry.execute("SHOW TABLES")
print(Curry.fetchall())
"""