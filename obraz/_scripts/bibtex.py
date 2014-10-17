# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-29 18:25
# modified : 2014-10-04 08:40
"""
File takes bibtex entries from database and inserts them in files to publish on
the website.
"""

__author__="Johann-Mattis List"
__date__="2014-10-04"

from collections import defaultdict
from lingpyd import *
from glob import glob
import bibtexparser as btp
from bibtexparser.bparser import BibTexParser as BTP

class BibTex(object):
    
    def __init__(self, bfile, jfile="data/journals.csv"):
        
        if not bfile:
            fname = '/home/mattis/DropBox/evobib/basic.bib'

        with open(bfile) as f:
            bd = f.read()

        # try open journals file
        self._journals = dict([(a,b[0]) for a,*b in csv2list(jfile)])

        # customize stuff
        parser = BTP()
        parser.ignore_nonstandard_types = False
        bdb = btp.loads(bd, parser=parser)

        self._entries = bdb.entries

        # make entries to keys
        self._dict = {}
        crossrefs = []
        for entry in self._entries:
            self._dict[entry['id']] = defaultdict(str)
            for k in entry:
                if k != 'id':
                    self._dict[entry['id']][k] = entry[k]
            if 'crossref' in entry:
                crossrefs += [(entry['id'],entry['crossref'])]

        # resolve crossrefs
        for source,target in crossrefs:
            if source in self._dict and target in self._dict:
                for k in self._dict[target]:
                    if k not in self._dict[source]:
                        self._dict[source][k] = self._dict[target][k]
            else:
                print("[!] WARNING: target for <{0}> missing!".format(target))
        
        self._alias = dict(
                location = ['address'],
                year = ['date']
                )
        self._modifiers = {
            'paperconference' : 'Paper, presented at the conference',
            'paperworkshop': 'Paper, presented at the workshop',
            'talkconference': 'Talk, held at the conference',
            'talkworkshop': 'Talk, held at the workshop',
            'talkatm': 'Talk, held at the'
            }

        self._clean_keys()
        self._clean_entries()
        self._load_templates()
    
    def _load_templates(self, path='data/'):
        
        self._templates = {}
        paths = glob(path+'*.template')
        for p in paths:
            term = p.split('/')[-1].split('.')[0]
            with open(p) as f:
                self._templates[term] = {}
                for line in f:
                    if line.strip():
                        pre,post = line.strip().split('\t')
                        self._templates[term][pre] = post
        self._types = {}
        paths = glob(path+'*.types')
        for p in paths:
            term = p.split('/')[-1].split('.')[0]
            with open(p) as f:
                term = p.split('/')[-1].split('.')[0]
                with open(p) as f:
                    self._types[term] = {}
                    for line in f:
                        if line.strip():
                            pre,post = line[:-1].split('\t')
                            self._types[term][pre] = post

    def format(self, key, template='rst'):

        # get entry
        if key in self._dict:
            entry = self[key]
        else:
            return 'null'

        check = defaultdict(str)

        # get template 
        etype = entry['type']
        ctemp = self._templates[template]
        if etype in ctemp:
            # browser over template and change entry types
            tentry = defaultdict(str)
            for k,v in self._types[template].items():
                if k in self._types[template]:
                    tmp = self._types[template][k].format(**entry)
                    if tmp == self._types[template][k].format(**check):
                        tentry[k] = ''
                    else:
                        tentry[k] = tmp
                else:
                    tentry[k] = v

            return ctemp[etype].format(**tentry).replace('?.','?')
        
        return 'wrong type '+etype

    def _clean_keys(self):
        
        keys = list(self._dict.keys())
        for key in keys:
            if 'XXX' in key:
                if self[key]['type'] != 'customa':
                    del self._dict[key]
                else:
                    self._dict[key.replace('XXX','TALK')] = self[key]
                    del self._dict[key]

    def _clean_entries(self):

        for key in self._dict.keys():
            
            for k in self._dict[key]:
                self._dict[key][k] = ''.join([x for x in self._dict[key][k] if
                    x not in '{}'])
            
            entry = self._dict[key]
            
            # resolve aliases
            for alias,targets in self._alias.items():
                for target in targets:
                    if target in entry:
                        entry[alias] = entry[target]

            # check howpublished
            if entry['howpublished']:
                if entry['howpublished'] in self._modifiers:
                    entry['howpublished'] = self._modifiers[entry['howpublished']]

            # modify authorstuff
            entry['author'] = entry['author'].replace(' AND ',' and ')
            entry['editor'] = entry['editor'].replace(' AND ',' and ')
            
            # resolve journals
            if entry['journal']:
                try:
                    entry['journal'] = self._journals[entry['journal']]
                except KeyError:
                    pass

            if entry['pages']:
                entry['pages'] = entry['pages'].replace('--','-')

            # author
            if ' and ' in entry['author']:
                authors = entry['author'].split(' and ')
            elif entry['author']:
                authors = [entry['author']]
            else:
                authors = []
            
            for i,author in enumerate(authors):
                if entry['shortauthor']:
                    authors[i] = (author,author)
                elif ',' in author:
                    try:
                        last,first = author.split(', ')
                        first = '-'.join([l[0]+'.' for l in first.split('-')])
                        tmp = [l[0]+'.' for l in first.split(' ')]
                        if len(tmp) > 1:
                            first = ' '.join(first)
                        authors[i] = (first+' '+last,last+', '+first)

                    except ValueError:
                        print('[!] Error in field "author" ({0}) for key {1}.'.format(author, key))
                elif ' ' in author:
                    tmp = author.split(' ')
                    first = ' '.join(tmp[0:-1])
                    first = '-'.join([l[0]+'.' for l in first.split('-')])
                    first = ' '.join([l[0]+'.' for l in first.split(' ')])
                    
                    last = tmp[-1]
                    authors[i] = (first+' '+last,last+', '+first)
                else:
                    authors[i] = (author,'')

            if len(authors) > 2:
                entry['author_str'] = '{0}, {1}, and {2}'.format(
                        authors[0][1], #', '.join(authors[0][::-1], #authors[0][1] + ', ' + authors[0][0],
                        ', '.join([a for a,b in authors[1:-1]]),
                        authors[-1][0])# + ' '+authors[-1][1])
            elif len(authors) == 2: 
                entry['author_str'] = authors[0][1] #authors[0][1] + ', ' + authors[0][0]
                entry['author_str'] += ' and '+ authors[1][0] #authors[1][0] + ' '+ authors[1][1]
            elif authors:
                entry['author_str'] = authors[0][1] # + ', ' + authors[0][0]

            if len(authors) > 2:
                entry['author_short'] = authors[0][1] + ' et al.'
            else:
                entry['author_short'] = entry['author_str']
        
            # editor
            if ' and ' in entry['editor']:
                editors = entry['editor'].split(' and ')
            elif entry['editor']:
                editors = [entry['editor']]
            else:
                editors = []
            
            for i,editor in enumerate(editors):
                if entry['shorteditor']:
                    editors[i] = (editor,editor)
                elif ',' in editor:
                    try:
                        last,first = editor.split(', ')
                        first = '-'.join([l[0]+'.' for l in first.split('-')])
                        tmp = [l[0]+'.' for l in first.split(' ')]
                        if len(tmp) > 1:
                            first = ' '.join(first)
                        editors[i] = (first+' '+last,last+', '+first)

                    except ValueError:
                        print('[!] Error in field "editor" ({0}) for key {1}.'.format(editor, key))
                elif ' ' in editor:
                    tmp = editor.split(' ')
                    first = ' '.join(tmp[0:-1])
                    first = '-'.join([l[0]+'.' for l in first.split('-')])
                    first = ' '.join([l[0]+'.' for l in first.split(' ')])
                    
                    last = tmp[-1]
                    editors[i] = (first+' '+last,last+', '+first)
                else:
                    editors[i] = (editor,'')
            
            if len(editors) > 2:
                entry['editor_str'] = '{0}, {1}, and {2}'.format(
                        editors[0][1], #editors[0][1] + ', ' + editors[0][0],
                        ', '.join([a for a,b in editors[1:-1]]),
                        editors[-1][0]) # + ' '+editors[-1][1])
                entry['editor_suffix'] = 'eds.'
            elif len(editors) == 2: 
                entry['editor_str'] = editors[0][1]# + ', ' + editors[0][0]
                entry['editor_str'] += ' and '+ editors[1][0]# + ' '+ editors[1][1]
                entry['editor_suffix'] = 'eds.'
            elif editors:
                entry['editor_str'] = editors[0][1]# + ', ' + editors[0][0]
                entry['editor_suffix'] = 'ed.'


   
            # check eventdates
            if 'eventdate' in entry:
                
                try:
                    a,b = entry['eventdate'].split('/')
    
                    ya,ma,da = a.split('-')
                    yb,mb,db = b.split('-')
    
                    if ya == yb and ma == mb and da == db:
                        entry['eventdate'] = '/'.join([ya,ma,da])
                    elif ya == yb and ma == mb:
                        entry['eventdate'] = '/'.join([ya,ma,da+'-'+db])
                    elif ya == yb:
                        entry['eventdate'] = '/'.join([ya,ma,da+'-'+mb+'/'+ma])
                    else:
                        entry['eventdate'] = '/'.join([ya,ma,da+yb,mb,db])
                except:
                    entry['eventdate'] = entry['eventdate'].replace('-','/')

    def __iter__(self):
        
        return iter(self._dict.keys())

    def __getitem__(self, key):

        return self._dict[key]

    # cleaning function for bibtex entries
    def clean(entry):
        
        print(entry['id'])
        for k in entry:
            entry[k] = ''.join([x for x in entry[k] if x not in '{}'])
    
        if 'author' in entry:
            tmp = entry['author'].split(' and ')
            if len(tmp) == 2:
                entry['author'] = ' and '.join(tmp)
            elif len(tmp) >= 3:
                entry['author'] = '; '.join(tmp[0:-1]) + ' and '+tmp[-1]
            elif len(tmp) == 1:
                pass
    
        if 'editor' in entry:
            tmp = entry['editor'].split(' and ')
            if len(tmp) == 2:
                entry['editor'] = ' and '.join(tmp) + ' (eds)'
            elif len(tmp) >= 3:
                entry['editor'] = tmp[0] + ' et al. (eds)'
            elif len(tmp) == 1:
                entry['editor'] += ' (ed)'
    
        if 'title' in entry and 'subtitle' in entry:
            entry['title'] += '. '+entry['subtitle']
            entry['title'] = entry['title'].replace('?.','?')
    
        if 'userb' in entry and 'title' in entry: 
            entry['title'] = '<em>'+entry['title'] +'</em> ' + '<font style="font-weight:normal">'+entry['userb']+'</font>'
    
        if 'usera' in entry:
            entry['title'] += ' ['+entry['usera']+']'
        
        if '_doi' in entry:
            if not entry['_doi'].startswith('http'):
                entry['_doi'] = 'http://dx.doi.org/'+entry['_doi']
        
        if 'volume' in entry:
            if 'number' in entry:
                entry['volume'] = entry['volume']+'.'+entry['number'].strip()
                entry['volume'] = entry['volume'].strip()
    
        if 'address' in entry:
            entry['location'] = entry['address']+'.'
            
    
        if 'howpublished' in entry:
            
            if entry['howpublished'] == 'paperconference':
                entry['howpublished'] = 'Paper, presented at the conference'
            if entry['howpublished'] == 'paperworkshop':
                entry['howpublished'] = 'Paper, presented at the workshop'
            if entry['howpublished'] == 'talkconference':
                entry['howpublished'] = 'Talk, held at the conference'
            if entry['howpublished'] == 'talkworkshop':
                entry['howpublished'] = 'Talk, held at the workshop'
            if entry['howpublished'] == 'talkatm':
                entry['howpublished'] = 'Talk, held at the'
    
    
    
        if 'date' in entry and 'year' not in entry:
            entry['year'] = entry['date']
    
        if 'eventdate' in entry:
            
            try:
                a,b = entry['eventdate'].split('/')
    
                ya,ma,da = a.split('-')
                yb,mb,db = b.split('-')
    
                if ya == yb and ma == mb and da == db:
                    entry['eventdate'] = '/'.join([ya,ma,da])
                elif ya == yb and ma == mb:
                    entry['eventdate'] = '/'.join([ya,ma,da+'-'+db])
                elif ya == yb:
                    entry['eventdate'] = '/'.join([ya,ma,da+'-'+mb+'/'+ma])
                else:
                    entry['eventdate'] = '/'.join([ya,ma,da+yb,mb,db])
            except:
                entry['eventdate'] = entry['eventdate'].replace('-','/')
    
        return entry
    
    def _prepare(self):

        # resolve all crossrefs
        for key,entry in entries.items():
            if 'crossref' in entry:
                try:
                    father = entries[entry['crossref']]
                    for k in father:
                        if k not in entry:
                            entry[k] = father[k]
                except KeyError:
                    print('[!] {0} failed for crossref {1}.'.format(key,entry['crossref']))


