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
        
        if line[11].strip():
            print(line[0],line[7])
            alts = [p.strip().split('(')[-1][:-1] for p in line[11].strip().split(',')]
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
doublets = open('doublets.tsv','w')
visited = {}
outf.write(comment.format(rc('timestamp')))
outf.write('OMEGAWIKI\tSEEALSO\tGLOSS\tALIAS\tDEFINITION\tPOS\tWOLD\n')
sorter = []
for line in sorted(good_lines, key=lambda x:x[2]):
    if line[0] not in visited:
        visited[line[0]] = [line[1:]]
        #outf.write('\t'.join(line)+'\n')
        sorter += [line[0]]
    else:
        visited[line[0]] += [line[1:]]


#outf.close()
d = 0
for key in visited:
    if len(visited[key]) > 1:
        d += 1
        for line in visited[key]:
            doublets.write(key+'\t'+'\t'.join(line)+'\n')
        doublets.write('#\n')
doublets.close()


def isfloat(var):
    try:
        float(var)
        return True
    except:
        return False

from urllib.request import urlopen

for key in sorter:

    # get the definition first
    response = urlopen(
            'http://www.omegawiki.org/api.php?format=xml&action=ow_define&dm={0}'.format(
                key
                )
            )
    xml = response.read()
    xml = str(xml)
    
    # extract defition 
    definition = re.findall('text="(.*?)"', xml)
    if definition:
        definition = definition[0].replace('\t',' ')
    else:
        definition = '-'
    print(definition)

    # get the 
    if len(visited[key]) == 1:
        outf.write(key+'\t'+visited[key][0][0]+'\t'+visited[key][0][1]+'\t-\t'+definition+'\t'+'\t'.join(visited[key][0][2:])+'\n')
    else:
        # get multiple glosses and wold keys
        wolds = []
        glosses = []
        for line in visited[key]:
            wolds += [line[-1]]
            glosses += [line[1]]

        wolds = [w for w in sorted(set(wolds)) if isfloat(w)]
        glosses = [g for g in sorted(set(glosses)) if g != visited[key][0][1]]
        if glosses:
            pass
        else:
            glosses = ['-']

        outf.write(key+'\t'+visited[key][0][0]+'\t'+visited[key][0][1]+'\t'+'; '.join(glosses)+'\t'+definition+'\t'+'\t'+visited[key][0][2]+'\t'+';'.join(wolds)+'\n')
outf.close()

import os
os.system('cp concepticon.tsv ~/')
