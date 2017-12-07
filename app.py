#!D:\Surya\copy-clipboard\venv\Scripts\python.exe

from sys import argv
from pathlib import Path
import os
import json

FILE = os.getcwd()+"\\newfile"
print(FILE)

def addCred():
    #Check weather the file exists or create new
    # with open('newfile','a') as f:
    #     f.write("second line")
    # Take input(key)
    # Take input(value)
    # encrypt the value
    # store the key value pair in file
    if not os.path.isfile(FILE):
        print("file not exists")
        print("Please enter the host name, password separated by space and type DONE at last:")
        cred_obj = {}
        while True:
            input_value = input()
            if input_value.upper() == "DONE":
                break
            else:
                input_host = input_value.split()
                cred_obj[input_host[0]] = input_host[1]
        
        print(cred_obj)
        with open(FILE,'w') as f:
            f.write(json.dumps(cred_obj))
    else:
        print("file exists")
        with open(FILE,'r') as f:
            data = f.read()
        print(json.loads(data))

def getCred():
    pass

if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == "new":
            addCred()
        else:
            print("wrong arguments")
    else:
        print("not new")
