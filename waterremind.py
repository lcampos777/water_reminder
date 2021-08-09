#pyinstaller --windowed --onefile --icon=./clock.ico app.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import datetime as dt
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from playsound import playsound
from win10toast_click import ToastNotifier

#creating main container
root = Tk()
root.title("Water Reminder")
#root.geometry("500x300+0+0")
root.iconbitmap("water.ico")
root.resizable(False,False)

#create notification object
toaster = ToastNotifier()

#colors
main_color = "#52489c"
second_color ="#4062bb"
third_color = "#59c3c3"
font_color = "#ebebeb"
button_color = "#f45b69"


#creating styles
style = ttk.Style()
style.theme_use("clam")

#root.config(background=main_color)

#Notebook style
style.configure("NB_Style.TNotebook.Tab", background=main_color, foreground=font_color, font=("Helvetica", 18, "bold"))
style.map("NB_Style.TNotebook.Tab", background=[("selected", main_color), ("active",second_color),])

#Buttons style
style.configure("BTN_Style.TButton",background=second_color, foreground=font_color, highlightthickness="20", font=("Helvetica", 18, "bold"))

style.map("BTN_Style.TButton",
    foreground=[("disabled", third_color),
                ("pressed", third_color),
                ("active", font_color)],
    background=[("disabled", button_color),
                ("pressed", "!focus", font_color),
                ("active", button_color)],
    highlightcolor=[("focus", second_color),
                ("!focus", third_color)],
    relief=[("pressed", "groove"),
                ("!pressed", "ridge")])

#Label Frame style
style.configure("LBFR_Style.TLabelframe", background=main_color, foreground=font_color, font=("Helvetica", 18, "bold"))

#Labels Style
style.configure("Label_Style.TLabel", background=second_color, foreground=font_color, font=("Helvetica", 18, "bold"))
style.configure("Label_Style2.TLabel", background=second_color, foreground=font_color, font=("Helvetica", 40, "bold"))

#function to add data to the log
def drink_check():
    drink_check = mb.askyesno(title="Water Reminder", message="Did you drink water?")
    log_dt = str(dt.now())

    with open("log.txt","a") as f:
        f.write(f"On {log_dt} --> {drink_check}\n")


#Sets the default value for the timer
def reset_timer():
    btn_stop.config(state="disabled")
    btn_start.config(state="enable")
    if len(minutes_var.get())==2 and len(seconds_var.get())==2:
        timer_var.set(f"0{hours_var.get()}:{minutes_var.get()}:{seconds_var.get()}")
    elif len(minutes_var.get())==2 and len(seconds_var.get())==1:
        timer_var.set(f"0{hours_var.get()}:{minutes_var.get()}:0{seconds_var.get()}")
    elif len(minutes_var.get())==1 and len(seconds_var.get())==1:
        timer_var.set(f"0{hours_var.get()}:0{minutes_var.get()}:0{seconds_var.get()}")
    elif len(minutes_var.get())==1 and len(seconds_var.get())==2:
        timer_var.set(f"0{hours_var.get()}:0{minutes_var.get()}:{seconds_var.get()}")

#starts the timer
def start_timer():
    btn_stop.config(state="enable")
    btn_start.config(state="disabled")
    hours = int(timer_var.get()[0:2])
    minutes = int(timer_var.get()[3:5])
    seconds = int(timer_var.get()[6:])

    seconds -= 1
    if seconds < 0:
        seconds = 59
        minutes -= 1

    if seconds == 0:
        if minutes == 0:
            minutes = 0
        else:
            minutes -= 1
            seconds = 59
    
    if minutes == 0:
        if hours == 0:
            hours = 0
        else:
            hours -= 1
            minutes = 59

    if len(str(minutes))==2 and len(str(seconds))==2:
        timer_var.set(f"0{hours}:{minutes}:{seconds}")

    elif len(str(minutes))==2 and len(str(seconds))==1:
        timer_var.set(f"0{hours}:{minutes}:0{seconds}")

    elif len(str(minutes))==1 and len(str(seconds))==1:
        timer_var.set(f"0{hours}:0{minutes}:0{seconds}")

    elif len(str(minutes))==1 and len(str(seconds))==2:
        timer_var.set(f"0{hours}:0{minutes}:{seconds}")
    
    global cancel_var
    cancel_var = root.after(1000,start_timer)

    if timer_var.get() == "00:00:00":
        root.after_cancel(cancel_var)
        playsound("Morning.mp3")
        toaster.show_toast(title="Drink Water", msg="Please remember to drink water",threaded=True,icon_path="water.ico")
        drink_check()


