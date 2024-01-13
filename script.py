from urllib import request
from http.client import HTTPResponse
from time import sleep

import tarfile, sys, os

print("Fetching man pages...")

with request.urlopen("https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/man-pages-6.05.tar.xz") as response:
    print("Finished.")

    print("Reading fetched data...")
    
    file_data = HTTPResponse.read(response)
    file_name = input("Filename? ")
    file_name = file_name + ".tar.xz"

    print("Checking if file exists...")
    sleep(1)

    if os.path.exists(file_name):
        print("File already exists.")
        replace_file = input("Would you like to overwrite existing file? (y/Y): ")
    
        if replace_file == "y" or replace_file == "Y":
            new_file = open(file_name, "w+b")
        
            print("Overwriting file...")
            sleep(1)
            new_file.write(file_data)
        
            print("Done.")
            new_file.close()
        
        else:
            print("Aborting")
            sys.exit(1)
    else:
        with open(file_name, "w+b") as new_file:
            print("File does not exist. Writing data to file...")
            sleep(1)
            new_file.write(file_data)
        
            print("Done.")
    

    print("Extracting tar file...")
    sleep(1)

    with tarfile.open(file_name, "r:xz") as tar_file:
        tar_file.extractall()
    
        print("Finished.")

print("Checking if requirements are satisfied...")
sleep(1)

path = os.getenv("PATH")
operating_system = sys.platform

if path == None:
    print("Could not get $PATH, ensure that this script has correct permissions.")
    sys.exit(2)

#this is going to get removed seeing as how windows doesn't have man-pages
path_delimiters = {"win32": ";", "linux": ":"}

sub_directories = path.split(path_delimiters[operating_system])

requirements_satisfied = [{"make": False}, {"man": False}]
requirement = [list(item.keys()) for item in requirements_satisfied]
pos = 0

#Ew wtf have I done
for directory in sub_directories:
    if os.path.exists(directory + requirement[pos][pos]):
        print(f"Found {requirement[pos][pos]}. Proceeding...")
        requirements_satisfied[pos][requirement[pos][pos]] = True
        pos += 1
pos = 0

for item in requirements_satisfied:
    if item[requirement[pos][pos]] == False:
        print(f"Could not find {requirement[pos][pos]}, finding {requirement[pos][pos]} and installing...")
        sleep(1)
        
        if requirement[pos][pos] == "make":
            with request.urlopen("https://github.com/gcc-mirror/gcc") as response:
                response_data = HTTPResponse.read(response)
                print(response_data)
        elif requirement[pos][pos] == "man":
            with request.urlopen("https://man-db.nongnu.org/development.html") as response:
                response_data = HTTPResponse.read(response)
                print(response_data)
    pos += 1
    

        