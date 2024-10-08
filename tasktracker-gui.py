#!/usr/bin/python3

import datetime
import json
import os
import time
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import *

class Timer:
    def __init__(self):
        self.timestamp = round(time.time())

    def return_start_time(self, count, unit):
        """ Returns the time from epoch calculated from the current timestamp back in time.

        Takes $count of selected $unit, i.e. minute, hour, day, week, month, year. """
        periods = {
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 2635200,
            "year": 31536000,
        }
        if not count:
            count = 1
        if not unit:
            unit = 'day'
        timeback = count * periods[unit]
        return round(self.timestamp - int(timeback))

    def return_start_date(self, timestamp):
        """ Returns the time from epoch for the given $timestamp passed as "DD Mon YY". """
        taim = time.strptime(timestamp, "%d %b %y")
        start = datetime.datetime(taim.tm_year, taim.tm_mon, taim.tm_mday).timestamp()
        return round(start)

    def current_timestamp(self):
        """ Returns current timestamp. """
        self.timestamp = round(time.time())
        return self.timestamp

class Diary:
    def __init__(self, dfile):
        self.dfile = dfile
        self.diary = []
        try:
            with open(self.dfile, 'r') as diary:
                diary_data = diary.readlines()
                for data in diary_data:
                    self.diary.append(json.loads(data))
        except FileNotFoundError:
            self.diary = []

    def append_file(self, entry):
        with open(self.dfile, 'a') as diary:
            diary.write(entry)
            diary.write("\n")

    def show_stats(self):
        count = len(self.diary)
        return count

    def return_tasks(self, timestamp=None, typ=None, group=None, qa=None, keywords=None, link=None):
        specs = []
        results = self.diary[:]
        part = []
        if timestamp:
            for task in results:
                if timestamp < task["time_of_creation"]:
                    part.append(task)
            results = part[:]
            part = []
        if typ:
            for task in results:
                if typ in task["type_of_task"]:
                    part.append(task)
            results = part[:]
            part = []
        if group:
            for task in results:
                if group in task["task_class"]:
                    part.append(task)
            results = part[:]
            part = []
        if qa:
            for task in results:
                if qa in task["fedora_qa_group"]:
                    part.append(task)
            results = part[:]
            part = []
        if keywords:
            keywords = keywords.split(',')
            for task in results:
                for key in keywords:
                    if key in task["keywords"]:
                        part.append(task)
            results = part[:]
            part = []
        if link:
            for task in results:
                if link in task["link_to_task"]:
                    part.append(task)
            results = part[:]
            part = []
        return results

class Dentry:
    def __init__(self):
        self.creation = 0
        self.task = ""
        self.typ = ""
        self.group = ""
        self.qa_group = ""
        self.keywords = []
        self.link = ""

    def create(self, timestamp, task, typ=None, group=None, qa_group=None, keywords=None, link=None):
        self.creation = timestamp
        self.task = task
        if typ:
            self.typ = typ
        if group:
            self.group = group
        if link:
            self.link = link
        if qa_group:
            self.qa_group = qa_group
        if keywords:
            kwords = keywords.split(',')
            self.keywords = kwords

    def json(self):
        jsondata = {
            "time_of_creation": self.creation,
            "description": self.task,
            "type_of_task": self.typ,
            "fedora_qa_group": self.qa_group,
            "task_class": self.group,
            "keywords": self.keywords,
            "link_to_task": self.link
        }
        return json.dumps(jsondata)

def unpack_link(link):
    unpacked = link.split('/')
    if len(unpacked) == 1:
        return link
    else:
        if unpacked[0] == "BZ":
            l = f"https://bugzilla.redhat.com/show_bug.cgi?id={unpacked[1]}"
        elif unpacked[0] == "PG":
            l = f"https://pagure.io/{unpacked[1]}/issue/{unpacked[2]}"
        else:
            l = link
        return l

