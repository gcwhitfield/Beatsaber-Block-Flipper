import json
import sys
import os
import string

'''
Thursday, March 26, 2020
Author: George Whitfield - gwhitfie@andrew.cmu.edu
Brief: Flip the cut direction of blocks in beat saber song files

How to use this file

Run "python3 parse.py {song name}"
    Note: You do not need to put the absolute path to the song file. Just put
    name of song file. The code will get the songs from ModLauncher/SongFiles/
'''



def flip(name):
    # print(f"Parsing {name}")
    print(os.getcwd())
    with open(name) as json_file:
        f = json.load(json_file)
        for e in f['_events']:
            print(e)


def main():
    # this file should only be run with one argument (the song file name)
    # if we have more than one argument, print an  error
    if len(sys.argv) != 2:
        print("Cannot use more or less than two argument. The first argument \
should be 'parse.py' and the second one should be the file name.");
        return
    else:
        flip(sys.argv[1])
        return

main()
