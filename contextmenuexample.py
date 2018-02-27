import Tkinter as tk
import ttk

class Page(tk.Frame):
    def __init__(self, parent, controller):
        self.root = parent;
        self.button = tk.Button(parent, text="Treeview", command=self.ChildWindow)
        self.button.pack()


    def ChildWindow(self):

        #Create menu
        self.popup = tk.Menu(self.root, tearoff=0)
        self.popup.add_command(label="Next", command=self.selection)
        self.popup.add_separator()

        def do_popup(event):
            # display the popup menu
            try:
                self.popup.selection = self.tree.set(self.tree.identify_row(event.y))
                self.popup.post(event.x_root, event.y_root)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.popup.grab_release()

        #Create Treeview
        win2 = tk.Toplevel(self.root)
        new_element_header=['1st']
        treeScroll = ttk.Scrollbar(win2)
        treeScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree = ttk.Treeview(win2, columns=new_element_header, show="headings")
        self.tree.heading("1st", text="1st")
        self.tree.insert("" ,  0, text="Line 1", values=("1A"))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH)

        self.tree.bind("<Button-3>", do_popup)

        win2.minsize(600,30)

    def selection(self):
        print self.popup.selection

root = tk.Tk()

Page(root, None)

root.mainloop()

def main():
    pass
if __name__ == '__main__':
    main()