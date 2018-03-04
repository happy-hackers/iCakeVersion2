try:
    from tkinter import *
except ImportError:
    import Tkinter
import webbrowser

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
import ttk
from multicolumnlistboxLib import *
from database import *
#from ttkcalendar import *

from shutil import copyfile

from datetime import datetime
import googlemaps
#from kmeans import *
from PIL import Image, ImageTk


#gmaps = googlemaps.Client(key="AIzaSyBykVZQJbt518Jh58CDo6vb3TH4pM0j21Q")
# gmaps = googlemaps.Client(key="AIzaSyB3Ao6QZnqxngkZPB4d5yQaboPp-mSjf4s")
# gmaps = googlemaps.Client(key="AIzaSyD44UyOsGzuyngSnb2WPLPuFGzhIG1OL1s")
gmaps = googlemaps.Client(key="AIzaSyCWzV0pbt_84I2DraGqg1OaC5kil5pZESY")


prefix = "https://www.google.com/maps/dir/?api=1"
origin = "&origin="
destination = "&destination="
viaDriving = "&travelmode=driving"
waypoints = "&waypoints="

window_open = False                  # to ensure only one add/edit order window
                                     # can be opened at one time
cake_window_open = False             # same functionality as window_open
popup_cake = None                    # right click menu for cakes windows

# calculate distance between two points using google map
def cal_dis(orders,end_loc):
    if orders:
        try:
                    locations = to_loc(orders)
                    print "proc_start_loc.get()"
                    print proc_start_loc.get()
                    new_location = gmaps.places_autocomplete(input_text = proc_start_loc.get(), \
                                                             location = proc_start_loc.get())[0]['description']
                    start_locationId = gmaps.geocode(new_location)[0]['place_id']
                    locations.insert(0,proc_start_loc.get())

                    # if there is specified end location append it to the end of locations
                    print "end location:"
                    print end_loc
                    print ','.join(get_address(end_loc))
                    if end_loc != hint1 and ','.join(get_address(end_loc)):
                       print "$"
                       locations.append(','.join(get_address(end_loc)))

                    print "locations"
                    print locations
                    directions_result = gmaps.directions(locations[0],
                                                         locations[-1],
                                                         waypoints=locations[1:-1],
                                                         mode="driving", avoid="tolls",
                                                         departure_time=datetime.now(),
                                                         optimize_waypoints = True)

                    totalDistance = 0
                    totalDuration = 0
                    newLocationIds = [start_locationId]
                    print "directions_result!!"
                    print directions_result
                    if not directions_result:
                        warning_window(master,"Some addresses can not be found!")
                        return
            
                    lists = directions_result[0]['legs']
            # Not loop to the last one
                    for index in range(len(lists)):
                        try:
                            #get rid off unit so use -3 to kms, -4 to mins
                            print lists[index]['distance']['text'][:-3]
                            print lists[index]['duration']['text'][:-4]
                            if lists[index]['distance']['text'][:-3]:
                                totalDistance += float(lists[index]['distance']['text'][:-3])
                            if lists[index]['duration']['text'][:-4]:
                                totalDuration += float(lists[index]['duration']['text'][:-4])

                            locationId = gmaps.geocode(gmaps.places_autocomplete(input_text = lists[index]['end_address'], \
                                    location = lists[index]['end_address'])[0]['description'])[0]['place_id']
                            print "cal_dis:"
                            print locationId
                            print lists[index]['end_address']
                            newLocationIds.append(locationId)
                        except IndexError:
                            warning_window(master,"Index Error in cal_dis(line 95)")
                            return
                        

            # add last location manunally
                    # if end_loc != hint1 and ','.join(get_address(end_loc)):
#                         print "end location!!!!!!!!!!!!"
#                         print locations[-1]
#
#                         locationId = gmaps.geocode(gmaps.places_autocomplete(input_text = locations[-1], \
#                                 location = locations[-1])[0]['description'])[0]['place_id']
#                         print locationId
#                         newLocationIds.append(locationId)

                    print "new locations!!!"
                    print newLocationIds
                    print gmaps.reverse_geocode(newLocationIds[-1])[0]['formatted_address']

                    finalLocations = outputFile(newLocationIds, totalDistance, \
                                             totalDuration, (len(locations)-1), orders,end_loc)
                    openWebsite(finalLocations)
        except:
            warning_window(master,"Server not available right now or one dispatcher can not have more than 21 orders, try again later") 
    else:
        return
        
# find order by id helper
def find_order_by_id2(orders,id):
    for order in orders:
        if order.order_number == id:
            return order

# setup doc
def setup_doc(document,order,order_num):  
    document.add_heading("{} : {}\n".format(order_num,order.address, level = 1))
    document.add_paragraph("Order number : {}".format(order.order_number))
    document.add_paragraph("Client Name : {}".format(order.name))
    document.add_paragraph("Phone : {}".format(order.phone))
    document.add_paragraph("Order Ps : {}".format(order.ps_info))
    document.add_paragraph("Cake info : ")
    setup_table(document,order)
    
    
    
# setup doc table
def setup_table(document,order):
    cake_num = 1
    row_num = 0
    table = document.add_table(rows = (len(order.cake_type)+1), cols = 5)
    table.style = 'Table Grid'

    # setup header for the table
    row = table.rows[row_num]
    row.cells[0].text = "Cake No"
    row.cells[1].text = "Cake Type"
    row.cells[2].text = "Cake Size"
    row.cells[3].text = "Cake Quantity"
    row.cells[4].text = "Ps Info"

    row_num += 1
    for cake in order.cake_type:
        row = table.rows[row_num]
        row.cells[0].text = str(cake_num)

        # bold cell
        cell_type = row.cells[1]
        cell_type.text = cake[index_cake_type]
        run = cell_type.paragraphs[0].runs[0]
        run.font.bold = True
        # bold cell
        cell_size = row.cells[2]
        cell_size.text = cake[index_cake_size]
        run = cell_size.paragraphs[0].runs[0]
        run.font.bold = True

        row.cells[3].text = cake[index_cake_quan]
        row.cells[4].text = cake[index_cake_ps]
        
        row_num += 1
        cake_num += 1
               
