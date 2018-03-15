# -*- coding: UTF-8 -*-  
import sys     
reload(sys)
sys.setdefaultencoding('utf-8')
""" This is a file for the database of orders
    created by Rondo 26/01/2018"""

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import random
from shutil import copyfile
import xlrd
# try:
#     from openpyxl import Workbook
# except ImportError:
#     print "Need to install openpyxl see https://openpyxl.readthedocs.io/en/stable/"
from datetime import datetime
import csv
import ast

background = "#f2f2f2"
textColor = "WHITE"
file_name = 'file/ordersdata.csv'
file_name2 = 'file/routedata.csv'
file_postcode = 'file/postcode.csv'
file_postcode_full = 'file/postcode_full.csv'
file_order = 'file/orderandcakedata.csv'
file_order_copy = 'file/orderandcakedata_copy.csv'
file_dis = 'file/dispatchers.csv'
file_dis_copy = 'file/dispatchers_copy.csv'
file_log = 'file/log.txt'
file_size = 'file/cake_size.csv'
file_type = 'file/cake_type.csv'
file_inner = 'file/cake_inner.csv'
file_shapes = 'file/cake_shapes.csv'
logo = 'file/1.jpg'
title_size = 20
cake_attr_num = 4
# hint for option menu
hint1= ">              请选择一个派送员              "
# index for order
index_no = 0
index_agent = 1
index_address = 2
index_name = 3
index_phone = 4
index_candle = 5
index_tableware = 6
index_writing = 7
index_price = 8
index_state = 9
index_mode = 10
index_date = 11
index_time = 12
index_psinfo = 13
index_cakes = 14
index_dis = 15
index_upfront = 16
# index for cake
index_cake_no = 0
index_cake_size = 1
index_cake_shape =2
index_cake_inner = 3
index_cake_type =4
index_cake_ps = 5
# index for dispatcher
index_dis_name = 0
index_dis_home = 1
index_dis_phone = 2
#index_dis_orders = 3
index_dis_ps = 3
# index for postcode
index_city = 0
index_other = 1

dis = '派送'
pickup = '自取'
processing = '正在派送'
waiting = '等待被派送'
arrived = '订单已签收'
start_location = ''
warning_message1 = '      (*)栏不得为空     '
warning_message2 = ' 至少需要一个订单来进行派送'
warning_message5 = ' 请至少选择一个派送员'
warning_message5 = ' service not available right now, please try agin later or \nmanually assign orders to dispatchers'
warning_message7 = '  地区没有订单      '
warning_message8 = ' 输入地址的区号有错误，或无法在数据库查找到'
warning_message9 = ' 输入地址的格式有误，应是（street,postcode）'

# sizes of column witdth
col_size1 = 48
col_size2 = 110
col_size3 = 80

# option menu items
size  = ['small','medium','big']
size2  = [['small'],['medium'],['big']]
cake_types = ['CakeType1','CakeType2','CakeType3','CakeType4']
states = [waiting,processing,arrived]
quantities = ['1','2','3','4','5','other(indicate \nin the ps block)']
modes = [dis,pickup]

# header for listboxes
header_new = ['订单号','蛋糕No','客服号','尺寸','形状','内芯','款式','价格','定金','写字','蜡烛','餐具','电话','地址','备注','状态']
header_full = ['订单号','客服号','价格','定金','写字','蜡烛','餐具','电话','地址','备注']
header_today = ['订单号', 'Address','Name','Mode','Cakes','State']
header_proc = ['No', 'Address','Name','Phone','Dispatcher','State']
header_small = ['No', 'Address']
header_cake = ['No','尺寸','形状','内芯','款式','备注']
header_dispatcher = ['Name','Home Address']
header_dispatcher_full = ['姓名','家庭住址','电话','备注']

# end locations options
end_location = ['8 Whiteman St, Southbank VIC 3006']
dispatch_options = ['','']

#######################################################################################
sample_data = [['22','800 swanston street,3053','Rondo','0401082050','CakeType1','Making'],
               ['24312','500 swanston street,3053','Michael','0405078123','CakeType2','Arrived'],
               ['5586','melbourne central,3000','Yibo','041230123','Type3','Waiting'],
               ['12314','442 Elizabeth street,3000','Jeffery','645231321','Type4','Waiting'],
               ['54645','200 collins street,3000','David','45234123','Type0','Waiting']]

