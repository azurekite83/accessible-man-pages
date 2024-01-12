from urllib import request
from http.client import HTTPResponse
import tarfile

print("Fetching man pages...")
response = request.urlopen("https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/man-pages-6.05.tar.xz")

file_data = HTTPResponse.read(response)

    
with open("file.tar.xz", "w+b") as new_file:
    new_file.write(file_data)
        
    print("Finished.")
    

print("Inspecting")
with tarfile.open("file.tar.xz", "r:xz") as tar_file:
    file_list = tar_file.getnames()
    
    print(file_list)