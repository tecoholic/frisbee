#!/usr/bin/python

""" -----------------------------------------------------
        generate_pcode.py

script to generate player code for a input list of player
names

------------------------------------------------------"""

import sys

def generate_shortcode(filename):
    with open(filename, 'r') as fp:
        for line in fp:
            nospace = "".join(line.split())
            f = open("pcode.txt", 'a')
            f.write(",".join([nospace[:3].upper(), line]))
            f.close()




if __name__ == "__main__":
    try:
        generate_shortcode(sys.argv[1])
    except IndexError:
        print "Usage: ./generate_pcode.py <filename> \n"\
                "The file should contain players name as a list"\
                ". One name per line format"
