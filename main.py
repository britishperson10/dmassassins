#!/bin/python
# Copyright (C) Joseph Rohani
import sys, urllib.request, os, shutil, time
global DEBUG
if "-d" in sys.argv:
    DEBUG=True
else:
    DEBUG=False
class Flags:
    def choose_flag(argc, argv):
        for x in argv:
            if x=="-h" or x=="--help":
                print("")

def check_dir(path="data"):
    if not os.path.exists((path+"/")):
        os.mkdir(path)

def download(name, ow=False, path="data"):
    global location, file_location
    name_orig=name
    name=name.lower()
    location=os.path.dirname(os.path.realpath(__file__))+"/data/"+name+"/"
    file_location=location+name
    if os.path.exists(location):
        
        if DEBUG:  pass
        elif input("The path exists, would you like to overwrite the path[y/N]:  ").lower()=="y":
            shutil.rmtree(f"{path}/{name}")
            os.mkdir(f"data/{name}")
            url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name}"
            urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
            print(f"File saved to:  {location}")
        elif answer.lower()=="r":
            pass
        else:
            print("Closing program")
            exit(0)
    else:
        os.mkdir(f"data/{name}")
        url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name}"
        urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
        print(f"File saved to:  {location}")

    

def sift(data):
    print(location)
    file=open(file_location, "r")
    line_list=[]
    for (i, line) in enumerate(file):
        line_upper=line.upper()
        if data in line_upper:
            line_list.append(i)
    file_contents=file.readlines()
    print(line_list)
    print(file_contents)
    print(file)
    for x in line_list:
        print(x)
        print(file_contents[x])
    
    


check_dir()
try:
    name=sys.argv[1]
except:
    name=input("Please enter a name:  ")
start=time.time()
download(name) #Add sys flags
print(time.time()-start)
start=time.time()
sift(input("data: ").upper())
print(time.time()-start)