#stops the timer
def stop_timer():
    btn_stop.config(state="disabled")
    btn_start.config(state="enable")
    root.after_cancel(cancel_var)

#Create the notebook
nb_main = ttk.Notebook(root, style="NB_Style.TNotebook")
nb_main.pack()

#Create notebook"s tabs
frm_main = ttk.Frame(nb_main, width=480, height=280)
frm_main.pack()

frm_settings = ttk.Frame(nb_main, width=480, height=280)
frm_settings.pack(fill=BOTH)

#Adding tabs to the notebook
nb_main.add(frm_main, text="Water Reminder")
nb_main.add(frm_settings, text="Settings")

#Creater Timer label frame
lbl_frm_timer = ttk.LabelFrame(frm_main, text="Timer", style="LBFR_Style.TLabelframe")
lbl_frm_timer.pack(fill=BOTH)

#create timer label and variable
timer_var = StringVar(value="00:00:00")
lbl_timer = ttk.Label(lbl_frm_timer, textvariable=timer_var, justify="center", style="Label_Style2.TLabel")
lbl_timer.grid(row=0, column=0, columnspan=3, pady=20)

#create timer buttons
btn_start = ttk.Button(lbl_frm_timer, text="Start", command=start_timer, style="BTN_Style.TButton")
btn_start.grid(row=1, column=0)

btn_stop = ttk.Button(lbl_frm_timer, text="Stop", command=stop_timer, state="disabled", style="BTN_Style.TButton")
btn_stop.grid(row=1, column=1)

btn_reset = ttk.Button(lbl_frm_timer, text="Reset", command=reset_timer, style="BTN_Style.TButton")
btn_reset.grid(row=1, column=2)

#create settings label frame
lbl_frm_settings = ttk.Labelframe(frm_settings, text="Settings", style="LBFR_Style.TLabelframe")
lbl_frm_settings.pack(fill=BOTH)

#create settings labels
lbl_hours = ttk.Label(lbl_frm_settings, text="Hours", justify="left", style="Label_Style.TLabel")
lbl_hours.grid(row=0, column=0, sticky=E, padx=5, pady=10)

lbl_minutes = ttk.Label(lbl_frm_settings, text="Minutes", justify="left", style="Label_Style.TLabel")
lbl_minutes.grid(row=1, column=0, sticky=E, padx=5, pady=10)

lbl_seconds = ttk.Label(lbl_frm_settings, text="Seconds", justify="left", style="Label_Style.TLabel")
lbl_seconds.grid(row=2, column=0, sticky=E, padx=5, pady=10)

#create settings spinboxes and variables
hours_var = StringVar(value=0)
minutes_var = StringVar(value=30)
seconds_var = StringVar(value=0)

spb_hours = ttk.Spinbox(lbl_frm_settings, from_=0, to=2, justify="center", wrap=True, textvariable=hours_var, state="readonly")
spb_hours.grid(row=0, column=1, sticky=W, padx=5, pady=10)

spb_minutes = ttk.Spinbox(lbl_frm_settings, from_=0, to=59, justify="center", wrap=True, textvariable=minutes_var, state="readonly")
spb_minutes.grid(row=1, column=1, sticky=W, padx=5, pady=10)

spb_seconds = ttk.Spinbox(lbl_frm_settings, from_=0, to=59, justify="center", wrap=True, textvariable=seconds_var, state="readonly")
spb_seconds.grid(row=2, column=1, sticky=W, padx=5, pady=10)

reset_timer()

#print(lbl_frm_settings.winfo_class())
#print(btn_reset.config())
#print(style.layout("TLabelframe"))
#print(style.element_options("Labelframe.border"))
#print(style.element_options("Button.focus"))
#print(style.element_options("Button.padding"))
#print(style.element_options("Button.label"))


root.mainloop()