sample_data2 = [['22','800 swanston street,3053','Rondo','0401082050',[['big', 'CakeType3', 2, 'empty']],'Making','empty','empty',dis,'empty','empty'],
               ['24312','500 swanston street,3053','Michael','0405078123',[['small', 'CakeType4', 2, 'empty']],'Arrived','empty','empty',dis,'empty','empty'],
               ['5586','melbourne central,3000','Yibo','041230123',[['medium', 'CakeType3', 2, 'empty'], ['small', 'CakeType4', 0, 'empty'], ['big', 'CakeType1', 1, 'empty']],'Waiting','empty','empty',dis,'empty','empty'],
               ['12314','442 Elizabeth street,3000','Jeffery','645231321',[['small', 'CakeType1', 0, 'empty'], ['medium', 'CakeType3', 0, 'empty']],'Waiting','empty','empty',dis,'empty','empty'],
               ['54645','200 collins street,3000','David','45234123',[['big', 'CakeType3', 2, 'empty'], ['big', 'CakeType3', 1, 'empty'], ['small', 'CakeType3', 0, 'empty']],'Waiting','empty','empty',dis,'empty','empty']]

sample_dispatchers = [['Jason','800 swanston street,3000','1',''],
                    ['John','442 Elizabeth street,3000','2',''],
                    ['Andy','3-13 Harrow St,3128','3','']]

cakes = []
i = 0
while i < 10:
    order_number = random.randint(0, 4)
    size_index = random.randint(0, 2)
    type_index = random.randint(0, 3)
    quantity = random.randint(0, 2)
    cakes.append([size[size_index],cake_types[type_index],quantity,'empty'])
    i+=1

# cake1 = cake_generator()
# cake2 = cake_generator()
# cake3 = cake_generator()
# cake4 = cake_generator()
# cake5 = cake_generator()
# cake_lists = [[cake1],[cake2],[cake3],[cake4],[cake5]]
cake_lists = [[],[],[],[],[]]
i = 0
while i < 10:
    number = random.randint(0, 4)
    cake_lists[number].append(cakes[i])
    i +=1

def cake_generator():
    #order_number = random.randint(0, 4)
    size_index = random.randint(0, 2)
    type_index = random.randint(0, 3)
    quantity = random.randint(0, 2)
    cake = [size[size_index],cake_types[type_index],quantity]
    return cake

"""database of orders for its management including
   adding new order, deleting order and updating"""
