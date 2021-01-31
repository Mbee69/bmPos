from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

import sqlite3
from collections import OrderedDict


Builder.load_string('''
<DataTable>:
    id: main_win
    RecycleView:
        viewclass: "CustLabel"
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')

class DataTable(BoxLayout):
    def __init__(self,table='',**kwargs):
        super().__init__(**kwargs)

        #products = self.get_products()
        products = table

        col_titles = [k for k in products.keys()]
        rows_len = len(products[col_titles[0]])
        self.columns = len(col_titles)
        print(rows_len)
        
        table_data = []
        for t in col_titles:
            table_data.append({'text':str(t),'size_hint_y': None,'height':50,'bcolor':(.06,.45,.45,1)})

        for r in range(rows_len):
            for t in col_titles:
                table_data.append({"text":str(products[t][r]),'size_hint_y': None,'height':30,'bcolor':(.06,.25,.25,1)})
        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data


#     def get_products(self):
#         conn = sqlite3.connect('dbPos.db')
#         c = conn.cursor()

#         c.execute('SELECT * FROM stocks')
#         data = c.fetchall()
#         #print(data)
#         _stocks=OrderedDict(
#             product_code = {},
#             product_name = {},
#             product_weight={},
#             in_stock={},
#             sold={},
#             order={},
#             last_purchase = {}
#         )
#         product_code=[]
#         product_name=[]
#         product_weight=[]
#         in_stock=[]
#         sold=[]
#         order=[]
#         last_purchase=[]
        
#         for row in data:
#             product_code.append(row[0])
#             product_name.append(row[1])
#             product_weight.append(row[2])
#             in_stock.append(row[3])
#             sold.append(row[4])
#             order.append(row[5])
#             last_purchase.append(row[6])
            

#         stocks_lengt = len(product_code)
#         idx = 0
#         while idx < stocks_lengt:
#             _stocks['product_code'][idx]= product_code[idx]
#             _stocks['product_name'][idx]= product_name[idx]
#             _stocks['product_weight'][idx]= product_weight[idx]
#             _stocks['in_stock'][idx]= in_stock[idx]
#             _stocks['sold'][idx]= sold[idx]
#             _stocks['order'][idx]= order[idx]
#             _stocks['last_purchase'][idx]= last_purchase[idx]

#             idx += 1

#         return _stocks

# class DataTableApp(App):
#     def build(self):
#         return DataTable()


# if __name__=="__main__":
#     DataTableApp().run()