#!D:\Surya\copy-clipboard\venv\Scripts\python.exe

from sys import argv
import pyperclip
# from pathlib import Path
import os
import base64
import json
import pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

FILE = "store"
PASSWORD = b"This"
SALT = b'3\x97\x16\x1b\x8e\x92\xef\xaf\x06\xaeT\xdcL\xad\xe4\x11'

class Crypt:
    def __init__(self):
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=100000,
            backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(PASSWORD))
        self.f = Fernet(self.key)

    def encrypt(self, data):
        encrypted_data = self.f.encrypt(bytes(data,'utf-8'))
        print(encrypted_data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        return self.f.decrypt(encrypted_data)


def addCred():
    if not os.path.isfile(FILE):
        print("file not exists")
        print("Please enter the host name, password separated by space and type DONE at last:")
        cred_obj = {}
        while True:
            input_value = input()
            #TODO: input validation
            if input_value.upper() == "DONE":
                break
            else:
                input_host = input_value.split()
                if len(input_host) != 2:
                    print("Invalid input. exit the program")
                    quit()
                cred_obj[input_host[0]] = Crypt.encrypt(input_host[1])

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
                data[input_host[0]] = Crypt.encrypt(input_host[1])

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
                pyperclip.copy(Crypt.decrypt(result).decode('UTF-8'))
                print("Password copied to clipboard")

if __name__ == '__main__':

    #initialise class
    crypting = Crypt()
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
