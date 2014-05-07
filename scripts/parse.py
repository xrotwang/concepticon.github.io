# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-05-06 13:03
# modified : 2014-05-06 13:03
"""
Parse the concepticon and convert it to different outputs.
"""

__author__="Johann-Mattis List"
__date__="2014-05-06"

from lingpy import *
import re

data = csv2list('Concepticon - WOLD.tsv')

head2line = dict(
        zip(
            [k.lower() for k in data[0]],
            range(len(data[0]))
            )
        )

output = {}
errors = open('errors.tsv', 'w')
bads = 0
good_lines = []
for line in data:

    link = line[7]
    idx = link.split('(')[-1][:-1]
    
    if ' ' in idx:
        idx = idx.split(' ')[0]
        print(idx)


    if ')' in idx:
        print(idx)
        idx = idx.replace(')','')

    try:
        idx = int(idx)
        # append stuff to important lines
        appends = []
        appends += [str(idx)] # omega-wiki link
        appends += [line[2]] # english raw gloss
        appends += [line[3]] # wold key
        appends += [line[5]] # part of speech
        good_lines += [appends]
    except:
        bads += 1
        errors.write('\t'.join(line)+'\n')
print(bads)
errors.close()

outf = open('concepticon.tsv','w')
comment = """# CONCEPTICON
# Created by: QLC Research Group (M. Cysouw, V. Kirchhoff, S. Nicolai, N.  Müller, J.-M. List [rearrange and modify this order, I put me as last person, since I didn't do quite much, not to indicate that I'm some kind of a leader in this project])
# Created on: {0}
# Contact: <whatemailtousehere?>

"""
outf.write(comment.format(rc('timestamp')))
outf.write('OMEGA_WIKI\tGLOSS\tWOLD\tPOS\n')
for line in good_lines:
    outf.write('\t'.join(line)+'\n')
outf.close()