###############################################################################
def outputFile(finalLocationIds, totalDistance, totalDuration, totalOrder, \
        orders,end_loc):
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import RGBColor
    import pandas as pd
    import easygui
    import os

    document = Document()

    heading = document.add_heading('iCake Delivery', 0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    order_num = 0

    dic_id = {}
    # input order info
    if end_loc != hint1:
        if ','.join(get_address(end_loc)):
            print "#####"
            print "end_loc is"
            print end_loc
            end_loc_without_name = (','.join(get_address(end_loc)))
            print end_loc_without_name
            document.add_heading("Dispatcher:{}".format(end_loc,font=("Calibri",title_size)))
            end_loc_id = gmaps.geocode(gmaps.places_autocomplete(\
                    input_text = end_loc_without_name, \
                        location = end_loc_without_name)[0]['description'])[0]['place_id']

            dic_id[end_loc_id] = "end location"
        else:
            document.add_heading("Dispatcher:{}".format(end_loc.split(',')[0],font=("Calibri",title_size)))
            
        
    else:
        document.add_heading("Driver Not Determined".format(font=("Calibri",title_size)))

    finalLocations = []

    dic_id[finalLocationIds[0]] = "start location"
    for order in orders:
        id = gmaps.geocode(order.address)[0]['place_id']
        dic_id[id] = order.order_number
        print "id is :"
        print id
        print order.address

    print dic_id


    print "ouput:"
    print finalLocationIds
    for item in finalLocationIds:
        fomattedAddress = gmaps.reverse_geocode(item)[0]['formatted_address']
        finalLocations.append(fomattedAddress)
        print item
        try:
            order_numberr = dic_id[item]
            order = find_order_by_id2(orders,order_numberr)
            print order
            print order_numberr
            if order:
                order_num += 1
                setup_doc(document,order,order_num)
        except KeyError:
            warning_window(master,"{}\nError with this address.".format(fomattedAddress))
        
       
            
    #document.add_paragraph("\nTotal distance is %.1f kms." % totalDistance)
    #document.add_paragraph("Total duration is %.1f mins." % totalDuration)
    document.add_paragraph("Total number of orders are %d.\n" % order_num)

    now = datetime.now()

    path = easygui.diropenbox()

    if end_loc != hint1:
        filename = now.strftime("%Y-%m-%d %H.%M ")+"for {}".format(end_loc.split(',')[0])+".docx"
    else:
        filename = now.strftime("%Y-%m-%d %H.%M ")+"for {}".format("Driver")+".docx"

    filepath = os.path.join(path, filename)
    document.save(filepath)

    return finalLocations

###############################################################################
def openWebsite(finalLocations):
    i = 0
    print "#####################"
    print finalLocations
    addPage = False
    while i < len(finalLocations):
        if (i % 10 == 0):
            if i != 0:
                webbrowser.open(prefix+origin+ start_point +destination+ end_point +\
                        viaDriving + waypoints + quote(points[:-1]) )
            points = ""
            start_point = quote(finalLocations[i])

        # if i is every 9th index item or the last one for all locations
        elif ((i + 1) % 10 == 0 or i == len(finalLocations)-1):
            end_point = quote(finalLocations[i])
            if (i == len(finalLocations)-1):
                webbrowser.open(prefix+origin+ start_point +destination+ end_point +\
                        viaDriving + waypoints + quote(points[:-1]) )

        else:
            #There will be one more | at the end
            points += finalLocations[i]+"|"

        i += 1

###############################################################################
def find_order_by_id(id,orders):
    for order in orders:
        if int(id) == int(order.order_number):
            return order
    print "Error(find_order_by_id()): no order found"
    return None

def to_loc(orders):
    locs = []
    for i in orders:
        locs.append(i.address)
    return locs

def to_order(orders):
    order_numbers = []
    for i in orders:
        order_numbers.append(i.order_number)
    return order_numbers

def to_order2(orders):
    order_numbers = []
    for i in orders:
        order_numbers.append([i.order_number])
    return order_numbers


def get_item_by_num(num,orders):
    for i in orders:
        new = []
        for n in  num.split(',')[0]:
            if n.isdigit() or n.isalpha():
                new.append(n)
        strr = ''.join(new)
        print strr
        print i.order_number
        if str(i.order_number) == str(strr):
            return i

def get_item_by_num2(num,orders):
    print "get_item_by_num2"
    if not orders:
        print "orders is null"
    for i in orders:
        print i
        print "i.order_number = {}".format(i.order_number)
        print "num[0] = {}".format(num)
        if int(i.order_number) == int(num):
            return i
###############################################################################
# sperate orders to orders in city and orders in other areas
def in_city(orders,postcode_city,postcode_full_city):
    return_list = [[],[]]
    if orders:
        print "in_city"

    for order in orders:
        print "#############"
        print order.address
        #print get_pos2(order.address)
        postcode = order.address.split(',')[-1]
        if postcode:
            if in_pos(postcode,postcode_city,postcode_full_city):
                print "city:"
                print order
                return_list[index_city].append(order)
            else:
                print "other:"
                print order
                return_list[index_other].append(order)
        else:
            warning_window(master,"{} raises time out".format(order.address))
            return
       

    return return_list

# check postcode of various forms in list or not    
def in_pos(postcode,list1,list_full):
    num_form = []
    for i in postcode:
        if i.isdigit():
            num_form.append(i)
    pos_num = "".join(num_form)
    print "num_form:"
    print num_form
    
    # user enter number of postcode
    if num_form:
        if "".join(num_form) in list1:
            return True
        else:
            return False
    else:
        new_pos = rip_num(postcode)
        for pos_full in list_full:
            new_pos_full = rip_num_full(pos_full)
            print "new_pos_full:"
            print new_pos_full.lower()
            print new_pos.lower()
            if new_pos_full.lower() == new_pos.lower():
                print "$$$"
                return True
        return False
        
# get postcode from an address
def get_pos(address):
    try:
        print "gmaps.places_autocomplete(input_text = address, \
                                                 location = address)"
        print gmaps.places_autocomplete(input_text = address, \
                                                 location = address)
        print "gmaps.places_autocomplete(input_text = address, \
                                                 location = address)[0]"
        print gmaps.places_autocomplete(input_text = address, \
                                                 location = address)[0]
        new_location = gmaps.places_autocomplete(input_text = address, \
                                                 location = address)[0]['description']
        locationId = gmaps.geocode(new_location)[0]['place_id']
        fomattedAddress = gmaps.reverse_geocode(locationId)[0]['formatted_address']
        print fomattedAddress

        postcode = []
        for i in fomattedAddress.split(',')[-2]:
            if i.isdigit():
                postcode.append(i)
        print "get_pos"
        print postcode
        
        return "".join(postcode)
    except:
        print "Error Time Out"
        return

# get postcode from an address
def get_pos2(address):
    postcode = []
    for i in address.split(',')[1]:
        if i.isdigit():
            postcode.append(i)
    return "".join(postcode)

# compare postcode using name:
def get_pos_full(address):
    address = "VIC " + address +",Australia"
    print address
    new_location = gmaps.places_autocomplete(input_text = address, \
                                             location = address)[0]['description']
    print new_location
    return new_location
    
# once confirmed cakes are being processed,change the state of the order
# and update dispatcher info
def update_state2(num,orders,menu_var,window):
    for i in range(num):
        for order in orders[i]:
            # dispatcher_info = menu_var[i].get()
#             dispatcher_name = dispatcher_info.split(",")[index_dis_name]
#
#             for dis in db.dispatchers:
#                 if dis[index_dis_name] == dispatcher_name:
#                     try:
#                         dis[index_dis_orders].append(order.order_number)
#                     except AttributeError:
#                         list1 = convert_data_to_list(dis[index_dis_orders])
#                         list1.append(order.order_number)
#                         dis[index_dis_orders] = list1

            for item in db.orders_all:
                if order == item:
                    item.state = processing
                    if menu_var[i].get() != hint1:
                        item.set_dispatcher(menu_var[i].get())
                    else:
                        item.set_dispatcher("dispatcher not in database")

    db.update_dispatchers()
    db.update()
    refresh_all()
    window.destroy()

# a window contains warning messages
def warning_window(master,message):
    window = Toplevel(master)
    window.title("Warning")
    Label(window,text = message).pack()
    Button(window, text = "ok", command = window.destroy).pack()
    center(window)
    

# reset all listbox and lists in the processing tab
def refresh():
    proc_left_box.clear()
    proc_right_box.clear()
    db.update()
    proc_left_box.update(ctl_num_address(db.orders_leftbox))
    update_dis_listbox()

#########################################################################################
#########################     cake   ####################################################
#########################################################################################
# pack all text labels for cake
def pack_cake_label(window):
    Label(window, text="Size:").grid(row=0,sticky=W)
    Label(window, text="CakeType:").grid(row=1,sticky=W)
    Label(window, text="Quantity:").grid(row=2,sticky=W)
    Label(window, text="Ps:").grid(row=3,sticky=W)

# add cake to the database
def add_cake(size,typee,quan,cake_ps,window,list_box_cakes,cakes):
    if isvalid(cake_ps.get()):
        new_cake = [size.get(),typee.get(),quan.get(),cake_ps.get()]

        print "new_cake:"
        print new_cake
        print "current_cakes(add_cake)"
        print cakes
        # gobal list storing cakes info to be added or edited
        cakes.append(new_cake)
        list_box_cakes.update(cakes)
        window.destroy()
        return True
    else:
        warning_window(master,"input text can only be combinations of \nnumbers,letters, space and comma")
        return False
        
    
# add cake window
def window_add_cake(root,list_box_cakes,cakes):
    window = Toplevel(root)
    window.title("Add a cake")
    window.config(width = 300,height = 180) # 200
    center(window)

    # set labels and entries(option menu)
    var,var2,var3,cake_ps,row_num = pack_cake_entry(window)
    
    print var.get()
    print var2.get()
    print var3.get()
    print cake_ps.get()

    Button(window,text = "add",command = lambda:add_cake(var,var2,\
            var3,cake_ps,window,list_box_cakes,cakes))\
            .grid(row=row_num,column = 0, sticky=W,pady = 4)
    Button(window,text= "cancel",command = window.destroy).\
    grid(row=row_num,column = 1, sticky=W,pady = 4)

# pack text labels for text
def pack_cake_label(window):
    Label(window, text="Size:").grid(row=0,sticky=W,pady = 4)
    Label(window, text="Cake Type:").grid(row=1,sticky=W,pady = 4)
    Label(window, text="Quantity:").grid(row=2,sticky=W,pady = 4)
    Label(window, text="Ps:").grid(row=3,sticky=W,pady = 4)

# set entries and labels for cake manipulation
def pack_cake_entry(window):
    pack_cake_label(window)
    var = StringVar()
    var.set(size[0])
    #read size and type from file
    cake_size = read_cake_size()
    cake_types = read_cake_types()

    cake_size = OptionMenu(window,var, *cake_size)        # option menu for cake size
    cake_size.grid(row=0,column = 1, sticky=W,pady = 4)
    #Button(window,text = "edit size",command= lambda:edit_cake_size(window)).grid(row=0,column = 2, sticky=W,pady = 4)

    var2 = StringVar()
    var2.set(cake_types[0])
    cake_type =OptionMenu(window,var2, *cake_types)   # option menu for cake types
    cake_type.grid(row=1,column = 1, sticky=W,pady = 4)
    #Button(window,text = "edit caketype").grid(row=1,column = 2, sticky=W,pady = 4)


    var3 = StringVar()
    var3.set(quantities[0])
    cake_quan = OptionMenu(window,var3, *quantities)  # option menu for cake quantity
    cake_quan.grid(row=2,column = 1, sticky=W,pady = 4)

    cake_ps = Entry(window)
    cake_ps.grid(row=3,column = 1, sticky=W,pady = 4)
    return var,var2,var3,cake_ps,4

# edit cake info
def edit_cake_window(master,list_box_cakes,cakes):
    if list_box_cakes.selected_rows:
        window = Toplevel(master)
        window.title("Edit a cake")
        window.config(width = 300,height = 200)
        center(window)

        edit_cake = list_box_cakes.selected_rows[0]
        var,var2,var3,cake_ps,row_num = pack_cake_entry(window)

        var.set(edit_cake[index_cake_size])
        var2.set(edit_cake[index_cake_type])
        var3.set(edit_cake[index_cake_quan])
        cake_ps.insert(0,edit_cake[index_cake_ps])

        Button(window,text = "confirm",command = lambda:edit_cake_info(\
            edit_cake,var,var2,var3,cake_ps,window,list_box_cakes,cakes))\
            .grid(row=row_num,column = 0, sticky=W,pady = 4)
        Button(window,text= "cancel",command = window.destroy).\
            grid(row=row_num,column = 1, sticky=W,pady = 4)
    else:
        return

# edit cake info
def edit_cake_info(edit_cake,var,var2,var3,cake_ps,window,list_box_cakes,cakes):
    result = add_cake(var,var2,var3,cake_ps,window,list_box_cakes,cakes)
    if result:
        delete_cake2(edit_cake,list_box_cakes,cakes)
    refresh_all()

# window for deleting selected cake
def delete_cake_window(master,list_box_cakes,cakes):
    print "\n\n\n########################\nlist_box_cakes.selected_rows"
    print list_box_cakes.selected_rows
    print list_box_cakes.selected_rows[0][0]
    print list_box_cakes.selected_rows[0][1]
    print list_box_cakes.selected_rows[0][2]
    print list_box_cakes.selected_rows[0][3]

    if list_box_cakes.selected_rows:
        edit_cake = list_box_cakes.selected_rows[0]

        window = Toplevel(master)
        window.config(width = 300,height = 80)
        center(window)
        window.title("Delete cake")
        Label(window, text="Do you really want to delete this cake?").pack()
        Button(window, text='Confirm', command= lambda:delete_cake(\
            window,edit_cake,list_box_cakes,cakes)).pack()

        Button(window, text='Cancel', command= \
            window.destroy).pack()
    else:
        return

# delete selected cake
def delete_cake(master,edit_cake,list_box_cakes,cakes):
    print "edit cake :"
    print edit_cake
    print "######################"
    print "cakes"
    print cakes
    for cake in cakes:
        print cake
        if cake_cmp(cake,edit_cake):
            cakes.remove(cake)
    print "######################"
    print "after:"
    print cakes
    list_box_cakes.update(cakes)
    master.destroy()

# delete selected  without closing any window
def delete_cake2(edit_cake,list_box_cakes,cakes):
    print "edit cake :"
    print edit_cake
    print "######################"
    print "cakes"
    print cakes
    for cake in cakes:
        print cake
        if cake_cmp(cake,edit_cake):
            cakes.remove(cake)
    print "######################"
    print "after:"
    print cakes
    list_box_cakes.update(cakes)

# compare two cakes
def cake_cmp(c1,c2):
    i = 0
    while i < cake_attr_num:
        print "{} vs {}".format(str(c1[i]),str(c2[i]))
        if not (str(c1[i]) == str(c2[i])):
            return False
        i += 1
    return True

# build a arranged list box according to row number
def build_list_box_cake(window,row_num):
    list_box_cakes = Multicolumn_Listbox(window, header_cake, \
                stripped_rows = ("white","#f2f2f2"), cell_anchor="center",height = 5)
    list_box_cakes.configure_column(0,width = 50)
    list_box_cakes.configure_column(1,width = 80)
    list_box_cakes.configure_column(2,width = 50)
    list_box_cakes.interior.grid(row=row_num, column=0,columnspan =2,rowspan = 3)
    list_box_cakes.interior.bind("<Button-2>", do_popup_cake)
    return list_box_cakes,(row_num+3)

#########################################################################################
#########################     order   ###################################################
#########################################################################################
# delete order from all lists by emptying all lists
def delete_order():
    list_orders.delete(0, END)
    raw_locations[:] = []
    locations[:] = []

# get address
def get_address(na_ad):
    tmp = na_ad.split(',')
    tmp.remove(na_ad.split(',')[0])
    #print tmp
    return tmp

# calculate the route and provide basic info
def run_order():
    if not db.orders_rightbox :
        warning_window(master,warning_message2)
        return
    elif not (proc_entry_num.get() or proc_entry_num_city.get()) :
        warning_window(master,warning_message5)
        return
    print "db.orders_rightbox"
    print db.orders_rightbox
    tmp = db.orders_rightbox
    print "tmp"
    print tmp 
    order_numbers = [">Choose an order"]
    
    if proc_entry_num_city.get() and proc_entry_num.get():
        orders_areas = in_city(db.orders_rightbox,db.postcode[index_city],db.postcode_full[index_city])
        if orders_areas:
            random_order("Melbourne City",int(proc_entry_num_city.get()),orders_areas[index_city],order_numbers)
            random_order("South-east area",int(proc_entry_num.get()),orders_areas[index_other],order_numbers)
        else:
            warning_window(master,"Usage is up to today's limit")
            
    elif proc_entry_num_city.get() and (not proc_entry_num.get() or int(proc_entry_num.get()) == 0):
        random_order("Melbourne City",int(proc_entry_num_city.get()),tmp,order_numbers)
    elif proc_entry_num.get() and (not proc_entry_num_city.get() or int(proc_entry_num_city.get()) == 0):
        random_order("South-east area",int(proc_entry_num.get()),tmp,order_numbers)
  
#assign order randomly
def random_order(title,num_dis,orders_area,order_numbers):
    if orders_area:
        if not db.orders_rightbox:
            print "db.orders_rightbox null (random_order)"
        else:
            print "not null(random_order)"
        tmp = []
        for order in orders_area:
            tmp.append(order)
        random.seed(datetime.now())
        orders = []
        for i in range(num_dis):
            orders.append([])
        if not db.orders_rightbox:
            print "db.orders_rightbox null (random_order)"
        else:
            print "not null(random_order)"
        i = 0
        while tmp:
            if i >= num_dis:
                i = 0
            order = random.choice(tmp)
            orders[i].append(order)
            tmp.remove(order)
            i += 1
        if not db.orders_rightbox:
            print "db.orders_rightbox null (random_order)"
        else:
            print "not null(random_order)"
        manual_order(title,num_dis,tmp,orders,order_numbers)
    else:
        warning_window(master,warning_message7 + title)

# allow user to manually assign orders
def manual_order(title,num_dis,orders_area,orders,order_numbers):
    manual_window = Toplevel(master)
    manual_window.title(title)

    if not db.orders_rightbox:
        print "db.orders_rightbox null (manual_order)"
    listboxes = []
    dispatchers = to_na_ad(db.dispatchers)
    dispatchers.insert(0,hint1)
    menu_var = []
    for i in range(num_dis):
        if i < 6:
            row_num = 0
            col_num = i
        elif 6<= i < 12:
            row_num = 4
            col_num = i-6
        elif 12 <= i < 18:
            row_num = 8
            col_num = i-12

        #set up dispatchers list menu
        var_dis = StringVar()
        var_dis.set(dispatchers[0])
        om_dispatchers = OptionMenu(manual_window,var_dis, *dispatchers)
        menu_var.append(var_dis)

        Label(manual_window,text = "Dispatcher {}".format((i+1))).grid(row=row_num,column=col_num,sticky = W)
        om_dispatchers.grid(row=(row_num+1),column=col_num,sticky = W)
        listbox = Multicolumn_Listbox(manual_window,
                            ['No'],
                            stripped_rows = ("white","#f2f2f2"),
                            cell_anchor="center",
                            height=5,
                            select_mode = EXTENDED)
        listbox.update(to_order2(orders[i]))
        listbox.interior.grid(row = (row_num+2),column =col_num)
        listboxes.append(listbox)
        Button(manual_window,text ="add",command =
                      lambda i=i,orders=orders,listboxes=listboxes,order_numbers=order_numbers
                      : manual_add_window(i,orders,listboxes,order_numbers,manual_window)).grid(row=(row_num+3),column=col_num,sticky = W)
        Button(manual_window,text ="delete",command =
                      lambda i=i,orders=orders,listboxes=listboxes,order_numbers=order_numbers
                      : manual_delete(i,orders,listboxes,order_numbers)).grid(row=(row_num+3),column=col_num,sticky = E,padx=5)
        Button(manual_window,text ="print file and view route",command =
                      lambda i=i:cal_dis(orders[i],menu_var[i].get())).grid(row=(row_num+4),column=col_num,sticky = W)
    Button(manual_window,text ="Confirm all routes",width = 12,
                 command = lambda i=num_dis: update_state2(i,orders,menu_var,manual_window)).grid(row=row_num+5,columnspan = (col_num+1))
    center(manual_window)

 # delete order in corresspoding listbox in the manul window
def manual_delete(i,orders,listboxes,order_numbers):
    if listboxes[i].selected_rows:
        selecteds = listboxes[i].selected_rows
        for selected in selecteds:
            print "i = {}".format(i)
            print selected
            order = get_item_by_num2(selected[0],db.orders_rightbox)
            orders[i].remove(order)
            order_numbers.append([order.order_number,order.address])
            print "manual_delete(order_numbers.append)"
            print order_numbers
            print listboxes[i].indices_of_selected_rows
            listboxes[i].delete_row(listboxes[i].indices_of_selected_rows[0])
            #listboxes[i].update(to_order2(orders[i]))
    else:
        return


# add order to corresspoding listbox in the manul window
def manual_add_window(i,orders,listboxes,order_numbers,window):
    manual_add_window = Toplevel(window)
    manual_add_window.title("Add")

    var = StringVar()
    var.set(order_numbers[0])
    om_order_numebrs = OptionMenu(manual_add_window,var, *order_numbers)

    om_order_numebrs.pack()
    Button(manual_add_window,text ="confirm",command =
                 lambda i=i,var=var,orders=orders,listboxes=
                 listboxes: manual_add(i,var,orders,listboxes,manual_add_window,order_numbers,om_order_numebrs)).pack()
    center(manual_add_window)

# add order to corresspoding listbox
def manual_add(i,var,orders,listboxes,manual_add_window,order_numbers,m):
    if var.get() != "Choose Order":
        order = get_item_by_num(var.get(),db.orders_rightbox)
        orders[i].append(order)
        print "orders[i]"
        for k in orders[i]: 
            print k
        print order_numbers
        order_numbers.remove([order.order_number,order.address])

        menu = m.children['menu']
        # Clear the menu.
        menu.delete(0, 'end')
        for num in order_numbers:
            print num
            # Add menu items.
            menu.add_command(label=num, command=lambda: var.set(num))
        print "###########"
        print listboxes[i].table_data
        for j in orders[i]:
            print j.order_number
            
        listboxes[i].insert_row(to_order2([order])[0])
        last = len(listboxes[i].table_data)-1
        tmp =  listboxes[i].table_data[last]
        listboxes[i].delete_row(last)
        listboxes[i].insert_row(tmp)
        manual_add_window.destroy()


# get list item according to address and order num
def get_item(list,item):
    print "get_item"
    for item1 in list:
        print item1
        print item
        if str(item1.order_number) == str(item[index_no]):
            print "get_item:"
            print item1
            return item1

# get index by item in listbox
def get_index(list,item):
    i = 0
    print item.order_number
    print "\n\n"
    while True:
        print list(i)[index_no]
        if str(list(i)[index_no]) == str(item.order_number):
            return i
        else:
            i += 1

# add left list box items to the right
def left_to_right():
    if not proc_left_box.indices_of_selected_rows:
        return

    selected_indices = proc_left_box.indices_of_selected_rows

    for index in selected_indices:
        listbox_item = proc_left_box.row_data(index)
        proc_right_box.insert_row(listbox_item)
        db.orders_rightbox.append(get_item(db.orders_leftbox,listbox_item))
        proc_left_box.delete_row(index)
        db.orders_leftbox.remove(get_item(db.orders_leftbox,listbox_item))

# add right list box items to the left
def right_to_left():
    if not proc_right_box.indices_of_selected_rows:
        return

    selected_indices = proc_right_box.indices_of_selected_rows

    for index in selected_indices:
        listbox_item = proc_right_box.row_data(index)
        proc_left_box.insert_row(listbox_item)
        db.orders_leftbox.append(get_item(db.orders_rightbox,listbox_item))
        proc_right_box.delete_row(index)
        db.orders_rightbox.remove(get_item(db.orders_rightbox,listbox_item))

# add all left list box items to the right
def add_all():
    for item in db.orders_leftbox:
        db.orders_rightbox.append(item)

    db.orders_leftbox[:] = []
    refresh_all()

# add order to the raw list
def add_order(order,location,name,phone,var2,ps_info,window,dispatcher,current_cakes,
              mode,pickup_date,pickup_time):
    global window_open
    if (order.get() == '' or phone.get() == ''\
        or location.get() == '' or current_cakes == []):
        warning_window(window,warning_message1)
        return False
    else:
        location_g = location.get()

        #add location text to a list in prepare for the later usage
        raw_locations.append(location_g)

        new_order =  Order(order.get(),location.get(),name.get(),phone.get(),\
                           current_cakes,var2.get(),ps_info.get())
        if dispatcher:
             new_order.set_dispatcher(dispatcher)

        if mode.get() != dis:
            new_order.mode = mode.get()

        if pickup_date:
            new_order.pickup_date = pickup_date.get()

        if pickup_time:
            new_order.pickup_time = pickup_time.get()

        db.add(new_order)

        #update listbox after adding new order
        refresh_all()
        print("Order number: %s\nLocation: %s" % (new_order.order_number,
                                                  new_order.address))
        window.destroy()
        # clear this global list of cakes infro after adding/editing
        # action done
        window_open = False
        return True
        
# calendar window
def pop_calendar(window,pickup_date):
    cal_window = Toplevel(window)
    cal_window.title('Calendar')
    ttkcal = Calendar(master=window,firstweekday=calendar.SUNDAY)
    ttkcal.pack(expand=1, fill='both')
    Button(cal_window,text = 'Confirm',command = \
                          lambda:confirm_date(window,ttkcal,pickup_date)).pack()
# confirm canlendar
def confirm_date(window,ttkcal,pickup_date):
    window.destroy()
    pickup_date = ttkcal.selection()
    print pickup_date

# arrange all entries including text lables for windows
# main use is to avoid duplicate codes
def pack_order_entry(window,cakes,item):
    order = Entry(window)                  # text entry for order
    location = Entry(window)               # location entry for order
    name = Entry(window)                   # name entry for order
    phone = Entry(window)                  # phone number
    ps_info = Entry(window)                # plus info about the order
    pickup_date = Entry(window)
    pickup_time = Entry(window)

    var2 = StringVar()                     # option menu for order state
    var2.set(states[0])
    state =OptionMenu(window,var2,*states)

    var_mode = StringVar()                 # option menu for mode
    var_mode.set(modes[0])
    mode =OptionMenu(window,var_mode,*modes)

    if item:
        # put placeholders for the convenience of user to edit details of an order
        order.insert(0,item.order_number)
        location.insert(0,item.address)
        name.insert(0,item.name)
        phone.insert(0,item.phone)
        var2.set(item.state)
        ps_info.insert(0,item.ps_info)
        var_mode.set(item.mode)
        print "item.pickup_date"
        print item.pickup_date
        print "item.pickup_time"
        print item.pickup_time
        if item.pickup_date:
            pickup_date.insert(0,item.pickup_date)
        if item.pickup_time:
            pickup_time.insert(0,item.pickup_time)

    order.grid(row=0, column=1,sticky=W)
    location.grid(row=1, column=1,sticky=W)
    name.grid(row=2, column=1,sticky=W)
    phone.grid(row=3, column=1,sticky=W)
    list_box_cakes,row_num = pack_order_label(window)

    state.grid(row=4, column=1,sticky=W)
    mode.grid(row=5,column = 1,sticky=W)
    pickup_date.grid(row=6,column = 1,sticky=W)
    pickup_time.grid(row=7,sticky=W,column = 1)
    ps_info.grid(row=8,column = 1,sticky=W)

    Button(window, text='Add Cake', command= \
            lambda:window_add_cake(window,\
            list_box_cakes,cakes)).grid(row=9, column=1,sticky=W)

    Button(window,text= "settings",command = \
            lambda: cake_setting_window(window)).\
            grid(row=9,column = 1, sticky=E)


    row_num = (row_num)
    return order,location,name,phone,var2,ps_info,row_num,list_box_cakes,var_mode,pickup_date,pickup_time

# pack all text labels
def pack_order_label(window):
    Label(window, text="Order Number*:").grid(row=0,sticky=W)
    Label(window, text="Location(St+postcode)*:").grid(row=1,sticky=W)
    Label(window, text="Name:").grid(row=2,sticky=W)
    Label(window, text="Phone*:").grid(row=3,sticky=W)
    Label(window, text="State*:").grid(row=4,sticky=W)
    Label(window, text="Mode:").grid(row=5,sticky=W)
    Label(window, text="Pickup Date:").grid(row=6,sticky=W)
    Label(window, text="Pickup Time:").grid(row=7,sticky=W)
    Label(window, text="Ps:").grid(row=8,sticky=W)
    Label(window, text="Cakes*:").grid(row=9,sticky=W)
    list_box_cakes,row_num = build_list_box_cake(window,10)
    return list_box_cakes,(row_num+2)

# add order window
def window_add_order():
    global window_open,popup_cake
    if not window_open:
        #window_open = True
        window = Toplevel(master)
        window.title("Add an order")

        cakes = []
        # user inputs
        order,location,name,phone,var2,ps_info,row_num,list_box_cakes,\
            mode,pickup_date,pickup_time =\
            pack_order_entry(window,cakes,None)

        # popup Menu for cake
        popup_cake = Menu(window,tearoff = 0)
        popup_cake.add_command(label="Display Info(Edit)",command = \
            lambda:edit_cake_window(window,list_box_cakes,cakes))
        popup_cake.add_command(label="Delete",command = \
            lambda:delete_cake_window(window,list_box_cakes,cakes))
        popup_cake.add_separator()

        Label(window, text = " fields with (*) cant be empty").\
            grid(row=row_num,columnspan = 2,pady = 4)
        Button(window, text='Add', command= \
               lambda:add_order(order,location,name,phone,\
                                var2,ps_info,window,None,cakes,\
                                mode,pickup_date,pickup_time)).\
               grid(row=(row_num+1), column=0,columnspan = 2, pady=4)
        center(window)

    else:
        return

# create a new window for editing an order history
def edit_info_his(master):
    global window_open,popup_cake
    item = get_selected_order()
    if item and not window_open:
        #window_open = True
        check_select_state()
        window = Toplevel(master)
        window.title("Edit order")

        current_cakes = item.cake_type
        print "item.cake_type"
        print current_cakes

        # popup Menu for cake
        popup_cake = Menu(window,tearoff = 0)
        popup_cake.add_command(label="Display Info(Edit)",command = \
            lambda:edit_cake_window(window,list_box_cakes,current_cakes))
        popup_cake.add_command(label="Delete",command = \
            lambda:delete_cake_window(window,list_box_cakes,current_cakes))
        popup_cake.add_separator()

        # user inputs
        order,location,name,phone,var2,ps_info,row_num,list_box_cakes,\
             mode,pickup_date,pickup_time = \
             pack_order_entry(window,current_cakes,item)

        list_box_cakes.update(current_cakes)
        Label(window,text="Dispatcher:").grid(row=row_num,column=0,sticky=W, pady=4)
        entry_dis = Entry(window)
        entry_dis.grid(row=row_num,column=1,sticky=W, pady=4)
        row_num += 1
        print "dissssssssssss"
        print item.dispatcher
        if item.dispatcher:
            entry_dis.insert(0,item.dispatcher)
        Button(window, text='Confirm', command= \
               lambda: edit_order(order,location,name,phone,\
                                   var2,ps_info,item,window,current_cakes\
                                   ,mode,pickup_date,pickup_time,entry_dis.get())).\
           grid(row=row_num,sticky=W, pady=4)
        center(window)
    else:
        return

# create a new window for editing an order
def edit_info(master):
    global window_open,popup_cake
    item = get_selected_order()
    if item and not window_open:
        #window_open = True
        check_select_state()
        window = Toplevel(master)
        window.title("Edit order")

        current_cakes = item.cake_type
        print "item.cake_type"
        print current_cakes

        # popup Menu for cake
        popup_cake = Menu(window,tearoff = 0)
        popup_cake.add_command(label="Display Info(Edit)",command = \
            lambda:edit_cake_window(window,list_box_cakes,current_cakes))
        popup_cake.add_command(label="Delete",command = \
            lambda:delete_cake_window(window,list_box_cakes,current_cakes))
        popup_cake.add_separator()

        # user inputs
        order,location,name,phone,var2,ps_info,row_num,list_box_cakes,\
             mode,pickup_date,pickup_time = \
             pack_order_entry(window,current_cakes,item)

        list_box_cakes.update(current_cakes)

        Button(window, text='Confirm', command= \
               lambda: edit_order(order,location,name,phone,\
                                   var2,ps_info,item,window,current_cakes\
                                   ,mode,pickup_date,pickup_time,item.dispatcher)).\
           grid(row=row_num, columnspan=2, pady=4)
        center(window)
    else:
        return

# edit order info
def edit_order(order,location,name,phone,\
               var2,ps_info,pre_order,window,cakes,
               mode,pickup_date,pickup_time,entry_dis):
    if entry_dis:
        result = add_order(order,location,name,phone,\
                    var2,ps_info,window,entry_dis,cakes\
                    ,mode,pickup_date,pickup_time)
    else:
        result = add_order(order,location,name,phone,\
                   var2,ps_info,window,None,cakes\
                   ,mode,pickup_date,pickup_time)
    if result:
        delete_order2(pre_order)
        
    refresh_all()

# window used for user to confirm deletion of an order
def delete_window(master):
    item = get_selected_order()
    print item
    if item:
        check_select_state()
        window = Toplevel(master)
        window.title("Delete order")
        window.config(width = 400,height = 80)
        center(window)
        Label(window, text="Do you really want to delete order number " + \
              item.order_number).pack()
        Button(window, text='Confirm', command= lambda:delete_order(item,window)).pack()

        Button(window, text='Cancel', command= \
            window.destroy).pack()
    else:
        return
        
# multiple delete
def delete_selected(listbox):
    print "delete_selected"
    if listbox.indices_of_selected_rows:
        list_orders = []
        list_order_nums =[]
        selected_indices = listbox.indices_of_selected_rows
        for index in selected_indices:
            print listbox.row_data(index)
            order = get_item(db.orders_all,listbox.row_data(index))
            print order
            list_orders.append(order)
            list_order_nums.append(order.order_number)
        
        # notify user to make sure he/she confirm the deletion
        window = Toplevel(master)
        window.title("Delete order")
        window.config(width = 400,height = 80)
        center(window)
        Label(window, text="Do you really want to delete order number " + \
              ",".join(list_order_nums)).pack()
        Button(window, text='Confirm', command= lambda:delete_order3(list_orders,window)).pack()

        Button(window, text='Cancel', command= \
            window.destroy).pack() 
        
    else:
        return

# delete an order
def delete_order(order,window):
    db.delete(order)
    refresh_all()
    window.destroy()

def delete_order2(order):
    db.delete(order)
    refresh_all()

# delete an order
def delete_order3(orders,window):
    for order in orders:
        db.delete(order)
    refresh_all()
    window.destroy()

# search order inside today list box
def search_listbox_today(input):
    search(input,today_list_box_all,db.orders_today)

# search order inside history list box
def search_listbox_history(input):
    search(input,history_listbox,db.orders_history)
    return

# search an order by any attribute
def search(input,listbox,orders):
    print "input"
    print input
    listbox.deselect_all()
    for item in orders:
        print item
        for sub_item in class_to_order(item):
            print "sub_item"
            print sub_item
            try:
                if sub_item and (input.lower() == sub_item.lower()):
                    print "found " + input
                    index = get_index(listbox.row_data,item)
                    listbox.select_row(index)
            # in this case, it should be list of cakes
            except AttributeError:
                for cake in sub_item:
                    for el in cake:
                        if input.lower() == el.lower():
                            print "found " + input
                            index = get_index(listbox.row_data,item)
                            listbox.select_row(index)


# deselect all selected items in processing tab
def deselect_proc():
    proc_left_box.deselect_all()
    proc_left_box.deselect_all()

# deselect all selected items in today tab
def deselect_today():
    today_list_box_all.deselect_all()
    today_list_box_processing.deselect_all()

# deselect all selected items in history tab
def deselect_his():
    history_listbox.deselect_all()

# find out which and where an item is selected (eg. index and listbox)
def find_selected_item():
    selected_indices = []
    return_list = []
    if today_list_box_all.indices_of_selected_rows:
       selected_indices = today_list_box_all.indices_of_selected_rows
       return_list = [selected_indices[0],today_list_box_all,db.orders_today]
       print "find_selected_item:"
       print  selected_indices[0]
    elif today_list_box_processing.indices_of_selected_rows:
       selected_indices = today_list_box_processing.indices_of_selected_rows
       return_list = [selected_indices[0],today_list_box_processing,db.orders_proc]
    elif history_listbox.indices_of_selected_rows:
      selected_indices = history_listbox.indices_of_selected_rows
      return_list = [selected_indices[0],history_listbox,db.orders_history]

    elif proc_right_box.indices_of_selected_rows:
        selected_indices = proc_right_box.indices_of_selected_rows
        return_list = [selected_indices[0],proc_right_box,db.orders_rightbox]
    elif proc_left_box.indices_of_selected_rows:
        selected_indices = proc_left_box.indices_of_selected_rows
        return_list = [selected_indices[0],proc_left_box,db.orders_leftbox]

    return return_list

# get info about selected item(order)
def get_selected_order():
    if find_selected_item():
        print "item found"
        selected_info = find_selected_item()
        listbox = selected_info[1]
        orders = selected_info[2]
        order = get_item(orders,listbox.row_data(selected_info[0]))
        print listbox.row_data(selected_info[0])
        return order
    else:
        return None

#refresh all listboxes
def refresh_all():
    update_dis_listbox()
    today_list_box_processing.update(class_to_list_without_info2(db.orders_proc))
    today_list_box_all.update(o2lists_mode(db.orders_today))
    proc_left_box.update(ctl_num_address(db.orders_leftbox))
    proc_right_box.update(ctl_num_address(db.orders_rightbox))
    history_listbox.update(class_to_list_without_info(db.orders_history))

#########################################################################################
#########################     menu   ####################################################
#########################################################################################
# bind popup menu to histotry listbox
def do_popup_his(event):
    # display the popup menu
    try:
        popup_his.tk_popup(event.x_root, event.y_root)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup_his.grab_release()

# bind popup menu to today/proc_left listbox
def do_popup(event):
    # display the popup menu
    try:
        popup.tk_popup(event.x_root, event.y_root)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()

# bind popup menu to cake listbox
def do_popup_cake(event):
    # display the popup menu
    try:
        popup_cake.tk_popup(event.x_root, event.y_root)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup_cake.grab_release()

# bind popup menu to dis listbox
def do_popup_dis(event):
    # display the popup menu
    try:
        popup_dis.tk_popup(event.x_root, event.y_root)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup_dis.grab_release()

# make sure only items of exact one listbox can be selected at one time
def check_select_state():
    tabtitle = tabControl.tab(tabControl.select(), "text")
    if tabtitle == "Today":
        deselect_proc()
        deselect_his()
    elif tabtitle == "History":
        deselect_proc()
        deselect_today()
    elif tabtitle == "Processing":
        deselect_his()
        deselect_today()

def do_deselect(event):
    print("Mouse position: (%s %s)" % (event.x, event.y))

#########################################################################################
#########################     dispatcher   ##############################################
#########################################################################################
# pack all text labels for dispatcher window
def pack_dis_label(window):
    Label(window, text="Name*:").grid(row=0,sticky=W,pady = 4)
    Label(window, text="Home(St+postcode)*:").grid(row=1,sticky=W,pady = 4)
    Label(window, text="Phone*::").grid(row=2,sticky=W,pady = 4)
    Label(window, text="Ps:").grid(row=3,sticky=W,pady = 4)

# arrange all entries including text lables for windows
# main use is to avoid duplicate codes
def pack_dis_entry(window):
    name = Entry(window)                # anem entry for dispatcher
    home = Entry(window)                # location entry for dispatcher
    phone = Entry(window)               # phone entry for dispatcher
    ps_info = Entry(window)             # plus info about the dispatcher

    pack_dis_label(window)
    name.grid(row=0, column=1,sticky=W,pady = 4)
    home.grid(row=1, column=1,sticky=W,pady = 4)
    phone.grid(row=2, column=1,sticky=W,pady = 4)
    ps_info.grid(row=3, column=1,sticky=W,pady = 4)

    return name,home,phone,ps_info,4

# add dispatchers window
def add_dispatchers_window(master):
    window = Toplevel(master)
    window.title("add dispatchers")
    window.config(width = 350,height = 185)
    center(window)

    name,home,phone,ps_info,row_num = pack_dis_entry(window)

    Button(window,text = "confirm",command = lambda:add_dispatcher(\
        name,home,phone,ps_info,window))\
        .grid(row=row_num,column = 0, sticky=W,pady = 4)
    Button(window,text= "cancel",command = window.destroy).\
        grid(row=row_num,column = 1, sticky=W,pady = 4)

# add dispatcher to the database
def add_dispatcher(name,home,phone,ps_info,window):
    new_dispatcher = [name.get(),home.get(),phone.get(),ps_info.get()]
    db.dispatchers.append(new_dispatcher)
    refresh_all()
    window.destroy()

# show dispatchers info on listbox
def update_dis_listbox():
    db.update_dispatchers()
    proc_left_box_dis.update(show_dis(db.dispatchers))


# edit dispatcher info
def edit_info_dis(master):
    if proc_left_box_dis.selected_rows:
        dis = proc_left_box_dis.selected_rows[0]
        print dis
        print dis[0]
        window = Toplevel(master)
        window.title("edit")
        window.config(width = 350,height = 185)
        center(window)

        name,home,phone,ps_info,row_num = pack_dis_entry(window)
        name.insert(0,dis[index_dis_name])
        home.insert(0,dis[index_dis_home])
        phone.insert(0,dis[index_dis_phone])
        ps_info.insert(0,dis[index_dis_ps])

        Button(window,text = "confirm",command = lambda:edit_dispatcher(\
            name,home,phone,ps_info,window,dis))\
            .grid(row=row_num,column = 0, sticky=W,pady = 4)
        Button(window,text= "cancel",command = window.destroy).\
            grid(row=row_num,column = 1, sticky=W,pady = 4)
    else:
        return


# add dispatcher to the database
def edit_dispatcher(name,home,phone,ps_info,window,old_dis):
    old_dispatcher = find_dis(db.dispatchers,old_dis)
    db.dispatchers.remove(old_dispatcher)
    new_dispatcher = [name.get(),home.get(),phone.get(),ps_info.get()]
    db.dispatchers.append(new_dispatcher)
    refresh_all()
    window.destroy()

# delete dispatcher
def delete_window_dis():
    if proc_left_box_dis.selected_rows:
        selected_dis = proc_left_box_dis.selected_rows[0]
        disp = find_dis(db.dispatchers,selected_dis)
        db.dispatchers.remove(disp)
        db.update_dispatchers()
        proc_left_box_dis.update(db.dispatchers)
    else:
        return

# only get first two data(name,address) to show in the listbox
def to_na_ad(old_list):
    dispatchers = []
    for dis in old_list:
        print "rip(dis[index_dis_name]"
        print rip(dis[index_dis_name])
        dispatchers.append("".join([rip(dis[index_dis_name]) + "," +dis[index_dis_home]]))
        #dispatchers.append("".join([dis[index_dis_name] + "," +dis[index_dis_home]]))
    return dispatchers
#rip off comma
def rip(name):
    new_name = []
    for i in name:
        if not i.isalpha() and  not i.isdigit():
            new_name.append(' ')
        else:
            new_name.append(i)
    return "".join(new_name)

# find dispatcher
def find_dis(list,disp):
    for dis in list:
        if str(dis[index_dis_name]) == str(disp[index_dis_name])\
           and str(dis[index_dis_home]) == str(disp[index_dis_home]):
           return dis
    return None

# build x scrollbar and y scrollbar for each tab
def build_scrollbar(container):
    canvas = Canvas(container, highlightthickness=0)
    xscroll = Scrollbar(container,orient="horizontal",command=canvas.xview)
    yscroll = Scrollbar(container,command=canvas.yview)
    canvas.config(xscrollcommand=xscroll.set,
                  yscrollcommand=yscroll.set,
                  scrollregion=(0,0,1210,500),
                  width=1200,height=490)

    xscroll.pack(side=BOTTOM, fill=X)
    yscroll.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    tab = Frame(canvas)
    canvas.create_window((0,0),window=tab,anchor='nw')

    return tab

#########################################################################################
#########################     settings   ################################################
#########################################################################################
#  setting window to modify the option of cake size, cake type etc.
def cake_setting_window(root):
    window = Toplevel(root)
    window.title("Setting")
    tmp_size = read_cake_size()
    tmp_type = read_cake_types()

    # listbox of size
    size_listbox = Multicolumn_Listbox(window,
                        ['Size'],
                        stripped_rows = ("white","#f2f2f2"),
                        cell_anchor="center",
                        height=5)

    size_listbox.update(to_listbox(tmp_size))
    size_listbox.interior.grid(row = 0,column =0)
    Button(window,text ="add",command = lambda: cake_setting_add_window(\
                        window,"size",size_listbox,tmp_size)).grid(row = 1,column =0,sticky=W)
    Button(window,text ="delele",command = lambda: cake_setting_delete(\
                        size_listbox,tmp_size)).\
                        grid(row = 1,column =0,sticky=E)

    # listbox of cake type
    type_listbox = Multicolumn_Listbox(window,
                        ['Cake Type'],
                        stripped_rows = ("white","#f2f2f2"),
                        cell_anchor="center",
                        height=5)
    type_listbox.update(to_listbox(tmp_type))
    type_listbox.interior.grid(row = 0,column =1)
    Button(window,text ="add",command = lambda: cake_setting_add_window(\
                        window,"type",type_listbox,tmp_type)).grid(row = 1,column =1,sticky=W)
    Button(window,text ="delele",command = lambda: cake_setting_delete(\
                        type_listbox,tmp_type)).grid(row = 1,column =1,sticky=E)
    Button(window,text ="confirm",command = \
                        lambda: cake_setting_confirm(window,tmp_size,tmp_type)).grid(row = 2,columnspan =2,pady =4)
    center(window)

# confirm all the changes
def cake_setting_confirm(window,size,types):
     f = open(file_size,'wb')
     f.truncate()
     writer = csv.writer(f,delimiter = ',')
     writer.writerow(size)
     f.close()

     f = open(file_type,'wb')
     f.truncate()
     writer = csv.writer(f,delimiter = ',')
     writer.writerow(types)
     f.close()

     window.destroy()
# add size/type
def cake_setting_add_window(window,indicator,listbox,list1):
    cake_setting_add_window = Toplevel(window)
    cake_setting_add_window.title("Add")
    Label(cake_setting_add_window,text = "new {}:".format(indicator)).\
                     grid(sticky =W,row=0,column =0,pady = 4)
    entry = Entry(cake_setting_add_window)
    entry.grid(sticky =W,row=0,column =1,pady = 4)
    Button(cake_setting_add_window,text = "confirm",command = \
                     lambda :cake_setting_add(indicator,listbox,entry,cake_setting_add_window,list1)).\
                     grid(row=1,columnspan =2,pady = 4)
    center(cake_setting_add_window)

# add it to the database
def cake_setting_add(indicator,listbox,entry,window,list1):
    new_size = entry.get()
    list1.append(new_size)
    listbox.update(to_listbox(list1))
    window.destroy()

# delete size/type
def cake_setting_delete(listbox,list1):
    if listbox.selected_rows:
        selected = listbox.selected_rows[0]
        print selected[0]
        print list1
        try:
            list1.remove(str(selected[0]))
        except UnicodeEncodeError:
            list1.remove(selected[0])

        listbox.update(to_listbox(list1))
    else:
        return

# about window
def about():
    window = Toplevel(master)
    window.title("About")
    image = Image.open(logo)
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    labimg = Label(window, image=photo)
    labimg.image = photo
    labimg.pack(fill = "both", expand = "yes")
    Label(window,text ="Copyright 2017-2018 Happy Hackers Pty Ltd. All rights reserved.").pack()

# open hh website
def open_web():
    webbrowser.open("http://happyhackers.com.au")

############## MAIN FUNCTION ##################################################
############## MAIN FUNCTION ##################################################
############## MAIN FUNCTION ##################################################
############## MAIN FUNCTION ##################################################
if __name__ == "__main__":
    f2 = open(file_postcode_full, "rb")
    reader = csv.reader(f2,delimiter=',')
    for line in reader:
        print line
    f2.close()
    
    # main window setup
    master = Tk()
    master.title("iCake")

    # scrollbar = Scrollbar(master)
#     scrollbar.pack(side=BOTTOM, fill=X)

    db = []                              # orders database
    raw_locations = []                   # list of locations from user input
    locations = []                       # list of locations from googlemaps api
    orders = {}                          # dictionary of ({id:info})
    infos = []                           # info of an order(ps_info)
    start_locationId = None              # the initial start location
    tabControl = ttk.Notebook(master)    # tab controller
    dis_right = []                       # list of dispatchers in the rilistbox
    tab_today = None
    tab_history = None
    tab_proc = None
    tab_dis = None

    db = Orders_database(file_order)
    #tab for 'Today','History','Processing'
    tab_today_container =Frame(tabControl,relief=GROOVE,width=50,height=100,bd=0)
    tab_today_container.place(x=10,y=10)
    tabControl.add(tab_today_container, text='Today')

    tab_history_container =Frame(tabControl,relief=GROOVE,width=50,height=100,bd=0)
    tab_history_container.place(x=10,y=10)
    tabControl.add(tab_history_container, text='History')

    tab_proc_container =Frame(tabControl,relief=GROOVE,width=50,height=100,bd=0)
    tab_proc_container.place(x=10,y=10)
    tabControl.add(tab_proc_container, text='Processing')

    tab_dis_container =Frame(tabControl,relief=GROOVE,width=50,height=100,bd=0)
    tab_dis_container.place(x=10,y=10)
    tabControl.add(tab_dis_container, text ='Dispatcher')

    # build x scrollbar and y scrollbar for each tab
    # if statement to speed up the loading when switching tabs
    if not tab_today:
        tab_today = build_scrollbar(tab_today_container)
    if not tab_history:
        tab_history = build_scrollbar(tab_history_container)
    if not tab_dis:
        tab_proc = build_scrollbar(tab_proc_container)
    if not tab_dis:
        tab_dis = build_scrollbar(tab_dis_container)

    # background_image= PhotoImage("1.png")
    # background_label = Label(tab_today, image=background_image)
    # background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # popup Menu
    popup = Menu(master,tearoff = 0)
    popup.add_command(label="Display Info(Edit)",command = lambda:edit_info(master))
    popup.add_command(label="Delete",command = lambda:delete_window(master))
    popup.add_separator()

    # popup Menu for dispatcher
    popup_dis = Menu(tab_proc,tearoff = 0)
    popup_dis.add_command(label="Display Info(Edit)",command = lambda:edit_info_dis(master))
    popup_dis.add_command(label="Delete",command = lambda:delete_window_dis())
    popup_dis.add_separator()

    popup_his = Menu(master,tearoff = 0)
    popup_his.add_command(label="Display Info(Edit)",command = lambda:edit_info_his(master))
    popup_his.add_command(label="Delete",command = lambda:delete_window(master))
    popup_his.add_separator()

    # menu for app about
    menubar = Menu(master)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="About",command=about)
    filemenu.add_command(label= "View website",command=open_web)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=master.quit)
    menubar.add_cascade(label="App", menu=filemenu)

    master.config(menu=menubar)
