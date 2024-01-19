from urllib import request
from http.client import HTTPResponse
from time import sleep
from zipfile import ZipFile

import tarfile, sys, os

def write_and_extract(name, response):
    if ".zip" in name:
        print("Writing to disk and extracting...")
        new_file = open(name, "w+b")
        new_file.write(response)
                
        new_file.close()
                
        zipped_file = ZipFile(name)
        zipped_file.extractall(".")
        zipped_file.close()
                
        print("Done.")
    elif ".tar.xz" in name:
        print("Writing to disk and extracting...")
        
        new_file = open(name, "w+b")
        new_file.write(response)
        
        new_file.close()
        
        tar_file = tarfile.open(name, "r:xz")
        tar_file.extractall(".")
        tar_file.close()
        
        print("Done.")
    else:
        print("File format not supported.")
    
print("Fetching man pages...")

with request.urlopen("https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/man-pages-6.05.tar.xz") as response:
    
    file_data = HTTPResponse.read(response)
    print("Done.")
    
    write_and_extract("man-pages.tar.xz", file_data)

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

#Stripping key out of inner lists
for i in range(0, len(requirement)):
    requirement[i] = "".join(requirement[i])

pos = 0

#Fixed it
for directory in sub_directories:
    if os.path.exists(directory + requirement[pos]):
        print(f"Found {requirement[pos]}. Proceeding...")
        requirements_satisfied[pos][requirement[pos]] = True
        pos += 1
pos = 0

for item in requirements_satisfied:
    if item[requirement[pos]] == False:
        print(f"Could not find {requirement[pos]}, finding {requirement[pos]} and installing...")
        sleep(1)
        
        if requirement[pos] == "make":
            print("Downloading make...")
            with request.urlopen("https://github.com/gcc-mirror/gcc/archive/master.zip") as response:
                response_data = HTTPResponse.read(response)
                write_and_extract("gcc.zip", response_data)
                
        elif requirement[pos] == "man":
            print("Downloading man-db...")
            with request.urlopen("https://gitlab.com/man-db/man-db/-/archive/main/man-db-main.zip") as response:
                response_data = HTTPResponse.read(response)
                write_and_extract("man-db.zip", response_data)
    pos += 1
    

        