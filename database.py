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
file_order = 'file/orderandcakedata.csv'
file_order_copy = 'file/orderandcakedata_copy.csv'
file_dis = 'file/dispatchers.csv'
file_dis_copy = 'file/dispatchers_copy.csv'

file_log = 'file/log.txt'

file_size = 'file/cake_size.csv'
file_type = 'file/cake_type.csv'
logo = 'file/1.jpg'
title_size = 20
cake_attr_num = 4
# hint for option menu
hint1= ">      Choose a dispatcher or not   "
# index for order
index_no = 0
index_address = 1
index_pos =2
index_name = 2
index_phone = 3
index_cakes = 4
index_state = 5
index_psinfo = 6
index_dis = 7
index_mode = 8
index_date = 9
index_time = 10
# index for cake
index_cake_size = 0
index_cake_type =1
index_cake_quan = 2
index_cake_ps = 3
# index for dispatcher
index_dis_name = 0
index_dis_home = 1
index_dis_phone = 2
#index_dis_orders = 3
index_dis_ps = 3
# index for postcode
index_city = 0
index_other = 1

dis = 'dispatch'
pickup = 'pick up'
processing = 'Processing'
waiting = 'Waiting'
arrived = 'Arrived'
making = 'Making'
start_location = ''
warning_message1 = ' fields with (*) cant be empty'
warning_message2 = ' need at least one address to dispatch'
warning_message3 = ' no generated route yet'
warning_message4 = ' Error: check address! strictly in the form of \n(street address,postcode)'
warning_message5 = ' choose at least one dispatcher please'
warning_message5 = ' service not available right now, please try agin later or \nmanually assign orders to dispatchers'
warning_message7 = ' no orders in '


# option menu items
size  = ['small','medium','big']
size2  = [['small'],['medium'],['big']]
cake_types = ['CakeType1','CakeType2','CakeType3','CakeType4']
states = ['Making','Waiting','Processing','Arrived']
quantities = ['1','2','3','4','5','other(indicate \nin the ps block)']
modes = [dis,pickup]

# header for listboxes
header_full = ['No', 'Address','Name','Phone','Cakes','State']
header_today = ['No', 'Address','Name','Mode','Cakes','State']
header_proc = ['No', 'Address','Name','Phone','Dispatcher','State']
header_small = ['No', 'Address']
header_cake = ['Size','CakeType','Quan','Ps']
header_dispatcher = ['Name','Home Address']
header_dispatcher_full = ['Name','Home Adderss','Phone','Ps']

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
    dispatchers = []
    cake_size = []
    cake_types = []
    def __init__(self,fp = file_name):
        tmp = []
        postcodee = []
        dispatcherss = []
        f = open(fp,'rb')
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            order = Order(line[index_no],line[index_address],\
                          line[index_name],line[index_phone],\
                          convert_data_to_list(line[index_cakes]),\
                          line[index_state])
            add_info_2order(order,line)
            
            tmp.append(order)
        f.close()

        f = open(file_postcode, "rb")
        reader = csv.reader(f,delimiter=',')
        for i in reader:
            postcodee.append(i)
        f.close

        f = open(file_dis,'rb')
        reader = csv.reader(f, delimiter=',')
        for dis in reader:
            print dis
            self.dispatchers.append(dis)
        f.close()

        f = open(file_type,'rb')
        reader = csv.reader(f,delimiter = ',')
        for row in reader:
            print row
            self.cake_types = row
            break
        f.close()

        f = open(file_size,'rb')
        reader = csv.reader(f,delimiter = ',')
        for row in reader:
            self.cake_size = row
            break
        f.close()

        self.postcode = postcodee
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
                if item.state== making:
                    item.set_dispatcher(None)
                    self.orders_today.append(item)
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
    dispatcher = None
    mode = dis
    pickup_date = None
    pickup_time = None
    location_id = None
    def __init__(self, order_number=None, \
                     address=None, \
                     name =None, \
                     phone = None, \
                     cake_type = None, \
                     state = None, \
                     ps_info = 'Empty',
                     ):
        self.order_number = order_number
        self.address = address
        self.name = name
        self.phone = phone
        self.cake_type = cake_type
        self.state = state
        self.ps_info = ps_info

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


""" This is a class for cake with basic functions including
    print its info and comparison"""
class Cake(object):
    """__init__() functions as the class constructor"""
    def __init__(self,
                order_number = None,
                size = None,
                caketype = None,
                quan = None,
                ps_info = 'Empty'):
        self.order_number = order_number
        self.size = size
        self.type = caketype
        self.quan = quan
        self.ps_info = ps_info

    def __str__(self):
            return str(self.__dict__)

    def __eq__(self, other):
            return self.__dict__ == other.__dict__

# convert a cake class to a list containing nessary info
def cake_to_list(cake):
    list = [cake.size,cake.type,cake.quan,cake.ps_info]
    return list

# convert a list containing nessary info to  a cake class
def list_to_cake(list_cake):
    try:
        newcake = Cake(list_cake[index_cake_size],list_cake[index_cake_type],\
        list_cake[index_cake_quan],list_cake[index_cake_ps])
    except IndexError:
        newcake = Cake(list_cake[index_cake_size],list_cake[index_cake_type],\
        list_cake[index_cake_quan],'empty')

# convert list of cake objects to a list cake lists
def cakes_to_lists(cakes):
    return_list = []
    for cake in cakes:
        return_list.append(cake_to_list(cake))
    return return_list

# convert a list of lists to a list of order classes
def list_to_class(list_lists):
    new_list = []
    for item in list_lists:
        try:
            new_order_item = Order(item[index_no],item[index_address],\
                             item[index_name],item[index_phone],\
                             item[index_cakes],item[index_state],item[index_psinfo])
        except IndexError:
            new_order_item = Order(item[index_no],item[index_address],\
                             item[index_name],item[index_phone],\
                             item[index_cakes],item[index_state],"EMPTY")
        new_list.append(new_order_item)

    return new_list

# convert a class to a list of str
def class_to_order(item):
    new_list_item = [item.order_number,item.address,\
                     item.name,item.phone,item.cake_type,\
                     item.state,item.ps_info,item.dispatcher,item.mode,\
                     item.pickup_date,item.pickup_time]

    return new_list_item

# order to list with mode
def o2list_mode(item):
    new_list_item = [item.order_number,item.address,\
                     item.name,item.mode,show_cake(item.cake_type),\
                     item.state]
    return new_list_item

# convert a list of lists to a list of order classes with mode
def o2lists_mode(items):
    new_list = []
    for item in items:
        new_list.append(o2list_mode(item))
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
        new_list_item = [item.order_number,item.address,\
                         item.name,item.phone,show_cake(item.cake_type),\
                         item.state]
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

# add info to order
def add_info_2order(order,line):
    print line
    if line[index_psinfo]:
        order.ps_info = line[index_psinfo]
    if line[index_dis]:
        order.dispatcher = line[index_dis]
    if line[index_mode]:
        order.mode = line[index_mode]
    try:
        order.date = line[index_date]
    except IndexError:
        order.date = ""
    try:
        order.time = line[index_time]
    except IndexError:
        order.time = ""
        
# write error message to log file
def write_2_log(message):
    now = datetime.now()
    f = open(file_log,'a+')
    f.write("Error({}): {}".format(now,message))
    f.close()

# check ps info doesnt contain special characters other than comma
def isvalid(stringg):
    for i in stringg:
        if not (i.isdigit() or i.isalpha() or (i == ',') or (i == ' ')):
            return False
    return True
    
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





