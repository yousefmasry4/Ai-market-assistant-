import pymysql


class db:
    def __init__(self):
        self.conn = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7360528', passwd='BgFrnfH2NA',
                                    db='sql7360528')

    def readitems(self):  # y
        cursor = self.conn.cursor()
        cursor.execute('select product_name from items')  # .execute runs codes in sqlmanagmentstudio
        return [str(product_name[0]).replace(" ", "") for product_name in cursor]

    def readcateg(self):  # y
        cursor = self.conn.cursor()
        cursor.execute('select name from category')
        return [name[0] for name in cursor]

    def getid(self):  # y
        cursor = self.conn.cursor()
        cursor.execute(' select customer_id from customer')
        return [contact_number[0] for contact_number in cursor]

    def checkid(self, getid, z):  # y  # z is the user contact number which is also the primary key
        if z in getid:
            self.conn.cursor().execute('''
                DELETE From collects
                where order_id = %s
            ''' % z)
            return self.getusername(z)[0]
        else:
            return None

    def adduserid(self, z):  # y
        cursor = self.conn.cursor()
        f = cursor.execute(
            'insert into customer(customer_id,customer_name,password) values(%s,' % z + "'user'" + ',123)')
        self.conn.commit()
        print(f.__str__())

    def addusername(self, n, z):  # Y  # n is the username
        cursor = self.conn.cursor()
        cursor.execute("update customer set customer_name= '%s' where customer_id =%s " % (n, z))
        self.conn.commit()

    def getusername(self, z):  # y
        cursor = self.conn.cursor()
        cursor.execute("select customer_name from customer where customer_id = %s " % z)
        return [customer_name[0] for customer_name in cursor]

    def getallitemsincat(self, cc):  # y  # c is the category name ps.use drinks for testing
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT items.product_name from items
             WHERE items.type =
             (
                SELECT category_id  FROM category 
                WHERE name ='%s'
             )
              '''%str(cc).upper())
        return [str(product_name[0]).replace(" ", "") for product_name in cursor]

    def addtolist(self, my_id, p):  # y  # adds items into collects
        cursor = self.conn.cursor()
        cursor.execute("insert into collects (order_id,product_name) values (%s,'%s') " % (my_id, str(p).upper()))
        self.conn.commit()

    def removefromlist(self, my_id, p):  # Y  # remove items from collects
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE  from collects  where collects.product_name = '%s' and order_id = %s ORDER BY order_id DESC LIMIT 1; " % (
            str(p).upper(), my_id))
        self.conn.commit()

    def getremainingitems(self, i):  # y
        cursor = self.conn.cursor()
        cursor.execute("select quantity from items where product_name = '%s' " % str(i).upper())
        return int([quantity[0] for quantity in cursor][0])

    def addaddress(self, a, i):  # y
        cursor = self.conn.cursor()
        cursor.execute("update customer set address='%s' where customer_id =%s " % (a, i))
        self.conn.commit()

    def getprice(self, p):  # y
        cursor = self.conn.cursor()
        cursor.execute("select price from items where product_name ='%s' " % (p))
        return int([price[0] for price in cursor][0])

    def getlistid(self, id):
        cursor = self.conn.cursor()
        cursor.execute("select product_name from collects  WHERE  order_id='%s'" % id)
        return [product_name[0] for product_name in cursor]

    def getcategoryofitem(self, p):  # y
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT category.name from category ,items
            where category.category_id =items.type
            and items.product_name='%s'
            '''
            % (p))
        return [category_name[0] for category_name in cursor][0]

    def getlocationofitem(self, p):  # y
        cursor = self.conn.cursor()
        cursor.execute("select section_location from items where product_name= '%s'" % p)
        return [category_name[0] for category_name in cursor][0]

    def getcouriernumber(self, n):  # y
        cursor = self.conn.cursor()
        cursor.execute(
            'select phone_number from delivery_phone_number'
            ' where delivery_id = '
            "(select delivery_id from delivery where delivery.first_name= '%s')"
            % n)
        return [i[0] for i in cursor][0]

    def getcourier(self):  # y
        cursor = self.conn.cursor()
        cursor.execute('select delivery.first_name from delivery order by busy_state  ')
        return [i[0] for i in cursor][0]


