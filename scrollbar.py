from Tkinter import *
import ttk

def data(tab_today):
    # set up ui for 'Today'
    today_search = Entry(tab_today)
    today_text_orders_all = Label(tab_today, text="Orders")
    today_text_processing = Label(tab_today, text="Dispatching Orders")

    today_text_orders_all.grid(row=0,column=0,sticky = W,padx =4)
    today_search.grid(row=0,column=1, sticky = E)
    today_text_processing.grid(row=2,sticky = W,padx = 4)

def myfunction(event):
    canvas.configure(scrollregion=(0,0,1000,1000),width=1000,height=300)

root=Tk()

tabControl = ttk.Notebook(root)    # tab controller


#
# myframe=Frame(tabControl,relief=GROOVE,width=50,height=100,bd=1)
# myframe.place(x=10,y=10)
# tabControl.add(myframe, text='History')
# tabControl.pack(fill=BOTH, expand=YES)
#
#
# canvas=Canvas(myframe)
# myscrollbar=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
# canvas.configure(xscrollcommand=myscrollbar.set)
#
# myscrollbar.pack(side="bottom",fill="x")
# canvas.pack(side="left")
# tab_today=Frame(canvas)
#
# canvas.create_window((0,0),window=tab_today,anchor='nw')
#
# tab_today.bind("<Configure>",myfunction)

#################################################################################
tab_today_container =Frame(tabControl,relief=GROOVE,width=50,height=100,bd=0)
tab_today_container.place(x=10,y=10)
tabControl.add(tab_today_container, text='Today')
tabControl.pack(fill=BOTH, expand=YES)

canvas = Canvas(tab_today_container)
scroll = Scrollbar(tab_today_container,orient="horizontal",command=canvas.xview)
canvas.config(xscrollcommand=scroll.set)

scroll.pack(side=BOTTOM, fill=X)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
tab_today = Frame(canvas)
    
canvas.create_window((0,0),window=tab_today,anchor='nw')
tab_today.bind("<Configure>",myfunction)

data(tab_today)
root.mainloop()