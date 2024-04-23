#!/bin/python3
# September 03, 2022
# Copyright (C) 2022 Joseph Rohani
# https://github.com/britishperson10/dmassassins
# Just realised that this shit might not work on Windows due to the goofy ass file system, also I know, excessive lib use
# Synopsis:  Files are saved to .data folder under the name, then refined are saved to name_reined
import sys, urllib.request, os, shutil, time, datetime
global DEBUG, VERSION, DOMAIN
VERSION=1.1
FLAGS=["-d", "-s", "-p", "-o", "-O", "-h", "-r", "--help", "-n", "-c", "-R", "-A", "-N"]
for x in sys.argv:
    if x.startswith("-") and not x in FLAGS:
        print(f"\"{x}\" is an unrecognised flag")
        exit(1)
if "-d" in sys.argv:
    DEBUG=True
else:
    DEBUG=False
if DEBUG:
    DOMAIN="0.0.0.0"
else:
    DOMAIN="josephrohani.ch"
if "-R" in sys.argv:
    if DEBUG:
        try: shutil.rmtree(".data")
        except FileNotFoundError: print("Path didn't even exist")
    elif input("Delete all data[y/N]:  ").lower()=="y": 
        try: shutil.rmtree(".data")
        except FileNotFoundError: print("Path didn't even exist")
    else: print("Not deleted")
    exit(0)

class Flags:
    def choose_flag(argv):
        # l=0
        for x in argv:
            if x=="-h" or x=="--help":
                print("--HELP PAGE--\nFlags:\n\t-h or --help:  This output\n\t-n: Specifiy target name\n\t-d:  Enable weird debug stuff that might be removed by the time I release this\n\t-s: The refined search data\n\t-o: Specify data output location, wouldn't recommend using this\n\t-r: if file exists, reuse it, can put \"r\" into the yes no prompt for same result\n\t-O: Overwrite existing file\n\t-p: Print the output data to the terminal\n\t-c: Will open the address in either google maps or openstreetmap, defaulting to openstreetmap, with openstreetmaps as \"-c osm\" and google maps as\"-c gm\" and Google Eart as \"-c ge\"\n\t-R: Remove the .data folder\n\t-A: Don't send analytics data\n\t-N: Omit name from analytics data\n\nMade by Joseph Rohani")
                exit(0)

def analytics(name): #Want to see how far this spreads, also funny for maybe selling data back to people
    if "-A" not in sys.argv:
        import socket, platform
        try:
            if "-N" not in sys.argv:
                dev_info=f" | {platform.platform()} | {name} | {os.getcwd()} | {os.getlogin()} | {VERSION} | {datetime.datetime.fromtimestamp(time.time())}::{time.tzname}--dmassassins"
            else:
                dev_info=f" | {platform.platform()} | __omitted__ | {os.getcwd()} | {os.getlogin()} | {VERSION} | {datetime.datetime.fromtimestamp(time.time())}::{time.tzname}--dmassassins"

            s=socket.socket()
            s.connect((DOMAIN,5001))
            s.send(dev_info.encode())
            s.close()
        except socket.gaierror:
            print("A")
        except ConnectionRefusedError:
            print("B")
        except:
            print("Z")
    else:
        print("Not sending analytics")
def check_dir(path=".data"):
    if not os.path.exists((path+"/")):
        os.mkdir(path)

def download(name, ow=False, path=".data"):
    global file_location, locationname
    name=name.lower()
    location=os.path.dirname(os.path.realpath(__file__))+"/.data/"+name+"/"
    file_location=location+name
    if os.path.exists(location):
        if DEBUG or "-r" in sys.argv:  pass
        elif "-O" in sys.argv:
            shutil.rmtree(f"{path}/{name}")
            os.mkdir(f".data/{name}")
            name_space=name.replace(" ", "%20")
            url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name_space}"
            start=time.time()
            urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
            end=time.time()
            print(f"File saved to:  {location} from {url}")
            print(f"Downloaded {os.path.getsize(file_location)} bytes in {round((end-start), 2)} seconds at a speed of {round((os.path.getsize(file_location))/(end-start), 1)}b/s")
        else:
            print(f"This file already exists, having last been edited at {datetime.datetime.fromtimestamp(os.path.getmtime(file_location))}")
            answer=input("Would you like to overwrite the path[y/N]:  ")
            if answer.lower()=="y":
                shutil.rmtree(f"{path}/{name}")
                name_space=name.replace(" ", "%20")
                os.mkdir(f".data/{name}")
                url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name_space}"
                start=time.time()
                urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
                end=time.time()
                print(f"File saved to:  {location} from {url}")
                print(f"Downloaded {os.path.getsize(file_location)} bytes in {round((end-start), 2)} seconds at a speed of {round((os.path.getsize(file_location))/(end-start), 1)}b/s")
            elif answer.lower()=="r":
                pass
            else:
                print("Closing program")
                exit(0)
    else:
        os.mkdir(f".data/{name}")
        name_space=name.replace(" ", "%20")
        url=f"https://mcassessor.maricopa.gov/mcs/export/property/?q={name_space}"
        start=time.time()
        urllib.request.urlretrieve(url, f"{path}/{name}/{name}")
        end=time.time()
        print(f"File saved to:  {location} from {url}")
        print(f"Downloaded {os.path.getsize(file_location)} bytes in {round((end-start), 2)} seconds at a speed of {round((os.path.getsize(file_location))/(end-start), 1)}b/s")

