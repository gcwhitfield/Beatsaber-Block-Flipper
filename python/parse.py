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




# this is the list of block info. Each element in an even index has a corresponding
# inverse at the i + 1 index. From the block_info we can construct a python
# dictionary mapping blocks to their inverses easily
#
# this dictionary only contains red blocks. The _type variable controls the 
# color of a block. 0 = red, 1 = blue
block_info = [
    {'_time': 0, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 1},
    {'_time': 0.5, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 0},
    {'_time': 1, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 1},
    {'_time': 1.5, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 0},
    {'_time': 2, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 1},
    {'_time': 2.5, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 0},
    {'_time': 3, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 1},
    {'_time': 3.5, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 0},
    {'_time': 4, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 1},
    {'_time': 4.5, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 0},
    {'_time': 5, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 1},
    {'_time': 5.5, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 0},
    {'_time': 6, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 1},
    {'_time': 6.5, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 0},
    {'_time': 7, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 1},
    {'_time': 7.5, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 0},
    {'_time': 8, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 1},
    {'_time': 8.5, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 0},
    {'_time': 9, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 1},
    {'_time': 9.5, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 0},
    {'_time': 10, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 1},
    {'_time': 10.5, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 0},
    {'_time': 11, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 1},
    {'_time': 11.5, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 0},
    {'_time': 12, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 2},
    {'_time': 12.5, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 3},
    {'_time': 13, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 2},
    {'_time': 13.5, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 3},
    {'_time': 14, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 2},
    {'_time': 14.5, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 3},
    {'_time': 15, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 2},
    {'_time': 15.5, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 3},
    {'_time': 16, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 2},
    {'_time': 16.5, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 3},
    {'_time': 17, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 2},
    {'_time': 17.5, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 3},
    {'_time': 18, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 2},
    {'_time': 18.5, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 3},
    {'_time': 19.5, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 2},
    {'_time': 20, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 3},
    {'_time': 20.5, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 2},
    {'_time': 21, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 3},
    {'_time': 21.5, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 2},
    {'_time': 22, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 3},
    {'_time': 22.5, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 2},
    {'_time': 23, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 3},
    {'_time': 23.5, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 2},
    {'_time': 24, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 3},
    {'_time': 24.5, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 4},
    {'_time': 25, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 7},
    {'_time': 25.5, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 4},
    {'_time': 26, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 7},
    {'_time': 26.5, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 4},
    {'_time': 27, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 7},
    {'_time': 27.5, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 4},
    {'_time': 28, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 7},
    {'_time': 28.5, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 4},
    {'_time': 29, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 7},
    {'_time': 29.5, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 4},
    {'_time': 30, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 7},
    {'_time': 30.5, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 4},
    {'_time': 31, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 7},
    {'_time': 31.5, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 4},
    {'_time': 32, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 7},
    {'_time': 32.5, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 4},
    {'_time': 33, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 7},
    {'_time': 33.5, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 4},
    {'_time': 34, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 7},
    {'_time': 34.5, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 4},
    {'_time': 35, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 7},
    {'_time': 35.5, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 4},
    {'_time': 36, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 7},
    {'_time': 36.5, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 5},
    {'_time': 37, '_lineIndex': 0, '_lineLayer': 2, '_type': 0, '_cutDirection': 6},
    {'_time': 37.5, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 5},
    {'_time': 38, '_lineIndex': 0, '_lineLayer': 1, '_type': 0, '_cutDirection': 6},
    {'_time': 38.5, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 5},
    {'_time': 39, '_lineIndex': 0, '_lineLayer': 0, '_type': 0, '_cutDirection': 6},
    {'_time': 39.5, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 5},
    {'_time': 40, '_lineIndex': 1, '_lineLayer': 2, '_type': 0, '_cutDirection': 6},
    {'_time': 40.5, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 5},
    {'_time': 41, '_lineIndex': 1, '_lineLayer': 1, '_type': 0, '_cutDirection': 6},
    {'_time': 41.5, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 5},
    {'_time': 42, '_lineIndex': 1, '_lineLayer': 0, '_type': 0, '_cutDirection': 6},
    {'_time': 42.5, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 5},
    {'_time': 43, '_lineIndex': 2, '_lineLayer': 2, '_type': 0, '_cutDirection': 6},
    {'_time': 43.5, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 5},
    {'_time': 44, '_lineIndex': 2, '_lineLayer': 1, '_type': 0, '_cutDirection': 6},
    {'_time': 44.5, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 5},
    {'_time': 45, '_lineIndex': 2, '_lineLayer': 0, '_type': 0, '_cutDirection': 6},
    {'_time': 45.5, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 5},
    {'_time': 46, '_lineIndex': 3, '_lineLayer': 2, '_type': 0, '_cutDirection': 6},
    {'_time': 46.5, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 5},
    {'_time': 47, '_lineIndex': 3, '_lineLayer': 1, '_type': 0, '_cutDirection': 6},
    {'_time': 47.5, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 5},
    {'_time': 48, '_lineIndex': 3, '_lineLayer': 0, '_type': 0, '_cutDirection': 6}
]