#########################################TAB1############################################
    # set up ui for 'Today'
    today_search = Entry(tab_today)
    today_add_order = Button(tab_today, text = 'add order',command =window_add_order)
    today_button_search = Button(tab_today, text = 'search',command =\
                                 lambda:search_listbox_today(today_search.\
                                                             get()))
    today_button_refresh = Button(tab_today, text = 'refresh',command =\
                                  refresh_all)
    today_list_box_all = Multicolumn_Listbox(tab_today, header_today, \
                            stripped_rows = ("white","#f2f2f2"), \
                            cell_anchor="center",height=14,select_mode = EXTENDED)
    today_button_multiple_delete = Button(tab_today, text = 'delete',command =\
                                  lambda:delete_selected(today_list_box_all))
    today_list_box_all.configure_column(3,width = 150)
    today_list_box_all.configure_column(4,width = 250)
    today_list_box_processing = Multicolumn_Listbox(\
                            tab_today, header_proc, stripped_rows = \
                            ("white","#f2f2f2"), cell_anchor="center",height=7)
    today_text_orders_all = Label(tab_today, text="Orders",font=("Calibri",title_size))
    today_text_processing = Label(tab_today, text="Dispatching Orders (display only, modification not allowed)",font=("Calibri",title_size))


    # bind listbox to popup menu
    today_list_box_all.interior.bind("<Button-2>", do_popup)
    today_list_box_all.interior.bind("<Button-1>", do_deselect)


    today_text_orders_all.grid(row=0,column=0,sticky = W,padx =4)
    today_search.grid(row=0,column=1, sticky = E)
    today_button_search.grid(row = 0,column =2, sticky = W,padx =4)
    today_button_refresh.grid(row = 0,column = 4, sticky = E)
    #today_button_multiple_delete.grid(row=0,column=0, sticky = E)
    today_add_order.grid(row=0,column=3, sticky = E)
    today_text_processing.grid(row=2,sticky = W,padx = 4)
    today_list_box_all.interior.grid(row=1,pady=4,columnspan =5)
    today_list_box_processing.interior.grid(row=3,pady=4,columnspan =5)

