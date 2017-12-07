from sys import argv
# import argparse 


if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == "new":
            print("new")
        else:
            print("wrong arguments")
    else:
        print("not new")
