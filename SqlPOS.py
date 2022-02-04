import datetime
import psycopg2 as pg2
con = pg2.connect(database='POS', user='postgres', password='password')
cur = con.cursor()


option = input("Where do you Want to go? I for inventory, C for customers and O for orders ")

if option == "I" or option == "i":
    Table = "Inventory"
    Inv2ndOption = input("Type S to search or A to add: ")
elif option == "C" or option == "c":
    Table = "Customers"
elif option == "O" or option == "o":
    Table = "Orders"
else: Table = "Inventory"

if Table == "Inventory":
    if Inv2ndOption == "A" or Inv2ndOption == "a":
        Sku = input("Enter Sku: ")
        Title = input("Enter Title: ")
        Price = input("Enter Price: ")
        Quantity = input("Enter Quantity: ")
        Location = input("Enter Location: ")
        cur.execute("INSERT INTO Inventory VALUES ('{}', '{}', {}, {}, '{}')".format(Sku, Title, float(Price), int(Quantity), Location))
        con.commit()
        con.close()
    elif Inv2ndOption == "S" or Inv2ndOption == "s":
        allorsku = input("Type E to search everything or Enter SKU to search ")
        if allorsku == "E" or allorsku == "e":
            cur.execute("SELECT * FROM inventory;")
            for row in cur.fetchall():
                print(row)
                con.commit()
        elif allorsku != "E" or allorsku != "e":
            cur.execute("SELECT * FROM inventory WHERE sku ='{}'".format(allorsku))
            print(cur.fetchall())
            con.commit()
            con.close()
    con.close()

if Table == "Customers":
    custallorphone = input("Type Customer's Phone Number or E to search all Customers ")
    if custallorphone == "E" or custallorphone == "e":
        cur.execute("SELECT * FROM Customers;")
        for row in cur.fetchall():
            print(row)
            con.commit()
    elif custallorphone != "E" or custallorphone != "e":
        cur.execute("SELECT * FROM Customers WHERE PhoneNum ='{}'".format(custallorphone))
        print(cur.fetchall())
        con.commit()
        con.close()

if Table == "Orders" :
    Order2ndOption = input ("Type C to create new order or type order number to search order or Customer's Phone number so search by Customer ")
    if len(Order2ndOption) == 10:
        cur.execute("SELECT * FROM totbyphone Where customer_id ='{}'".format(Order2ndOption))
        for row in cur.fetchall():
            print(row)
            con.commit()

    if Order2ndOption != "C" and Order2ndOption != "c" and len(Order2ndOption)< 10:
        cur.execute("SELECT * FROM orders WHERE order_id =" + Order2ndOption)
        for row in cur.fetchall():
            print(row)
            con.commit()

    if Order2ndOption == "C" or Order2ndOption == "c":
        Skuz = []
        Skueach = ""
        while Skueach != "D" or Skueach != "d":
            Skueach = input("Enter skus for order then D when done ")
            Skuz.append(Skueach)
            cur.execute(" SELECT sku FROM inventory WHERE sku = '{}'".format(Skueach))
            checker = cur.fetchone()
            if checker == None and Skueach != 'd' and Skueach != 'D':
                print("Sku does not exist, Let's create it ")
                title = input("Enter Title ")
                price = input("Enter Price ")
                quantity = input("Enter Quantity ")
                location = input("Enter Location ")

                cur.execute(
                    "INSERT INTO inventory (sku, title, price, quantity, location) VALUES ('{}','{}',{},{},'{}')".format(Skueach, title, float(price), int(quantity), location))
            elif Skueach == "D" or Skueach == "d":
                currentdate = datetime.date.today()
                cur.execute("SELECT max(Order_id) FROM Orders;")
                maxorder = cur.fetchone()[0] + 1
                Customnum = input("Enter Customer Phone Number ")
                cur.execute("SELECT PhoneNum FROM Customers WHERE PhoneNum = '{}'".format(Customnum) + ";")
                try:
                    checkit = int(cur.fetchone()[0])
                except:
                    print("No Customer exists that is linked to that phone number. Let's create one ")
                    FirstName = input("Enter First Name ")
                    LastName = input("Enter Last Name ")
                    Street = input("Enter Street Address ")
                    City = input("Enter City ")
                    State = input("Enter State ")
                    ZipCode = input("Enter Zip Code ")
                    cur.execute("INSERT INTO Customers (phonenum, firstname, lastname, street, city, state, zipcode, order_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(Customnum, FirstName, LastName, Street, City, State, ZipCode, int(maxorder)))

                break
            #Skuz.append(Skueach)

try:

        for item in Skuz:
            cur.execute("SELECT Price FROM Inventory WHERE Sku ='{}'".format(item) + ";")
            cur.execute("INSERT INTO Orders (order_id, sku, price, customer_id, date) VALUES ({},'{}', {}, {}, '{}')".format(int(maxorder), item, float(cur.fetchone()[0]), Customnum, currentdate))
            cur.execute("SELECT * FROM order_total WHERE order_id = {}".format(int(maxorder)))
            print("Total = '{}'".format(cur.fetchone()[1]))
            con.commit()

except:
             print("")

