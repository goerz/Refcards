#!/usr/bin/python
""" Replace characters in ascii.tex with the data from latin1_symbols.txt 

    If you were to change the information in the latin1_symbols.txt to
    something that is appropriate to another codepage, you could very easily
    create an ascii table for that codepage just by running this program.

    This program will save its result in ascii_out.tex
"""

import re

ascii_file = "ascii.tex"
char_file = "latin1_symbols.txt"

ascii_fh = open(ascii_file)
out_fh = open("ascii_out.tex", "w")
char_fh = open(char_file)

chars = {} # dict for code point -> latex expression

char_line_pattern = re.compile(r'^([0-9]{1,})\s+(\S.*)$')
ascii_line_pattern = re.compile(
     r'^\s*([0-9]{1,})\\textit\{d\}.*(&\s*\S.*\\\\)\s*$')
    # e.g.
    #128\textit{d} & 80\textit{h} & ~ & x \\

# build chars data structure
for (i, line) in enumerate(char_fh):
    cl_match = char_line_pattern.match(line)
    if cl_match:
        chars[cl_match.group(1)] = cl_match.group(2)
    else:
        print("Can't understand line %i in char file" % i)

# go through ascii.tex and insert data
for (i, line) in enumerate(ascii_fh):
    al_match = ascii_line_pattern.match(line)
    if al_match:
        try:
            replacement = "& %s \\\\" % chars[al_match.group(1)]
            line=line.replace(al_match.group(2), replacement)
            print("Made replacement of '%s' with '%s' in line %i" 
                  % (al_match.group(2), replacement, i ) )
        except KeyError:
            print("No replacement found in line %i" % i)
    else:
        print("Left line %i unchanged" % i)
    out_fh.write(line)

ascii_fh.close()
out_fh.close()
char_fh.close()