# this is the function called when the button is clicked
def btn_save():
    """ Collects the info from the form and saves it into the file."""
    # Collect the date from the form
    value_desc = descrip.get()
    descrip.delete(0, END)
    if not value_desc:
        textfield.delete(1.0, END)
        textfield.insert(END, "No description was provided, task was not saved.")
    else:
        value_ttype = str(selected_task.get())
        value_pgroup = str(selected_project.get())
        value_qasection = str(selected_section.get())
        value_keywords = keywords.get()
        keywords.delete(0, END)
        value_link = link.get()
        value_link = unpack_link(value_link)
        link.delete(0, END)
        descrip.focus()
        # Create the entry
        dentry = Dentry()
        timestamp = clock.current_timestamp()
        dentry.create(timestamp, value_desc, value_ttype, value_pgroup, value_qasection, value_keywords, value_link)
        # Save into the file
        diary.append_file(dentry.json())
        textfield.delete(1.0, END)
        textfield.insert(END, f"Task '{value_desc[:15]}...' was succesfully saved.\n")
        # Delete selected
        selected_task.set("")
        selected_project.set("")
        selected_section.set("")


# this is the function called when the button is clicked
def btn_show():
    diary = Diary(datafile)
    value_ttype = str(selected_task.get())
    value_pgroup = str(selected_project.get())
    value_qasection = str(selected_section.get())
    value_keywords = keywords.get()
    keywords.delete(0, END)
    value_unit = str(selected_unit.get())
    value_number = str(selected_number.get())
    markdown = markbool.get()
    ttype.focus()
    timecreate = f"{value_number}-{value_unit}"
    if timecreate == "-":
        timecreate = "01 Jan 00"
    timecreate = timecreate.split('-')
    if len(timecreate) > 1:
        if not timecreate[0]:
            # When no numbers are filled, assume 1
            starttime = clock.return_start_time(1, timecreate[1])
        else:
            starttime = clock.return_start_time(int(timecreate[0]), timecreate[1])
    else:
        starttime = clock.return_start_date(timecreate[0])

    tasks = diary.return_tasks(starttime, value_ttype, value_pgroup, value_qasection, value_keywords)
    textfield.delete(1.0, END)
    for t in tasks:
        if markdown == 1:
            textfield.insert(END, f"* {t['description']} ({t['link_to_task']})\n")
        else:
            textfield.insert(END, f"{t['description']} ({t['link_to_task']})\n")

def btn_today():
    diary = Diary(datafile)
    markdown = markbool.get()
    ttype.focus()
    timecreate = "1-day"
    timecreate = timecreate.split('-')
    if len(timecreate) > 1:
        timestamp = clock.return_start_time(1, "day")
    else:
        timestamp = clock.return_start_date(1)

    tasks = diary.return_tasks(timestamp, "", "", "", "")
    textfield.delete(1.0, END)
    for t in tasks:
        if markdown == 1:
            textfield.insert(END, f"* {t['description']} ({t['link_to_task']})\n")
        else:
            textfield.insert(END, f"{t['description']} ({t['link_to_task']})\n")

def btn_week():
    diary = Diary(datafile)
    markdown = markbool.get()
    ttype.focus()
    timecreate = "1-week"
    timecreate = timecreate.split('-')
    if len(timecreate) > 1:
        timestamp = clock.return_start_time(int(timecreate[0]), timecreate[1])
    else:
        timestamp = clock.return_start_date(timecreate[0])

    tasks = diary.return_tasks(timestamp, "", "", "", "")
    textfield.delete(1.0, END)
    for t in tasks:
        if markdown == 1:
            textfield.insert(END, f"* {t['description']} ({t['link_to_task']})\n")
        else:
            textfield.insert(END, f"{t['description']} ({t['link_to_task']})\n")

# this is the function called when the button is clicked
def btn_copy():
    textcopy = textfield.get("1.0", END)
    root.clipboard_clear()
    root.clipboard_append(textcopy)
    root.update() # now it stays on the clipboard after the window is closed

def load_choices():
    choices = {}
    with open('choices.txt', 'r') as chFile:
        content = chFile.readlines()
    for line in content:
        group, items = line.split(':')
        listed = items.split(',')
        listed = [item.strip() for item in listed]
        listed.sort()
        listed.append("")
        choices[group] = listed
    return choices



root = Tk()

# This is the section of code which creates the main window
#root.geometry('867x542')
#root.configure(background='#EEEEEE')
root.title('Weekly Highlights TaskTracker')

markbool = tk.IntVar()

# Frames - Info, Text, Buttons
entries = Frame(root)
entries.grid(column=0,row=0, padx=5,pady=5)

