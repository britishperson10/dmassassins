#!/bin/python
# Copyright (C) Joseph Rohani
import sys, urllib.request, os, shutil

class Flags:
    def choose_flag(flag):
        pass

def check_dir(path="data"):
    if not os.path.exists((path+"/")):
        os.mkdir(path)

def download(name, ow=False, path="data"):
    global location, file_location
    location=os.path.dirname(os.path.realpath(__file__))+"/data/"+name+"/"
    file_location=location+name
    if os.path.exists(location):
        answer=input("The path exists, would you like to overwrite the path[y/N]:  ")
        if answer=="y" or answer=="Y":
            shutil.rmtree(f"{path}/{name}")
            os.mkdir(f"data/{name}")
        else:
            print("Closing program")
            exit(0)
    elif not os.path.exists(location):
        os.mkdir(f"data/{name}")
    url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name}"
    urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
    print(f"File saved to:  {location}")

def sift(data):
    print(location)
    file=open(file_location, "r")
    line_list=[]
    for (i, line) in enumerate(file):
        if data in line:
            line_list.append(i)
    print(line_list)

check_dir()
name=sys.argv[1]
download(name) #Add sys flags

sift(name.upper())