class Orders_database(object):
    """__init__() functions as the class constructor"""
    orders_today = []
    orders_proc = []
    orders_history = []
    orders_leftbox = []
    orders_rightbox = []
    orders_pickup = []
    postcode = []
    postcode_full = []
    dispatchers = []
    def __init__(self,fp = file_name):
        tmp = []
        postcodee = []
        postcodee_full = []
        dispatcherss = []
        f = open(fp,'rb')
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            print "#line:{}".format(line)
            print "#cakes:{}".format(line[index_cakes])
            order = Order(line[index_no],line[index_agent],line[index_address],\
                          line[index_name],str(line[index_phone]),line[index_candle],\
                          line[index_tableware],line[index_writing],line[index_price],\
                          line[index_state],line[index_mode],line[index_date],line[index_time],\
                          line[index_psinfo],convert_data_to_list(line[index_cakes]),\
                          line[index_dis],line[index_upfront])       
            tmp.append(order)
        f.close()

        f = open(file_postcode, "rb")
        reader = csv.reader(f,delimiter=',')
        for i in reader:
            postcodee.append(i)
        f.close
        
        f = open(file_postcode_full, "rb")
        reader = csv.reader(f,delimiter=',')
        for i in reader:
            postcodee_full.append(i)
        f.close

        f = open(file_dis,'rb')
        reader = csv.reader(f, delimiter=',')
        for dis in reader:
            print dis
            self.dispatchers.append(dis)
        f.close()


        self.postcode = postcodee
        self.postcode_full = postcodee_full
        self.orders_all = tmp
        self.update()

    def add(self,item):
        for item1 in self.orders_all:
            if item1 == item:
                print "Error(add): item already exsits in the database!"

        self.orders_all.append(item)
        self.update()

    def delete(self,item):
        found2 = False
        for item1 in self.orders_all:
            if item1 == item:
                self.orders_all.remove(item1)
                found2 = True

        if not found2:
            print "Error(delete): item not in the database!"
        else:
            self.update()

    def add_cake_to_order(self,cake,order_number):
        for item in self.orders_all:
            if item.order_number == order_number:
                item.cake_type.append(cake)
                return item.cake_type

    def get_cakes(self,order_number):
        for item in self.orders_all:
            if item.order_number == order_number:
                return item.cake_type

    def update_dispatchers(self):
        f = open(file_dis,'wb')
        f.truncate()
        writer = csv.writer(f, delimiter=',')
        for dis in self.dispatchers:
            writer.writerow(dis)
        f.close()


    def update(self):
        # to prevent the case of losing data
        copyfile(file_order, file_order_copy)
        self.orders_today[:] = []
        self.orders_proc[:] = []
        self.orders_history[:] = []
        self.orders_leftbox[:] = []
        self.orders_rightbox[:] = []
        f = open(file_order, "wb")
        f.truncate()
        writer = csv.writer(f,delimiter=',')
        for item in self.orders_all:
            print "item.cake_type"
            print item.cake_type
            writer.writerow(class_to_order(item))
            if item.mode != dis:
                self.orders_pickup.append(item)
                if item.state == arrived:
                    self.orders_history.append(item)
                else:
                    self.orders_today.append(item)
            else:
                if item.state == processing:
                    self.orders_proc.append(item)
                    self.orders_today.append(item)
                if item.state== waiting:
                    item.set_dispatcher(None)
                    self.orders_leftbox.append(item)
                    self.orders_today.append(item)
                if item.state == arrived:
                    self.orders_history.append(item)
        f.close()

    def print_details(self):
        print "orders today:"
        for item in self.orders_today:
            item.print_order()
        print "\norders processing:"
        for item in self.orders_proc:
            item.print_order()
        print "\norders history:"
        for item in self.orders_history:
            item.print_order()
        print "\norders leftbox:"
        for item in self.orders_leftbox:
            item.print_order()
        print "\norders rightbox:"
        for item in self.orders_rightbox:
            item.print_order()

    def not_in(self,list,item):
        not_found = True
        for item1 in list:
            if item1 == item :
                not_found = False
                break
        return not_found

""" This is a class for order with basic functions including
    print its info and comparison"""
class Order(object):
    """__init__() functions as the class constructor"""

    def __init__(self, order_number=None, 
                     agent = None,
                     address=None, 
                     name =None, 
                     phone = None, 
                     candle = None,
                     tableware = None,
                     writing = None,
                     price = None,
                     state = None, 
                     mode = dis,
                     pickup_date = None,
                     pickup_time = None,
                     ps_info = None,
                     cake_type = None, 
                     dispatcher = None,
                     upfront = None
                     ):
        self.order_number = int(order_number)
        self.agent = str(agent)
        self.address = str(address)
        self.name = str(name)
        self.phone = phone
        self.candle = str(candle)
        self.tableware = str(tableware)
        self.writing = str(writing)
        self.price = str(price)
        self.state = str(state)
        self.mode = str(mode)
        self.pickup_date = str(pickup_date)
        self.pickup_time = str(pickup_time)
        self.cake_type = cake_type
        self.ps_info = str(ps_info)
        self.dispatcher = str(dispatcher)
        self.upfront = str(upfront)

    def __str__(self):
            return str(self.__dict__)

    def __eq__(self, other):
            return self.__dict__ == other.__dict__

    def print_order(self):
        print ("%s,(%s),%s,%s,%s,%s,%s" % (self.order_number,self.address,\
              self.name,self.phone,self.cake_type,self.state,\
              self.ps_info))

    def set_dispatcher(self,dispatcher):
        self.dispatcher = dispatcher

# convert a class to a list of str
def class_to_order(item):
    new_list_item = [item.order_number,item.agent,item.address,\
                     item.name,str(item.phone),item.candle,item.tableware,\
                     item.writing,item.price,item.state,item.mode,\
                     item.pickup_date,item.pickup_time,item.ps_info,\
                     item.cake_type,item.dispatcher,item.upfront]

    return new_list_item