########################################TAB2#############################################
    # set up ui for 'History'
    # history_date = Entry(tab_history)
    history_search = Entry(tab_history)

    history_button_search = Button(tab_history, text = 'search',command =\
                                 lambda:search_listbox_history(history_search.get()))
    # history_listbox = Listbox(tab_history, width = 70,height = 20)
    history_listbox = Multicolumn_Listbox(tab_history,header_full, \
                            stripped_rows = ("white","#f2f2f2"), cell_anchor="center"\
                                          ,height=22,select_mode = EXTENDED)
    history_button_refresh = Button(tab_history, text = 'refresh',command =\
                                  refresh_all)

    history_listbox.interior.bind("<Button-2>", do_popup_his)
    #history_date.grid(row = 0,column = 0,sticky = W)
    Label(tab_history,text = 'History of all arrived orders',font=("Calibri",title_size)).\
                      grid(row=0,column = 0,sticky = W,padx=4)
    history_search.grid(row=0,column = 4,sticky = E,padx=4)
    history_button_refresh.grid(row=0,column =9,pady=4,sticky =E)
    history_button_search.grid(row = 0,column = 5,sticky=W)
    history_listbox.interior.grid(row=1,column = 0,columnspan = 10,pady=4)

#########################################TAB3############################################
    # set up ui for 'Processing'

    #orders ui elements
    proc_text_name = Label(tab_proc, text ="Dispatch Orders",font = ("Calibri",title_size))
    proc_entry_num = Entry(tab_proc)
    proc_entry_num_city = Entry(tab_proc)
    proc_entry_num.insert(0,1)
    proc_ps = Label(tab_proc, text = "*Only waiting orders can be\n assigned to dispatcher")
    proc_left_box = Multicolumn_Listbox(tab_proc, header_small, \
                        stripped_rows = ("white","#f2f2f2"), cell_anchor="center",\
                                        height=20,select_mode = EXTENDED)
    proc_right_box = Multicolumn_Listbox(tab_proc, header_small, \
                        stripped_rows = ("white","#f2f2f2"), cell_anchor="center",\
                                        height=20)
    proc_add_all_button = Button(tab_proc, text = "add all",command = add_all)
    proc_add_button = Button(tab_proc, text = ">",command = left_to_right)
    proc_delete_button = Button(tab_proc, text = "<",command = right_to_left)

    proc_clear_button = Button(tab_proc, text = "refresh",\
                               command = refresh)
    proc_run_button = Button(tab_proc, text = "run",command = run_order,\
                             width=8)
    # proc_manually_button = Button(tab_proc, text = "manually assgin orders",command = manually_run,\
    #                          width=20)
    proc_start_loc = Entry(tab_proc)
    proc_end_loc = Entry(tab_proc)
    proc_start_loc.insert(0,start_location)

    #orders ui elements setup
    proc_left_box.interior.bind("<Button-2>", do_popup)
    proc_text_name.grid(row = 0, column = 0,sticky=W)
    Label(tab_proc, text ="Waiting to be dispatched").grid(row=1,column = 0,pady=4,sticky = W)
    proc_left_box.interior.grid(row=2,rowspan = 10,column = 0,columnspan =2)
    Label(tab_proc, text ="Ready to be dispatched").grid(row=1,column = 3,pady=4,sticky = W)
    proc_right_box.interior.grid(row=2,rowspan = 10,column = 3,columnspan =2)
    proc_add_all_button.grid(row =5, column =2)
    proc_add_button.grid(row =4,column = 2)
    proc_delete_button.grid(row =6,column = 2)
    proc_clear_button.grid(row =12,column=0,sticky = W)
    proc_ps.grid(row = 12,column = 1,sticky = W)

    Label(tab_proc, text = "Start location:").grid(row = 1,column =5,padx = 30,sticky = W)
    proc_start_loc.grid(row=2,column = 5,sticky = W,padx = 30,ipady = 10)
    Label(tab_proc, text = "Enter number of dispatchers\n(South-east Area):").grid(row = 3,column =5,padx = 30,sticky = W)
    proc_entry_num.grid(row=4,column = 5,sticky = W,padx = 30)
    Label(tab_proc, text = "Enter number of dispatchers\n(Melbourne City):").grid(row = 5,column =5,padx = 30,sticky = W)
    proc_entry_num_city.grid(row=6,column = 5,sticky = W,padx = 30)

    proc_run_button.grid(row = 7,column =5,sticky = W,padx = 30)
    # Label(tab_proc, text = "Or").grid(row = 8,column =5,padx = 30,sticky = W)
 #    proc_manually_button.grid(row = 9,column =5,padx = 30,sticky = W)

