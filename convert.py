# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-08 09:07
# modified : 2014-10-08 09:07
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2014-10-08"

from lingpyd import *
from glob import glob
import json

def data2object(path):
    txtname = path.split('/')[-1].replace('.tsv','').split('_')[0]
    data = csv2list(path)
    d = {}
    
    # get header
    header = data[0]

    # get owid 
    owidx = header.index('OMEGAWIKI')
    for line in data[1:]:
        owid = line[owidx]
        d[owid] = {}
        for i,cell in enumerate(line):
            if i != owidx:
                head = header[i]
                
                try:
                    d[owid][head] += [cell]
                except KeyError:
                    d[owid][head] = [cell]

    txt = 'var ' + txtname + ' = ' + json.dumps(d)+';\n'
    return txtname,txt

def data2json(path):
    txtname = path.split('/')[-1].replace('.tsv','').split('_')[0]
    data = csv2list(path)
    d = {}
    
    # get header
    header = data[0]

    # get owid 
    owidx = header.index('OMEGAWIKI')
    for line in data[1:]:
        owid = line[owidx]
        d[owid] = {}
        for i,cell in enumerate(line):
            if i != owidx:
                head = header[i]
                
                try:
                    d[owid][head] += [cell]
                except KeyError:
                    d[owid][head] = [cell]
    if not 'GLOSS' in header:
        if 'ENGLISH' in header:
            eidx = header.index('ENGLISH')
            for k in d:
                d[k]['GLOSS'] = d[k]['ENGLISH']

    txt = '  "' + txtname + '" : ' + json.dumps(d)+''
    return txtname,txt

txt,maintxt = data2object('concepticon.tsv')
files = glob('data/conceptlists/*.tsv')
clists = []
maintxt += 'var CNC = {\n'
for i,f in enumerate(files):
    try:
        txt,ftxt = data2json(f)
        maintxt += ftxt
        clists += [txt]
        if i != len(files)-1:
            maintxt += ',\n'
        else:
            maintxt += '\n'
    except:
        print(f)
maintxt += '};\n';

with open('javascripts/concepticon.js', 'w') as f:
    f.write(maintxt)
    f.write('var main_list = '+json.dumps(clists)+';')
    