# order to list with mode
def order2list(item,cake):
    print item.phone
    print str(item.phone)
    new_list_item = [item.order_number,cake[index_cake_no],item.agent,cake[index_cake_size],cake[index_cake_shape],\
                     cake[index_cake_inner],cake[index_cake_type],item.price,item.upfront,\
                     item.writing,item.candle,item.tableware,strip(item.phone),item.address,\
                     item.ps_info,item.state]
    return new_list_item

# convert a list of lists to a list of order classes with mode
def order2lists(items):
    new_list = []
    for item in items:
        print item.phone
        print str(item.phone)
        for cake in item.cake_type:
            new_list.append(order2list(item,cake))
    return new_list

# show list of cakes nicely
def show_cake(cakes):
    print "cakes"
    print cakes
    new = []
    for cake in cakes:
        try:
            new.append(cake[index_cake_type])
        except IndexError:
            write_2_log("cake[index_cake_type] IndexEror,database.py/show_cake")
    return new

# list to a string
def trim2(list1):
    new = []
    for i in list1:
        if i:
            tmp = " ".join(i)
            new.append(tmp)
    return new

# show order numebrs in dispatcher listbox nicely
def show_dis(dispatchers):
    # new = []
 #    for dis in dispatchers:
 #        tmp = dis[index_dis_orders]
 #        tmp = convert_data_to_list(tmp)
 #        dis[index_dis_orders] = tmp

    print dispatchers
    return dispatchers


# convert a list of order classes to a list of lists used
# to create listbox
def class_to_list_without_info(list_class):
    new_list = []
    for item in list_class:
        new_list_item = [item.order_number,item.agent,item.price,item.upfront,\
                         item.writing,item.candle,item.tableware,item.phone,\
                         item.address,item.ps_info]
        new_list.append(new_list_item)
    return new_list

# convert a list of order classes to a list of lists used
# to create listbox
def class_to_list_without_info2(list_class):
    new_list = []
    for item in list_class:
        new_list_item = [item.order_number,item.address,\
                         item.name,item.phone,item.dispatcher,\
                         item.state]
        new_list.append(new_list_item)

    return new_list


# convert a list of order classes to a list of lists used
# to create listbox
def class_to_list(list_class):
    new_list = []
    for item in list_class:
        new_list_item = class_to_order(item)
        new_list.append(new_list_item)

    return new_list

# convert a list of order classes to a list of lists used
# to create listbox
def ctl_num_address(list_class):
    new_list = []
    for item in list_class:
        new_list_item = [item.order_number,item.address]
        new_list.append(new_list_item)

    return new_list

# clean unnecessary characters while reading from database
def clear_char(stringg):
    new_string = []
    count = 0
    for i in stringg:
        print "clear_char"
        print i
        if count == 0 and i == 'u':
            continue
        elif i.isdigit() or i.isalpha():
            new_string.append(i)
        else:
            continue
        count += 1
    return ''.join(new_string)

# convert string form of list to original list form
def convert_data_to_list(stringg):    
    x = ast.literal_eval(stringg)
    #print x
    new_list = [n for n in x]
    #print new_list
    return new_list


# get rid of empty list
def trim_list(list):
    new_list = []
    for i in list:
        if not(i == ''):
            new_list.append(int(i))
    return new_list

# get rid of empty list
def trim_list2(list):
    new_list = []
    for i in list:
        if not(i == ''):
            new_list.append(i)
    return new_list


# change a list of string to a list of lists of string inorder to
# be displayed in listbox
def to_listbox(list1):
    new_list = []
    for string in list1:
        tmp = [string]
        new_list.append(tmp)
    return new_list

# read cake shapes from file
def read_cake_shapes():
    cake_shapes = []
    f = open(file_shapes,'rb')
    reader = csv.reader(f,delimiter = ',')
    for row in reader:
        cake_shapes = row
        break
    f.close()
    return cake_shapes
        
# read cake inner from file
def read_cake_inner():
    cake_inner = []
    f = open(file_inner,'rb')
    reader = csv.reader(f,delimiter = ',')
    for row in reader:
        cake_inner = row
        break
    f.close()
    return cake_inner
    
