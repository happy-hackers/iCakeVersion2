from tkinter import *
import ttk


def demo():
    #root = tk.Tk()
    master = Tk()

    master.title("tab sample")

    tabControl = ttk.Notebook(master)

    # adding Frames as pages for the ttk.Notebook
    # first page, which would get widgets gridded into it
    page1 = ttk.Frame(tabControl, width= 800,height = 600)
    # second page
    page2 = ttk.Frame(tabControl,width = 800,height = 600)

    tabControl.add(page1, text='One')
    tabControl.add(page2, text='Two')

    tabControl.pack()
    
    day_label = Label(page1, text="Day1:")
    day_label.pack()
    day_label.place(x=0, y=30)

    day_label = Label(page2, text="Day2:")
    day_label.pack()
    day_label.place(x=0, y=30)

    master.mainloop()

if __name__ == "__main__":
    demo()