#!/bin/python
# September 03, 2022
# Copyright (C) 2022 Joseph Rohani
# Just realised that this shit might not work on Windows due to the goofy ass file system, also I know, excessive lib use
# Synopsis:  Files are saved to data folder under the name, then refined are saved to name_reined
import sys, urllib.request, os, shutil, time, datetime
global DEBUG
if "-d" in sys.argv:
    DEBUG=True
else:
    DEBUG=False
class Flags:
    def choose_flag(argv):
        # l=0
        for x in argv:
            if x=="-h" or x=="--help":
                print("--HELP PAGE--\nFlags:\n\t-h or --help:  This output\n\t-d:  Enable weird debug stuff that might be removed by the time I release this\n\t-s: The refined search data\n\t-o: Specify data output location, wouldn't recommend using this\n\t-r: if file exists, reuse it, can put \"r\" into the yes no prompt for same result\n\t-O: Overwrite existing file\n\t-p: Print the output data to the terminal\n\nMade by Joseph Rohani")
                exit(0)
def check_dir(path="data"):
    if not os.path.exists((path+"/")):
        os.mkdir(path)

def download(name, ow=False, path="data"):
    global file_location, locationname
    name=name.lower()
    location=os.path.dirname(os.path.realpath(__file__))+"/data/"+name+"/"
    file_location=location+name
    if os.path.exists(location):
        
        if DEBUG or "-r" in sys.argv:  pass
        elif "-O" in sys.argv:
            shutil.rmtree(f"{path}/{name}")
            os.mkdir(f"data/{name}")
            url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name}"
            start=time.time()
            urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
            end=time.time()
            print(f"File saved to:  {location}")
            print(f"Downloaded {os.path.getsize(file_location)} bytes in {round((end-start), 2)} seconds at a speed of {round((os.path.getsize(file_location))/(end-start), 1)}b/s")
        else:
            print(f"This file already exists, having last been edited at {datetime.datetime.fromtimestamp(os.path.getmtime(file_location))}")
            answer=input("Would you like to overwrite the path[y/N]:  ")
            if answer.lower()=="y":
                shutil.rmtree(f"{path}/{name}")
                os.mkdir(f"data/{name}")
                url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name}"
                start=time.time()
                urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
                end=time.time()
                print(f"File saved to:  {location}")
                print(f"Downloaded {os.path.getsize(file_location)} bytes in {round((end-start), 2)} seconds at a speed of {round((os.path.getsize(file_location))/(end-start), 1)}b/s")
            elif answer.lower()=="r":
                pass
            else:
                print("Closing program")
                exit(0)
    else:
        os.mkdir(f"data/{name}")
        url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name}"
        start=time.time()
        urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
        end=time.time()
        print(f"File saved to:  {location}")
        print(f"Downloaded {os.path.getsize(file_location)} bytes in {round((end-start), 2)} seconds at a speed of {round((os.path.getsize(file_location))/(end-start), 1)}b/s")

    

def sift(data):
    file=open(file_location, "r")
    line_list=[]
    data_list=[]
    for (i, line) in enumerate(file):
        line_upper=line.upper()
        if data in line_upper and i not in [0, 1]:
            line_list.append(i)
    file.close()
    for x in line_list:
        data_list.append(open(file_location, "r").readlines()[x])
    return data_list

def save_addies(addies):
    file=open(f"{file_location}_refined", "w")
    for x in addies:
        file.write(x+"\n")
    file.close()
Flags.choose_flag(sys.argv) #Just the help flag really, cannot be bothered for such a stupid project anyways
check_dir()
if "-n" in sys.argv:
    name=sys.argv[(sys.argv.index("-n"))+1]
else:
    name=input("Please enter a name:  ")
if "-s" in sys.argv:
    refine_data=sys.argv[(sys.argv.index("-s"))+1]
else:
    refine_data=input("Data to filter by:  ")
download(name)
addies=sift(refine_data.upper())
save_addies(addies)
if "-p" in sys.argv:
    print()
    for x in addies:    print(x, end="")



