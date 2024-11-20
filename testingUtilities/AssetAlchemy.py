import pymysql
import requests
import datetime
import time

# INITIALISATION of database network, tempfile, login
db=pymysql.connect(host='localhost',user='root',password='12APRIL2002')
Curry=db.cursor()
tempfile={
    'accesstype':None
}

# (1) NO1, INITIALISATION, NODE1, Haneef
print("\n"*30)
txt=[
    '    A        L        CCCCC     H   H    EEEEE     M   M    Y   Y\n   A A       L       C          H   H    E         MM MM     Y Y \n  A   A      L      C           HHHHH    EEEE      M M M      Y   \n AAAAAAA     L       C          H   H    E         M   M      Y   \nA       A    LLLLL    CCCCC     H   H    EEEEE     M   M      Y   \n',
    '  OOO     FFFFF             A       SSSSS   SSSSS   EEEEE   TTTTT   SSSSS\n O   O    F                A A     S       S        E         T    S    \nO     O   FFFF            A   A     SSSSS   SSSSS   EEEE      T     SSSSS \n O   O    F              AAAAAAA         S       S  E         T          S\n  OOO     F             A       A   SSSSS   SSSSS   EEEEE     T     SSSSS'
    '\n\n\n𝘼𝙇𝘾𝙃𝙀𝙈𝙔 𝙊𝙁 𝘼𝙎𝙎𝙀𝙏𝙎'+"   "*24+'Version 1.0',
    "\n\n\nAsset Alchemy is an Investment Company Management system, it is a platform for users to deposit money\n, invest in verious markets and grow their money via smart investment methods. Top gainers are\nrefreshed and displayed for free users, but they are limited to just one market to invest in, and it\nmust be from the Top gainers. The premium users can invest in upto 5 markets at a time, they are\noffered a variety of options and advanced analytics. Admin options are confidential.\n\n© Alchemy of Assets 2024. A program developed by Haneef Rahman, Radhe Nabi, Vasu Garg.\n\n\n\n<#> Press <ENTER> to continue..."
]
print(txt[0])
for i in txt[1]:
    print(i,end='')
    time.sleep(0)
for i in txt[2]:
    print(i,end='')
    time.sleep(0)
input()

Curry.execute("SHOW DATABASES")
print(Curry.fetchall())

