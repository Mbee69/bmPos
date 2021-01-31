from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from collections import OrderedDict
import sqlite3

from utils.datatable import DataTable
from datetime import datetime
import hashlib

import pandas as pd
import matplotlib.pyplot as plt
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FCK

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mydb = sqlite3.connect('dbPos.db')
        self. myc = self.mydb.cursor()

        print(self.get_products())

        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        #Display products
        product_content = self.ids.scrn_product_contents
        products = self.get_products()
        producttable = DataTable(table=products)
        product_content.add_widget(producttable)

        #Admin Spinner
        spinvalues=[]
        
        for x in range(len(products['product_code'])):
            line = ' | '.join([products['product_code'][x],products['product_name'][x]])
            spinvalues.append(line)

        self.ids.target_product.values = spinvalues

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pass = TextInput(hint_text='Password')
        crud_des = Spinner(text='Operator',values=['Operator','Admin'])
        crud_submit = Button(text='Add',size_hint_x=None,width=100,on_release= lambda x: self.add_user(crud_first.text,crud_last.text,crud_user.text,crud_pass.text,crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pass)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def add_user(self, first, last, user, password, des):
        content = self.ids.scrn_contents
        content.clear_widgets()

        password = hashlib.sha256(password.encode()).hexdigest()
        sql = "INSERT INTO users(firstname,lastame,username,password,destination) values(?,?,?,?,?)"
        values = [first,last,user,password,des]

        print(sql)
        self.myc.execute(sql,values)
        self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pass = TextInput(hint_text='Password')
        crud_des = Spinner(text='Operator',values=['Operator','Admin'])
        crud_submit = Button(text='Update',size_hint_x=None,width=100,on_release= lambda x: self.update_user(crud_first.text,crud_last.text,crud_user.text,crud_pass.text,crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pass)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)


    def update_user(self, first,last,user,password,des):
        content = self.ids.scrn_contents
        content.clear_widgets()

        password = hashlib.sha256(password.encode()).hexdigest()
        sql = 'UPDATE users SET firstname=?,lastame=?,username=?,password=?,destination=? WHERE username=?'
        values = [first,last,user,password,des,user]
        print(sql)
        self.myc.execute(sql,values)
        self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='User Name')
        crud_submit = Button(text='Remove',size_hint_x=None,width=100,on_release= lambda x: self.remove_user(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_user(self, user):
        content = self.ids.scrn_contents
        content.clear_widgets()

        sql = 'DELETE FROM users WHERE username=?'
        values = [user]
        print(sql)
        self.myc.execute(sql,values)
        self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)
        #self.ids.ops_fields.clear_widgets()

    def add_product_fields(self):
        print('Add P')
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_weight = TextInput(hint_text='Product Weight')
        crud_in_stock = TextInput(hint_text='Product In Stock')
        crud_sold = TextInput(hint_text='Product Sold')
        crud_order = TextInput(hint_text='Product Order')
        crud_purchase = TextInput(hint_text='Product Last Purchase')
        crud_submit = Button(text='Add',size_hint_x=None,width=100,on_release= lambda x: self.add_product(crud_code.text,crud_name.text,crud_weight.text,crud_in_stock.text,crud_sold.text,crud_order.text,crud_purchase.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_in_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)

    def add_product(self, code, name,weight,stock,sold,sorder,purchase):
        product_content = self.ids.scrn_product_contents
        product_content.clear_widgets()

        sql = "INSERT INTO stocks(product_code,product_name,product_weight,in_stock,sold,product_order,last_purchase) values(?,?,?,?,?,?,?)"
        values = [code, name,weight,stock,sold,sorder,purchase]

        print(sql)
        self.myc.execute(sql,values)
        self.mydb.commit()

        products = self.get_products()
        producttable = DataTable(table=products)
        product_content.add_widget(producttable)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_weight = TextInput(hint_text='Product Weight')
        crud_in_stock = TextInput(hint_text='Product In Stock')
        crud_sold = TextInput(hint_text='Product Sold')
        crud_order = TextInput(hint_text='Product Order')
        crud_purchase = TextInput(hint_text='Product Last Purchase')
        crud_submit = Button(text='Update',size_hint_x=None,width=100,on_release= lambda x: self.update_product(crud_code.text,crud_name.text,crud_weight.text,crud_in_stock.text,crud_sold.text,crud_order.text,crud_purchase.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_in_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)

    def update_product(self, code, name,weight,stock,sold,sorder,purchase):
        product_content = self.ids.scrn_product_contents
        product_content.clear_widgets()

        sql = "UPDATE stocks SET product_code=?,product_name=?,product_weight=?,in_stock=?,sold=?,product_order=?,last_purchase=? WHERE product_code=?"
        values = [code, name,weight,stock,sold,sorder,purchase,code]

        print(sql)
        self.myc.execute(sql,values)
        self.mydb.commit()

        products = self.get_products()
        producttable = DataTable(table=products)
        product_content.add_widget(producttable)
    
    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_submit = Button(text='Remove',size_hint_x=None,width=100,on_release= lambda x: self.remove_product(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_product(self, code):
        product_content = self.ids.scrn_product_contents
        product_content.clear_widgets()

        sql = "DELETE FROM stocks WHERE product_code=?"
        values = [code]

        print(sql)
        self.myc.execute(sql,values)
        self.mydb.commit()

        products = self.get_products()
        producttable = DataTable(table=products)
        product_content.add_widget(producttable)

    def get_users(self):
        conn = sqlite3.connect('dbPos.db')
        c = conn.cursor()

        # c.execute('CREATE TABLE IF NOT EXISTS users (firstname text, lastname text, username text, password text, designations text)')
        # conn.commit()

        # c.close()
        # conn.close()
        c.execute('SELECT * FROM users')
        data = c.fetchall()
        print(data)
        _users=OrderedDict()
        _users['first_names'] = {}
        _users['last_names']={}
        _users['user_names']={}
        _users['passwords']={}
        _users['designations']={}

        first_names=[]
        last_names=[]
        user_names=[]
        passwords=[]
        designations=[]
        
        for row in data:
            first_names.append(row[1])
            last_names.append(row[2])
            user_names.append(row[3])
            pwd = row[4]
            if len(pwd)>10:
                pwd=pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(row[5])

        users_lengt = len(first_names)
        idx = 0
        while idx < users_lengt:
            _users['first_names'][idx]= first_names[idx]
            _users['last_names'][idx]= last_names[idx]
            _users['user_names'][idx]= user_names[idx]
            _users['passwords'][idx]= passwords[idx]
            _users['designations'][idx]= designations[idx]

            idx += 1

        return _users

    def get_products(self):
        conn = sqlite3.connect('dbPos.db')
        c = conn.cursor()

        c.execute('SELECT * FROM stocks')
        data = c.fetchall()
        print(data)
        _stocks=OrderedDict()

        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight']={}
        _stocks['in_stock']={}
        _stocks['sold']={}
        _stocks['order']={}
        _stocks['last_purchase'] = {}

        product_code=[]
        product_name=[]
        product_weight=[]
        in_stock=[]
        sold=[]
        order=[]
        last_purchase=[]
        
        for row in data:
            product_code.append(row[0])
            product_name.append(row[1])
            product_weight.append(row[2])
            in_stock.append(row[3])
            try:
                sold.append(row[4])
            except KeyError:
                sold.append('')
            try:
                order.append(row[5])
            except KeyError:
                order.append('')
            try:
                last_purchase.append(row[6])
            except KeyError:
                last_purchase.append('')
            

        stocks_lengt = len(product_code)
        idx = 0
        while idx < stocks_lengt:
            _stocks['product_code'][idx]= product_code[idx]
            _stocks['product_name'][idx]= product_name[idx]
            _stocks['product_weight'][idx]= product_weight[idx]
            _stocks['in_stock'][idx]= in_stock[idx]
            _stocks['sold'][idx]= sold[idx]
            _stocks['order'][idx]= order[idx]
            _stocks['last_purchase'][idx]= last_purchase[idx]

            idx += 1

        return _stocks
    def view_stats(self):
        target_product = self.ids.target_product.text
        target = target_product[:target_product.find(' | ')]
        name = target_product[target_product.find(' | '):]
    def change_screen(self,instance):
        if instance.text == "Manage Users":
            self.ids.screen_manager.current = 'scrn_content'
        elif instance.text == "Manage Products":
            self.ids.screen_manager.current = 'scrn_product_content'
        elif instance.text == "Manage Analysis":
            self.ids.screen_manager.current = 'scrn_analysis_content'


class AdminApp(App):
    def build(self):
        return AdminWindow()

if __name__=="__main__":
    AdminApp().run()