#########################################TAB4############################################
    # set up ui for dispatcher
    #dispatcher
    proc_left_box_dis = Multicolumn_Listbox(tab_dis, header_dispatcher_full, \
                        stripped_rows = ("white","#f2f2f2"), cell_anchor="center",\
                                        height=22)
    proc_left_box_dis.interior.bind("<Button-2>", do_popup_dis)
    proc_add_dispatcher_button = Button(tab_dis, text = "Add new dispatchers",\
                        command = lambda: add_dispatchers_window(tab_proc))

    Label(tab_dis, text ="Manage dispathcers",font=("Calibri",title_size))\
                .grid(row=0,column = 0,pady=4,sticky = W)
    proc_left_box_dis.interior.grid(row=1,rowspan = 7,column = 0,columnspan =5)
    proc_add_dispatcher_button.grid(row =0,column=4,sticky = E,pady = 4)

    #image
    image2 = Image.open(logo)
    image2 = image2.resize((200, 200), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(image2)
    labimg2 = Label(tab_dis, image=photo2)
    labimg2.image = photo2
    #image

    labimg2.grid(row = 3,column =5,padx = 30,sticky = S)
    Label(tab_dis, text = "Contact  admin@happyhackers.com.au \nIf there is any problem.",font=("Calibri",17)).grid(row = 6,column =5,padx = 30,sticky = S)
    Label(tab_dis, text = "This application is designed by  Happy Hackers Pty Ltd. \nAll rights reserved",font=("Calibri",15),foreground = 'gray').grid(row = 7,column =5,padx = 30,sticky = N)
    refresh_all()

    tabControl.pack(fill=BOTH, expand=YES)
    mainloop( )