# read cake size from file
def read_cake_size():
    cake_size = []
    f = open(file_size,'rb')
    reader = csv.reader(f,delimiter = ',')
    for row in reader:
        cake_size = row
        break
    f.close()
    return cake_size

# read cake types from file
def read_cake_types():
    cake_types = []
    f = open(file_type,'rb')
    reader = csv.reader(f,delimiter = ',')
    for row in reader:
        print row
        cake_types = row
        break
    f.close()
    return cake_types
        
# write error message to log file
def write_2_log(message):
    now = datetime.now()
    f = open(file_log,'a+')
    f.write("Log({}): {}\n".format(now,message))
    f.close()

# check ps info doesnt contain special characters other than comma
def isvalid(stringg):
    for i in stringg:
        if not (i.isdigit() or i.isalpha() or (i == ',') or (i == ' ') or (i == '，') ):
            return False
    return True

# get rid of number
def rip_num(str):
    new_str = []
    for i in str:
        if  not i.isdigit():
            new_str.append(i)
    return_str = []
    for i in "".join(new_str).split(' '):
        if i.lower() != 'vic':
            return_str.append(i)
            
    return "".join(return_str)
    
# get rid of unnessary info
def rip_num_full(str):
    new_str = rip_num(str)
    return new_str.split(',')[0]

# justify the order of listbo
def justify_order(listbox,tmp):
    last = len(listbox.table_data)-1
    listbox.insert_row(tmp)
    if last >= 0:
        listbox.delete_row(last)

def justify_order2(listbox):
    last = len(listbox.table_data)-1
    if last >= 0:
        tmp =  listbox.table_data[last]
        listbox.delete_row(last)
        listbox.insert_row(tmp)
    
# update listbox
def update_listbox(lists,listbox):
    listbox.update(lists)
    last = len(listbox.table_data)-1
    if last > 0:
        print listbox.table_data[last]
        listbox.delete_row(last)
        listbox.insert_row(lists[0],0)
    # listbox.clear()
 #    for i in lists:
 #        listbox.insert_row(i)
 #        listbox.insert_row(i)
 #        last = len(listbox.table_data)-1
 #        listbox.delete_row(last)
 #    last = len(listbox.table_data)-1
 #    if last > 0:
 #        print listbox.table_data[last]
 #        listbox.delete_row(last)

# check wheter all integet or not
def isvalid_id(idd):
    print "idd"
    print idd
    for i in idd:
        if not i.isdigit():
            return True
    return False
# get rid of char which is not number
def strip(strr):
    new = []
    for i in strr:
        if i.isdigit():
            new.append(i)
    return "".join(new)
# center a window
# @sources: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
    
if __name__ == "__main__":
    # for item in c_orders:
#         print item.print_order()
#  #    c_lists = class_to_list(c_orders)
#  #    for item in c_lists:
#  #        print item[index_name]
#
#     print "#########"
#

   f = open(file_size,'wb')
   writer = csv.writer(f,delimiter = ',')
   writer.writerow(size)
   f.close()

   f = open(file_type,'wb')
   writer = csv.writer(f,delimiter = ',')
   writer.writerow(cake_types)
   f.close()

   f = open(file_dis,'wb')
   writer = csv.writer(f,delimiter = ',')
   for i in sample_dispatchers:
       writer.writerow(i)
   f.close()

   f = open(file_order,'wb')
   writer = csv.writer(f,delimiter = ',')
   for i in sample_data2:
       writer.writerow(i)
   f.close()

   db = Orders_database(file_order)
   print db.cake_size
   #
   # for item in sample_data2:
#        print '\n'
#        for i in item[index_cakes]:
#            print i

    # f = open(file_postcode, "wb")
#     writer = csv.writer(f,delimiter=',')
#
#     workbook = xlrd.open_workbook("Delivery.xlsx","rb")
#     sheets = workbook.sheet_names()
#     required_data = []
#     for sheet_name in sheets:
#         sh = workbook.sheet_by_name(sheet_name)
#         #print sh.col_values(0)
#         writer.writerow(trim_list(sh.col_values(0)))
#         #print sh.col_values(1)
#         writer.writerow(trim_list(sh.col_values(1)))
#
#     f.close()
#
#     f = open(file_postcode, "rb")
#     reader = csv.reader(f,delimiter=',')
#     for i in reader:
#         print i
#     f.close()





