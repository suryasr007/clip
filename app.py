#!D:\Surya\copy-clipboard\venv\Scripts\python.exe

from sys import argv
import pyperclip
import os
import base64
import json


FILE = "store"

def encoded(data):
    encoded_data = base64.b64encode(bytes(data, 'utf-8'))
    print(encoded_data.decode())
    return encoded_data.decode()

def decoded(encoded_data):
    decoded_data = base64.b64decode(encoded_data)
    print(decoded_data.decode())
    return decoded_data.decode()


def addCred():
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
                if len(input_host) != 2:
                    print("Invalid input. exit the program")
                    quit()
                cred_obj[input_host[0]] = encoded(input_host[1])

        with open(FILE,'w') as f:
            f.write(json.dumps(cred_obj))
        
        print("Added credential successfully")
        
    else:
        print("file exists")
        with open(FILE,'r') as f:
            data = f.read()

        if not data:
            data = {}
            with open(FILE,'w') as f:
                f.write(json.dumps(data)) 
        data = json.loads(data)
        print("Please enter the host name, password separated by space and type DONE at last:")
        while True:
            input_value = input()
            if input_value.upper() == "DONE":
                break
            else:
                input_host = input_value.split()
                if len(input_host) != 2:
                    print("Invalid input. exit the program")
                    quit()
                data[input_host[0]] = encoded(input_host[1])

        with open(FILE,'w') as f:
            f.write(json.dumps(data))
        print("Added credential successfully")

def getCred():
    if not os.path.isfile(FILE):
        print("It seems file doesn't exist. Please start program using 'new' argument add a credential.")
    else:
        with open(FILE,'r') as f:
            data = f.read()

        if not data:
            print("It seems there are no credentials. Please add \
                credentials and run the program")
        else:
            data_dict = json.loads(data)
            print("\nAvailable credentials")
            print("-------"*3)            
            print(*[k for k in data_dict.keys()], sep='\n')
            print("-------"*3)
            name = input("please enter the server for which you want the password:")

            if name not in data_dict.keys():
                print("\n======="*3)
                print("The password of entered key is not available")
                print("======="*3)
                
            else:
                #copy to clipboard.
                result = data_dict[name]
                pyperclip.copy(decoded(result))
                print("Password copied to clipboard")

if __name__ == '__main__':

    if len(argv) > 1:
        if argv[1] == "new":
            addCred()
        else:
            print("wrong arguments")
    else:
        getCred()
        while True:
            print("\npress 'q' to quit or enter to continue")
            if input() == 'q':
                quit()
            getCred()
