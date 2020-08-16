import pymysql

class db:
    def __init__(self):
        self.conn = pymysql.connect(host='sql7.freesqldatabase.com',user='sql7360528',passwd='BgFrnfH2NA',db='')
    def readitems(self):
        cursor = self.conn.cursor()
        cursor.execute('select product_code from items')  # .execute runs codes in sqlmanagmentstudio
        return [product_code[0] for product_code in cursor]

    def readcateg(self):
        cursor = self.conn.cursor()
        cursor.execute('select name from category')
        return [name[0] for name in cursor]

    def getid(self):
        cursor = self.conn.cursor()
        cursor.execute(' select contact_number from costumer')
        return [contact_number[0] for contact_number in cursor]

    def checkid(self,getid, z):  # z is the user contact number which is also the primary key
	cursor=self.conn.cursor()
        found = [i for i in getid if z in i]
        if found == empty :
		return NONE
	else :
		return found

    def adduserid(self, z):
        cursor = self.conn.cursor()
        cursor.execute('insert into costumer(contact_number,costumer_name) values(?,?)', (z, "user"))

    def addusername(self, n, z):  # n is the username
        cursor = self.conn.cursor()
        cursor.execute("update costumer set costumer_name= ? where contact_number =? ", (n, z))

    def getusername(self, z):
        cursor = self.conn.cursor()
        cursor.execute("select costumer_name from costumer where contact_number =? ", z)
        return [costumer_name[0] for costumer_name in cursor]

    def getallitemsincat(self, c):  # c is the category name ps.use drinks for testing
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT items.product_name from items WHERE items.product_code in (select contain.product_code from contain where contain.category_id in(select category.category_id from category where category.name=?))",
            (c))
        return ([product_name[0] for product_name in cursor])

    def addtolist(self, p):  # adds items into collects
        cursor = self.conn.cursor()
        cursor.execute("insert into collects (order_id,product_name) values ('1',?) ", (p))

    def removefromlist(self, p):  # remove items from collects
        cursor = self.conn.cursor()
        cursor.execute('delete from collects  where collects.product_name = ?', (p))
    def getremainingitems(conn,i):
	cursor=conn.cursor()
	cursor.execute('select quantity from items where product_name = ? ',(i))
	return [quantity[0] for quantity in cursor]
    def addaddress(conn,a,i):
	cursor=conn.cursor()
	cursor.execute('update customer set address=? where contact_number =? ',(a,i))
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
    
    def getcouriernumber(self,n):
	cursor=self.conn.cursor()
	cursor.execute('select phone_number from delivery_phone_number where delivery_id = (select delivery_id from delivery where delivery.first_name= ?)',(n))
    def getremainingitems(self,i):
	cursor=self.conn.cursor()
	cursor.execute('select quantity from items where product_name = ? ',(i))
	return [quantity[0] for quantity in cursor]
    
    def addaddress(self,a,i):
	cursor=self.conn.cursor()
	cursor.execute('update customer set address=? where contact_number =? ',(a,i))
        
    def getquantity(self,x):
	cursor=self.conn.cursor()
	cursor.execute('select quantity from items where product_name= ?',(x))
	return [quantity [0] for quantity in cursor]
        
    def getcourier(self):
        cursor = self.conn.cursor()
        cursor.execute('select top (1) delivery.first_name from delivery order by busy_state asc')
