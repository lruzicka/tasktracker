#!/usr/bin/python

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Minimalistic TaskTracker")

buttonframe = ttk.Frame(root, padding="2 5 5 5")
buttonframe.grid(column=0, row=1, sticky=(N, W, E, S))
infoframe = ttk.Frame(root, width=600, height=480, padding="2 5 2 5")
infoframe.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Button(buttonframe, text="Save task", width=15).grid(column=0, row=0, sticky=(W, E))
ttk.Button(buttonframe, text="Show tasks", width=15).grid(column=1, row=0, sticky=(W, E))

ttk.Label(infoframe, text="Task description:", padding="2 1 5 1").grid(column=0, row=0, sticky=(E))
ttk.Label(infoframe, text="Task type:", padding="2 1 5 1").grid(column=0, row=1, sticky=(E))
ttk.Label(infoframe, text="Task product:", padding="2 1 5 1").grid(column=0, row=2, sticky=(E))
ttk.Label(infoframe, text="Task Fedora type:", padding="2 1 5 1").grid(column=0, row=3, sticky=(E))
ttk.Label(infoframe, text="Task keywords:", padding="2 1 5 1").grid(column=0, row=4, sticky=(E))
ttk.Label(infoframe, text="Task link:", padding="2 1 5 1").grid(column=0, row=5, sticky=(E))

description = ttk.Entry(infoframe, width=50)
description.grid(column=1, row=0, sticky=(W, E))



root.mainloop()