def sift(data_array):
    
    line_list=[]
    data_list=[]
    for data in data_array:
        file=open(file_location, "r")
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
    try:
        refine_temp=sys.argv[(sys.argv.index("-s"))+1]
        no_flag=False
    except IndexError:
        # The -s flag is empty and also at the end of the file
        no_flag=True
    if refine_temp.startswith("-"):
        if input(f"If you would like to filter with the term\"{refine_temp}\", enter \"y\":  ").lower()=="y":
            pass
        else:
            print("Please ensure that you enter an argument after the flag or a trailing flag might be interpreted as an argument")
            exit(1)
    elif no_flag or len(refine_temp)<1:
        print("Please provide a value for the flag \"-s\"")
        exit(1)
    else: no_flag=False
    refine_data=refine_temp.upper().strip(" ").split(",")
else:
    if not DEBUG:
        refine_temp=input("Data to filter by:  ")
    else:
        refine_temp=" "
if len(refine_temp)<1:
    refine_data=" "
refine_data=refine_temp.upper().strip(" ").split(",")
analytics(name) #Can be disabled with "-A" flag, mostly just to see how far this spreads
download(name)
addies=sift(refine_data)
save_addies(addies)
if "-p" in sys.argv or DEBUG:
    print("Raw Data:")
    for x in addies:    print(f"\t{x}", end="")
    print()
if "-c" in sys.argv:
    try:
        map_arg=sys.argv[(sys.argv.index("-c"))+1]
        no_flag=False
    except IndexError:
        # The -c flag is empy and also at the end of the file
        no_flag=True
    if no_flag or len(map_arg)<1 or map_arg.startswith("-"):
        map_arg="osm"
    else: no_flag=False
    if map_arg=="gm" or map_arg=="gsm": #doing this becuase when testing I always did gsm fo r some reason and it caused me many headaches
        wb="https://www.google.com/maps/place/"
        wb_name="Google Maps"
    elif map_arg=="ge":
        wb="https://earth.google.com/web/search/"
        wb_name="Google Earth"
    else:
        wb="https://www.openstreetmap.org/search?query="
        wb_name="Open Street Maps"
    import webbrowser
    addresses=[]
    for line in addies:
        address=""
        x=0
        for char in line:
            if x>1 and x<5:
                address=address+char
            if char==",":
                x+=1
        addresses.append(address[0: -1]) #append the address without the trailing comma because 
    choosing=True
    if len(addresses)<1:
        print("There were no results after filtering")
        exit(0)
    print(f"Opening in: {wb_name}")
    # Next few lines are from when I wasmessing around with termux(No installed webbrowser) and nothing happened so in that case I'm gonna just print the URL to use.
    try:
        webbrowser.get()
        wb_exists=True
    except webbrowser.Error:
        wb_exists=False
    while choosing:
        i=0
        for addy in addresses:
            i+=1
            print(f"{i} : {addy}")
        choice=input("Choose the address to open or enter (0) to quit\n")
        try:
            int(choice)
        except ValueError:
            if len(choice)<1 or choice=="q":
                exit(0)
            print("\033[1;37;41mMan just choose an actual option\033[0m")
            exit(69420)
        if int(choice)==0 or choice =="q":
            choosing=False
        else:
            choice_real=int(choice)-1
            try:
                if wb_exists:
                    webbrowser.open(f"{wb}{addresses[choice_real]}")
                else:
                    print(f"Please open the URL:  \"{wb}{addresses[choice_real]}\" in a browser")
            except IndexError:
                print("\033[1;37;41mCHOOSE AN ACTUAL OPTION\033[0m")