# returns a new dicionary mapping blocks to their inverses
# inverse_dict_new()[block] = inverse_block
#
# the dictionary contains keys and values of the following format
# {_line_index, _lineLayer, _curDirection}
# these three varibles are the minimum amount of information needed to map blocks
# to their inverses
def inverse_dict_new():
    result = dict()
    for i in range(0, len(block_info), 2):
        # add blocks to their inverses
        curr_block_info = (
            block_info[i]['_lineIndex'],
            block_info[i]['_lineLayer'],
            block_info[i]['_cutDirection'],
        )
        inverse_block_info = (
            block_info[i + 1]['_lineIndex'],
            block_info[i + 1]['_lineLayer'],
            block_info[i + 1]['_cutDirection'],
        )
        result[curr_block_info] = inverse_block_info
        result[inverse_block_info] = curr_block_info
    return result

# prints the original dictionary from <sys.argv[1]> and our flipped dictionary
# <sys.argv[1]>-flipped.dat
def dbg_print_result():
    print("Here is the original vs flipped block...")
    with open(sys.argv[1]) as orig_json:
        orig = json.load(orig_json)
        with open(sys.argv[1].replace('.dat', '') + "-flipped.dat") as new_json:
            new = json.load(new_json)
            for i in range(len(orig['_notes'])):
                
                print("Original note: ", orig['_notes'][i])
                print("Flipped note: ", new['_notes'][i], "\n")

    


# 1) opens file given as second command line argument
# 2) create a dictionary that maps blocks to their inverses
# 3) reads the notes in file
# 4) map blocks to their inverse 
# 5) write result to new file called <sys.argv[1]>-flipped.dat
def doit():
    inv_dict = inverse_dict_new()
    with open(sys.argv[1]) as json_file:
        f = json.load(json_file)
        li = []
        flip_li = []
        for n in f['_notes']: # read the argument
            li.append(n)


        for i in range(len(li)): # loop over notes
            # find the inverse block
            block = li[i] # this is a dictionary
            info = (
                block['_lineIndex'],
                block['_lineLayer'],
                block['_cutDirection']
            )
            flipped_info = inv_dict[info] # tuple containing flipped info
            flipped_block = {
                "_time": block['_time'],
                "_lineIndex": flipped_info[0],
                "_lineLayer": flipped_info[1], 
                "_type": block['_type'], 
                "_cutDirectino": flipped_info[2]
            }
            f['_notes'][i] = flipped_block
            print("here is the flipped info", flipped_info)

        # write out to new file
        with open(sys.argv[1].replace('.dat', '') + "-flipped.dat", 'x') as newfile:
            json.dump(f, newfile)

        dbg_print_result()

def main():
    # this file should only be run with one argument (the song file name)
    # if we have more than one argument, print an  error
    if len(sys.argv) != 2:
        print("Cannot use more or less than two argument. The first argument \
should be 'parse.py' and the second one should be the file name.");
        return
    else:
        doit()
        
main()
