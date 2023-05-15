import sqlite3
import atexit
from itertools import product

from dbtools import Dao
 
# Data Transfer Objects:
class Employee(object):
    #TODO: implement
    
    def __init__(self, id, name, salary, branch):
        
        self.id = id
        self.name = name
        self.salary = salary
        self.branch = branch
        
 
class Supplier(object):
    #TODO: implement
    
    def __init__(self, id, name, contact_information):
        
        self.id = id
        self.name = name
        self.contact_information = contact_information
    

class Product(object):
    #TODO: implement
    
    def __init__(self, id, description, price, quantity):
        
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

class Branche(object):
    #TODO: implement

    def __init__(self, id, location, number_of_employees):
        
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

class Activitie(object):
    #TODO: implement
    
    def __init__(self, product_id, quantity, activator_id, date):
        
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


class Employees_report(object):
    def __init__(self, name, salary, working_location, total_sales_income):
        self.name = name
        self.salary = salary
        self.working_location = working_location
        self.total_sales_income = total_sales_income


class Activities_report(object):
    def __init__(self, activity_date , item_description, quantity, seller_name, supplier_name):
        self.activity_date = activity_date
        self.item_description = item_description
        self.quantity = quantity
        self.seller_name = seller_name
        self.supplier_name = supplier_name


# Data Access Objects:
class employees(object):
    #TODO: implement
    
    def __init__(self, connection):
        
        self.con = connection
        
    def insert(self, Employee):
        
        self.con.execute("""INSERT INTO employees (id, name, salary, branche) VALUES (?,?,?,?) """ 
                        , [Employee.id, Employee.name, Employee.salary, Employee.branch])
    
    def find(self,employee_id):

        c = self.con.cursor()
        c.execute("""SELECT * FROM employees WHERE id = ?"""
                ,[employee_id])

        return Employee(*c.fetchone())

    def find_all(self):
        c = self.con.cursor()
        return c.execute("SELECT * FROM employees").fetchall()

 
class suppliers(object):
    #TODO: implement
    
    def __init__(self, connection):
        
        self.con = connection
        
    def insert(self, Supplier):
        
        self.con.execute("""INSERT INTO suppliers (id, name, contact_information) VALUES (?,?,?) """ 
                        , [Supplier.id, Supplier.name, Supplier.contact_information])
    
    def find(self, supplier_id):

        c = self.con.cursor()
        c.execute("""SELECT * FROM suppliers WHERE id = ?"""
                ,[supplier_id])

        return supplier(*c.fetchone())

    def find_all(self):
        c = self.con.cursor()
        return c.execute("SELECT * FROM suppliers").fetchall()


class products(object):
    #TODO: implement
    
    def __init__(self, connection):
        
        self.con = connection
        
    def insert(self, Product):
        
        self.con.execute("""INSERT INTO products (id, description, price, quantity) VALUES (?,?,?,?) """ 
                        , [Product.id, Product.description, Product.price, Product.quantity])
    
    def find(self, product_id):

        c = self.con.cursor()
        c.execute("""SELECT * FROM products WHERE id = ?"""
                ,[product_id])

        return Product(*c.fetchone())


    def updateQuantity(self, product_id , new_quantity): 

        self.con.execute("""UPDATE products SET quantity = (?) WHERE id = (?)"""
                ,[new_quantity, product_id])

    def find_all(self):
        c = self.con.cursor()
        return c.execute("SELECT * FROM products").fetchall()



class branches(object):
    #TODO: implement
    
    def __init__(self, connection):
        
        self.con = connection
        
    def insert(self, Branche):
        
        self.con.execute("""INSERT INTO branches (id, location, number_of_employees) VALUES (?,?,?) """ 
                        , [Branche.id, Branche.location, Branche.number_of_employees])
    
    def find(self,branche_id):

        c = self.con.cursor()
        c.execute("""SELECT * FROM branches WHERE id = ?"""
                ,[branche_id])
        
        return Branch(*c.fetchone())


    def find_all(self):
        c = self.con.cursor()
        return c.execute("SELECT * FROM branches").fetchall()



class activities(object):
    #TODO: implement
    
    def __init__(self, connection):
        
        self.con = connection
        
    def insert(self, Activitie):
        
        self.con.execute("""INSERT INTO activities (product_id, quantity, activator_id, date) VALUES (?,?,?,?) """ 
                        , [Activitie.product_id , Activitie.quantity , Activitie.activator_id , Activitie.date])
    
    def find(self, activitie_product_id):

        c = self.con.cursor()
        c.execute("""SELECT * FROM activities WHERE id = ?"""
                ,[activitie_product_id])

        return activitie(*c.fetchone())


    def find_all(self):
        c = self.con.cursor()
        return c.execute("SELECT * FROM activities ORDER BY activities.date ASC" ).fetchall()




  

#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        #self._conn.text_factory = bytes
        

        #TODO: complete
        
        self.activities = activities(self._conn)
        self.branches = branches(self._conn)
        self.employees = employees(self._conn)
        self.products = products(self._conn)
        self.suppliers = suppliers(self._conn)
        
        
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()


    def get_employees_report(self):
        all = self._conn.cursor().execute(""" SELECT employees.name, employees.salary, branches.location, IFNULL(SUM(-1 * products.price * activities.quantity ), 0)
                                        FROM (employees INNER JOIN branches ON employees.branche = branches.id
                                         LEFT OUTER JOIN activities ON employees.id = activities.activator_id
                                         LEFT OUTER JOIN products ON activities.product_id = products.id)
                                        GROUP BY employees.id
                                        ORDER BY employees.name ASC""").fetchall()
        return[Employees_report(*row) for row in all]


    def get_activities_report(self):
        return self._conn.cursor().execute(""" SELECT activities.date, products.description, activities.quantity, employees.name, suppliers.name
                                        FROM (activities INNER JOIN products ON activities.product_id = products.id
                                        LEFT OUTER JOIN employees ON activities.activator_id = employees.id
                                        LEFT OUTER JOIN suppliers ON activities.activator_id = suppliers.id)
                                        ORDER BY activities.date ASC""").fetchall()



# singleton
repo = Repository()
atexit.register(repo._close)