buttons = Frame(root)
buttons.grid(column=0,row=2, columnspan=2, pady=10)

text = Frame(root)
text.grid(column=1,row=0, padx=5, pady=5, rowspan=2)

search = Frame(root)
search.grid(column=0, row=1, padx=5, pady=5)

choices = load_choices()

# This is the section of code which creates the a label
Label(entries, text='Task description:', font=('arial', 12, 'normal')).grid(column=0,row=0, sticky=(W))
Label(entries, text='Task type:', font=('arial', 12, 'normal')).grid(column=0,row=1, sticky=(W))
Label(entries, text='Task target:', font=('arial', 12, 'normal')).grid(column=0,row=2, sticky=(W))
Label(entries, text='Task group:', font=('arial', 12, 'normal')).grid(column=0,row=3, sticky=(W))
Label(entries, text='Additional keywords:', font=('arial', 12, 'normal')).grid(column=0,row=4, sticky=(W))
Label(entries, text='Link to task:', font=('arial', 12, 'normal')).grid(column=0,row=5, sticky=(W))


# This is the section of code which creates a text input box
descrip=Entry(entries, width=50)
descrip.grid(column=1,row=0)
descrip.focus()

try:
    tasks = choices['tasks']
except KeyError:
    tasks = [""]

selected_task = StringVar(entries)
selected_task.set("")
ttype=OptionMenu(entries, selected_task, *tasks)
ttype.grid(column=1,row=1, sticky=(W))

try:
    projects = choices['group']
except KeyError:
    projects = [""]

selected_project = StringVar(entries)
selected_project.set("")
pgroup=OptionMenu(entries, selected_project, *projects)
pgroup.grid(column=1,row=2, sticky=(W))

try:
    sections = choices['section']
except KeyError:
    sections = [""]

selected_section = StringVar(entries)
selected_section.set("")
qasection=OptionMenu(entries, selected_section, *sections)
qasection.grid(column=1,row=3, sticky=(W))

keywords=Entry(entries, width=50)
keywords.grid(column=1,row=4, sticky=(W))

link=Entry(entries,width=50)
link.grid(column=1,row=5, sticky=(W))


# This is the section of code which creates a button
Button(buttons, text='Save task', bg='#FFAAAA', font=('arial', 12, 'normal'), command=btn_save).grid(column=0,row=0, padx=3)
Button(buttons, text='Show tasks', bg='#AAFFAA', font=('arial', 12, 'normal'), command=btn_show).grid(column=1,row=0, padx=3)
Button(buttons, text='All 1 day', bg='#AAFFFF', font=('arial', 12, 'normal'), command=btn_today).grid(column=2,row=0, padx=3)
Button(buttons, text='All 1 week', bg='#AADDDD', font=('arial', 12, 'normal'), command=btn_week).grid(column=3,row=0, padx=3)
Button(buttons, text='Copy text', bg='#EEEEEE', font=('arial', 12, 'normal'), command=btn_copy).grid(column=4,row=0, padx=3)


# This defines the text field
textfield = Text(text)
textfield.grid(column=0, row=0)

# This defines the search criteria
Label(entries, text='History units:', font=('arial', 12, 'normal')).grid(column=0,row=6, sticky=(W))
Label(entries, text='Number of units:', font=('arial', 12, 'normal')).grid(column=0,row=7, sticky=(W))

# This is the section of code which creates an option menu
units = ["", "minute", "hour", "day", "week", "month", "year"]
selected_unit = StringVar(entries)
selected_unit.set("")
unittype = OptionMenu(entries, selected_unit, *units)
unittype.grid(column=1, row=6, sticky=(W))

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
selected_number = StringVar(entries)
selected_number.set("1")
unitnumber = OptionMenu(entries, selected_number, *numbers)
unitnumber.grid(column=1, row=7, sticky=(W))

# This is the section of code which creates a checkbox
CheckBoxOne=Checkbutton(entries, text='Markdown', variable=markbool, font=('arial', 12, 'normal'))
CheckBoxOne.grid(column=1, row=8, pady=5, sticky=(W))

clock = Timer()
try:
    datafile = sys.argv[1]
except IndexError:
    datafile = 'completed_tasks.json'
diary = Diary(datafile)

root.mainloop()
