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
        
        if line[7].strip():
            print(line[0],line[7])
            alts = [p.strip().split('(')[-1][:-1] for p in line[7].strip().split(',')]
            alts = ';'.join([a for a in alts if a.isdigit()])
            if alts:
                appends += [alts]
            else:
                appends += ['-']
        else:
            appends += ['-']

        appends += [line[2].upper()] # english raw gloss
        appends += [line[5]] # part of speech

        appends += [line[3] if not line[3].startswith('0') else '-'] # wold key


        good_lines += [appends]
    except:
        bads += 1
        errors.write('\t'.join(line)+'\n')
print(bads)
errors.close()

outf = open('concepticon.tsv','w')
comment = """# CONCEPTICON
# Created by: QLC Research Group
# Created on: {0}

"""
outf.write(comment.format(rc('timestamp')))
outf.write('OMEGAWIKI\tSEEALSO\tGLOSS\tPOS\tWOLD\n')
for line in sorted(good_lines, key=lambda x:x[2]):
    outf.write('\t'.join(line)+'\n')
outf.close()
