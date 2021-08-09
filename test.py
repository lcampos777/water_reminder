# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Create an instance of ttk style
s = ttk.Style()
s.theme_use('default')
s.configure('TNotebook.Tab', background="green3")
s.map("TNotebook", background= [("selected", "green3")])

# Create a Notebook widget
nb = ttk.Notebook(win)

# Add a frame for adding a new tab
f1= ttk.Frame(nb, width= 400, height=180)

# Adding the Tab Name
nb.add(f1, text= 'Tkinter-1')
f2 = ttk.Frame(nb, width= 400, height=180)
nb.add(f2, text= "Tkinter-2")

nb.pack(expand= True, fill=BOTH, padx= 5, pady=5)
win.mainloop()