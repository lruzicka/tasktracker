#!/usr/bin/python3

import datetime
import json
import os
import time

class Parser:
    def __init__(self):
        pass

class Timer:
    def __init__(self):
        self.timestamp = time.time()
    
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
        timeback = count * periods[unit]
        return round(self.timestamp - int(timeback))

    def return_start_date(self, timestamp):
        """ Returns the time from epoch for the given $timestamp passed as "DD Mon YY". """
        taim = time.strptime(timestamp, "%d %b %y")
        start = datetime.datetime(taim.tm_year, taim.tm_mon, taim.tm_mday).timestamp()
        return round(start)

    def current_timestamp(self):
        """ Returns current timestamp. """
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
                    print(data)
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
        results = self.diary
        round_results = []
        if timestamp:
            specs.append("timestamp")
        if typ:
            specs.append("typ")
        if group:
            specs.append("group")
        if qa:
            specs.append("qa")
        if keywords:
            specs.append("keywords")
        if link:
            specs.append("link")

        while len(specs) > 0:
            s = specs.pop(0)
            for task in results:
                if s == "typ" and typ in task["type_of_task"]:
                    round_results.append(task)
                elif s == "group" and group in task["task_class"]:
                    round_results.append(task)
                elif s == "qa" and qa in task["fedora_qa_group"]:
                    round_results.append(task)
                elif s == "keywords":
                    keywords = keywords.split(',')
                    gotores = False
                    for k in keywords:
                        if k in task["keywords"]:
                            gotores = True
                    if gotores:
                        round_results.append(task)
                elif s == "link" and link in task["link_to_task"]:
                    round_results.append(task)
                elif s == "timestamp" and int(task["time_of_creation"]) >= int(timestamp):
                    round_results.append(task)
            results = round_results
        if results:
            return results
        else:
            return []

class Entry:
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

def main():
    clock = Timer()
    diary = Diary('completed_tasks')
    activity = input("What to do? (sHow/Save): ") or "S"

    if activity == "S":
        description = input("Task description: ")
        typ = input("Task type (bug, fix, test, ...): ") or "bug"
        group = input("Project group: ") or "fedora"
        qa = input("Fedora QA group (fedora, automation, ...): ") or "fedora"
        keywords = input("Keywords (one,two): ")
        link = input("Link: (BZ/number, PG/repo/number): ")
        link = unpack_link(link)

        entry = Entry()
        entry.create(clock.current_timestamp(), description, typ, group, qa, keywords, link)

        diary.append_file(entry.json())
        print("The task was saved.")

    elif activity == "H":
        specify = input("Do you want to specify the search? (y/n): ") or "n"
        if specify == "y":
            timecreate = input("Search start (DD MMM YY) or how far back (1-day, 2-week): ")
            if timecreate == "":
                timecreate = "01 Jan 00"
            timecreate = timecreate.split('-')
            if len(timecreate) > 1:
                timestamp = clock.return_start_time(int(timecreate[0]), timecreate[1])
            else:
                timestamp = clock.return_start_date(timecreate[0])
            typ = input("Search for type: ")
            group = input("Search for project group: ")
            qa = input("Search for Fedora QA group: ")
            keywords = input("Search for keywords: ")
            link = input("Search in links: ")

            tasks = diary.return_tasks(timestamp, typ, group, qa, keywords, link)
        else:
            tasks = diary.diary
        for t in tasks:
            print(t)
    else:
        print('Action was not recognized, quitting.')


if __name__ == "__main__":
    main()
    
