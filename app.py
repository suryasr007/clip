#Enter the interpretor path of python.exe if using virtual env

from sys import argv
import pyperclip
import os
import base64
import json

#file where the data is stored (current location: application root)
FILE = "store"

#encodes the the data to base64
def encoded(data):
    encoded_data = base64.b64encode(bytes(data, 'utf-8'))
    return encoded_data.decode()

#decodes the encoded data 
def decoded(encoded_data):
    decoded_data = base64.b64decode(encoded_data)
    return decoded_data.decode()

# Function to add the credentials 
#format:
#   server1 password1
#   server2 password2
def addCred():
    # If the FILE doesn't exists
    # creates the file and dump data. 
    if not os.path.isfile(FILE):
        print("file not exists")
        print("Please enter the host name, password separated by space and type DONE at last:")
        cred_obj = {}
        while True:
            input_value = input()
            if input_value.upper() == "DONE":
                break
            else:
                credentials = input_value.split()
                if len(credentials) < 2:
                    print("Invalid Input exiting the program")
                    break
                else:
                    servername = " ".join(credentials[:(len(credentials)-1)])
                    password = encoded(credentials[-1])
                    cred_obj[servername] = password

        with open(FILE,'w') as f:
            f.write(json.dumps(cred_obj))
        print("Added credential successfully")
        
    else:
        # If FILE exists and data exists
        # Retrieve data and append new data and push the object
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
                credentials = input_value.split()
                if len(credentials) < 2:
                    print("Invalid Input exiting the program")
                    break
                else:
                    servername = " ".join(credentials[:(len(credentials)-1)])
                    password = encoded(credentials[-1])
                    data[servername] = password

        with open(FILE,'w') as f:
            f.write(json.dumps(data))
        print("Added credential successfully")

def getCred():
    # List the list of servers whose credentials are available.
    # Entered server details are copied to clipboard 
    if not os.path.isfile(FILE):
        print("It seems file doesn't exist. Please start program using 'new' argument and add a credential.")
    else:
        with open(FILE,'r') as f:
            data = f.read()

        if not data:
            print("It seems there are no credentials. Please add credentials and run the program")

        else:
            data_dict = json.loads(data)
            print("\nPasswords of below servers are available")
            print("-------"*3)            
            print(*[k for k in data_dict.keys()], sep='\n')
            print("-------"*3)
            name = input("please enter the server for which you want the password:")

            if name not in data_dict.keys():
                print("\n======="*3)
                print("The password of is not available for the entered server")
                print("======="*3)
                
            else:
                #copy to clipboard.
                result = data_dict[name]
                pyperclip.copy(decoded(result))
                print("Password copied to clipboard")

if __name__ == '__main__':
    # If the argument is 'new' add the credentials 
    if len(argv) > 1:
        if argv[1] == "new":
            addCred()
        else:
            print("wrong arguments")
    else:
        getCred()
        while True:
            print("\npress 'q' to quit or 'enter' to copy password again")
            if input() == 'q':
                quit()
            getCred()
