import pymysql


class db:
    def __init__(self):
        self.conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7360528', passwd='BgFrnfH2NA', db='sql7360528')
    def readitems(self):#y
        cursor = self.conn.cursor()
        cursor.execute('select product_name from items')  # .execute runs codes in sqlmanagmentstudio
        return [str(product_name[0]).replace(" ","") for product_name in cursor]
    def readcateg(self):#y
        cursor = self.conn.cursor()
        cursor.execute('select name from category')
        return [name[0] for name in cursor]
    def getid(self):#y
        cursor = self.conn.cursor()
        cursor.execute(' select customer_id from customer')
        return [contact_number[0] for contact_number in cursor]
    def checkid(self, getid, z):#y  # z is the user contact number which is also the primary key
        if z in getid:
            self.conn.cursor().execute('''
                DELETE From collects
                where order_id = %s
            '''%z)
            return self.getusername(z)[0]
        else:
            return  None
    def adduserid(self, z):#y
        cursor = self.conn.cursor()
        f=cursor.execute('insert into customer(customer_id,customer_name,password) values(%s,'%z+"'user'"+',123)')
        self.conn.commit()
        print(f.__str__())
    def addusername(self, n, z):#Y  # n is the username
        cursor = self.conn.cursor()
        cursor.execute("update customer set customer_name= '%s' where customer_id =%s "%(n,z))
        self.conn.commit()
    def getusername(self, z):#y
        cursor = self.conn.cursor()
        cursor.execute("select customer_name from customer where customer_id = %s "%z)
        return [customer_name[0] for customer_name in cursor]
    def getallitemsincat(self, c):#y  # c is the category name ps.use drinks for testing
        c=str(c).upper()
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT items.product_name from items
             WHERE items.type =
             (
                SELECT category_id  FROM category 
                WHERE name ='%s'
             )
              '''
            %c)
        return [str(product_name[0]).replace(" ", "") for product_name in cursor]
    def addtolist(self,my_id, p):#y  # adds items into collects
        cursor = self.conn.cursor()
        cursor.execute("insert into collects (order_id,product_name) values (%s,'%s') "%(my_id,str(p).upper()))
        self.conn.commit()
    def removefromlist(self,my_id, p):#Y  # remove items from collects
        cursor = self.conn.cursor()
        cursor.execute("DELETE  from collects  where collects.product_name = '%s' and order_id = %s ORDER BY order_id DESC LIMIT 1; "%(str(p).upper(),my_id))
        self.conn.commit()

    def getremainingitems(self, i):
        cursor = self.conn.cursor()
        cursor.execute("select quantity from items where product_name = '%s' "%str(i).upper())
        return [quantity[0] for quantity in cursor]

    def addaddress(conn, a, i):
        cursor = conn.cursor()
        cursor.execute('update customer set address=? where contact_number =? ', (a, i))

    def getprice(self, p):
        cursor = self.conn.cursor()
        cursor.execute("select price from items where product_name =? ", (p))
        return [price[0] for price in cursor]

    def getlistid(self):
        cursor = self.conn.cursor()
        cursor.execute("select product_name,order_id from collects ")
        return [product_name[0] for product_name in cursor], [order_id[0] for order_id in cursor]

    def getcategoryofitem(self, p):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT category.name from category where category.category_id in (select contain.category_id from contain where contain.product_code in (select items.product_code from items where items.product_name=?))',
            (p))
        return [category_name[0] for category_name in cursor]

    def getlocationofitem(self, p):
        cursor = self.conn.cursor()
        cursor.execute('select location from items where product_name= ?', p)
        return [category_name[0] for category_name in cursor]

    def getcouriernumber(self, n):
        cursor = self.conn.cursor()
        cursor.execute(
            'select phone_number from delivery_phone_number where delivery_id = (select delivery_id from delivery where delivery.first_name= ?)',
            (n))

    def getremainingitems(self, i):
        cursor = self.conn.cursor()
        cursor.execute('select quantity from items where product_name = ? ', (i))
        return [quantity[0] for quantity in cursor]

    def addaddress(self, a, i):
        cursor = self.conn.cursor()
        cursor.execute('update customer set address=? where contact_number =? ', (a, i))

    def getquantity(self, x):
        cursor = self.conn.cursor()
        cursor.execute('select quantity from items where product_name= ?', (x))
        return [quantity[0] for quantity in cursor]

    def getcourier(self):
        cursor = self.conn.cursor()
        cursor.execute('select top (1) delivery.first_name from delivery order by busy_state asc')
db=db()