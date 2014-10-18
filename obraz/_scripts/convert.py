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
    """
    Convert data to json structures.
    """
    txtname,*post = path.split('/')[-1].replace('.tsv','').split('_')
    if post:
        txtname += '_'+'-'.join(post)
        
    data = csv2list(path)
    d = {}
    
    # get header
    header = data[0]

    # get owid 
    owidx = header.index('OMEGAWIKI')
    for line in data[1:]:
        owid = line[owidx]
        if owid not in d:
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

def check_multilinks(path):
    """
    Get multiple links in the data and store them in a separate array.
    """

    txtname,*post = path.split('/')[-1].replace('.tsv','').split('_')
    if post:
        txtname += '_'+'-'.join(post)
        
    data = csv2list(path)
    header = data[0]

    owidx = header.index('OMEGAWIKI')
    if not 'GLOSS' in header:
        if 'ENGLISH' in header:
            gidx = header.index('ENGLISH')
        else:
            raise ValueError("index for gloss not found in data")
    else:
        gidx = header.index("GLOSS")

    g = {}
    for line in data[1:]:
        try:
            g[line[gidx]] += [line[owidx]]
        except KeyError:
            g[line[gidx]] = [line[owidx]]

    multg = dict([(k,v) for k,v in g.items() if len(v) > 1])
    g = {}
    for line in data[1:]:
        try:
            g[line[owidx]] += [line[gidx]]
        except KeyError:
            g[line[owidx]] = [line[gidx]]

    multo = dict([(k,v) for k,v in g.items() if len(v) > 1])

    txtA = '  "' + txtname + '" : ' + json.dumps(multg)
    txtB = '  "' + txtname + '" : ' + json.dumps(multo)

    return txtname,txtA,txtB



txt,maintxt = data2object('../concepticon.tsv')
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
maintxt += '};\n'
maintxtA = 'var MULTIGLOSS = {\n'
maintxtB = 'var MULTIKEY = {\n'
for i,f in enumerate(files):
    #try:
        print(f)
        txt,txtA,txtB = check_multilinks(f)
        maintxtA += txtA
        maintxtB += txtB
        if i != len(files) -1:
            maintxtA += ',\n'
            maintxtB += ',\n'
        else:
            maintxtA += '\n'
            maintxtB += '\n'
    #except:
    #    print(f)
maintxt += maintxtA + '};\n'
maintxt += maintxtB + '};\n'

with open('../media/concepticon.js', 'w') as f:
    f.write(maintxt)
    f.write('var main_list = '+json.dumps(sorted(clists))+';')


# create the meta list from concepticon for our search
conc = csv2list('../concepticon.tsv')
D = {}
out = [[conc[0][0]]+['FGLOSS']+conc[0][1:]]
for line in conc[1:]:
    glosses = line[2].lower().split(' ')
    for gloss in glosses:
        gloss = ''.join([g for g in gloss if g in
            'abcdefghijklmnopqrstuvwxyz'])
        if gloss:
            out += [[line[0]] + [gloss] + line[1:]]
with open('../concepticonS.tsv', 'w') as f:
    for line in out:
        f.write('\t'.join(line)+'\n')


