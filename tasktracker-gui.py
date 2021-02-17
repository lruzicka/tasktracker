#!/usr/bin/python

import tkinter as tk
from tkinter import ttk
from tkinter import * 

# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = descrip.get()
	return userInput


# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = ttype.get()
	return userInput


# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = pgroup.get()
	return userInput


# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = qasection.get()
	return userInput


# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = keywords.get()
	return userInput


# this is a function to get the user input from the text input box
def getInputBoxValue():
	userInput = link.get()
	return userInput

def getCheckboxValue():
	checkedOrNot = markbool.get()
	return checkedOrNot

# this is the function called when the button is clicked
def btn_save():
    value_desc = descrip.get()
    descrip.delete(0, END)
    value_ttype = ttype.get()
    ttype.delete(0, END)
    value_pgroup = pgroup.get()
    pgroup.delete(0, END)
    value_qasection = qasection.get()
    qasection.delete(0, END)
    value_keywords = keywords.get()
    keywords.delete(0, END)
    value_link = link.get()
    link.delete(0, END)
    output = [value_desc, value_ttype, value_pgroup, value_qasection, value_keywords, value_link]
    descrip.focus()
    print(output)


# this is the function called when the button is clicked
def btn_show():
	print('clicked')

# this is the function called when the button is clicked
def btn_copy():
	print('clicked')


root = Tk()

# This is the section of code which creates the main window
#root.geometry('867x542')
root.configure(background='#F0F8FF')
root.title('Weekly Highlights TaskTracker')

markbool = tk.IntVar()

# Frames - Info, Text, Buttons
entries = Frame(root, bg='#F0F8FF')
entries.grid(column=0,row=0, padx=5,pady=5)

buttons = Frame(root, bg='#F0F8FF')
buttons.grid(column=0,row=2, columnspan=2, pady=10)

text = Frame(root, bg='#F0F8FF')
text.grid(column=1,row=0, padx=5, pady=5, rowspan=2)

search = Frame(root, bg='#F0F8FF')
search.grid(column=0, row=1, padx=5, pady=5)


# This is the section of code which creates the a label
Label(entries, text='Task description:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=0, sticky=(W))
Label(entries, text='Task type:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=1, sticky=(W))
Label(entries, text='Task Project group:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=2, sticky=(W))
Label(entries, text='Fedora QA section:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=3, sticky=(W))
Label(entries, text='Task Keywords:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=4, sticky=(W))
Label(entries, text='Link to task:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=5, sticky=(W))


# This is the section of code which creates a text input box
descrip=Entry(entries, width=50)
descrip.grid(column=1,row=0)

ttype=Entry(entries, width=50)
ttype.grid(column=1,row=1, sticky=(W))

pgroup=Entry(entries, width=50)
pgroup.grid(column=1,row=2, sticky=(W))

qasection=Entry(entries, width=50)
qasection.grid(column=1,row=3, sticky=(W))

keywords=Entry(entries, width=50)
keywords.grid(column=1,row=4, sticky=(W))

link=Entry(entries,width=50)
link.grid(column=1,row=5, sticky=(W))


# This is the section of code which creates a button
Button(buttons, text='Save task', bg='#22CFAA', font=('arial', 12, 'normal'), command=btn_save).grid(column=0,row=0, padx=3)
Button(buttons, text='Show tasks', bg='#88FFAA', font=('arial', 12, 'normal'), command=btn_show).grid(column=1,row=0, padx=3)
Button(buttons, text='Copy text', bg='#AACFAA', font=('arial', 12, 'normal'), command=btn_copy).grid(column=2,row=0, padx=3)


# This defines the text field
textfield = Text(text)
textfield.grid(column=0, row=0)

# This defines the search criteria
Label(entries, text='History units:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=6, sticky=(W))
Label(entries, text='Number of units:', bg='#F0F8FF', font=('arial', 12, 'normal')).grid(column=0,row=7, sticky=(W))

# This is the section of code which creates a listbox
unittype = Entry(entries, width=50)
unittype.grid(column=1, row=6, sticky=(W))

unitnumber = Entry(entries, width=50)
unitnumber.grid(column=1, row=7, sticky=(W))

# This is the section of code which creates a checkbox
CheckBoxOne=Checkbutton(entries, text='Markdown', variable=markbool, bg='#F0F8FF', font=('arial', 12, 'normal'))
CheckBoxOne.grid(column=1, row=8, pady=5, sticky=(W))

root.mainloop()

