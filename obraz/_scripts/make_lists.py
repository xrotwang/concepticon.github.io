# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-17 09:51
# modified : 2014-10-17 09:51
"""
Make documentatin from bibtex file for all Swadesh lists in the sample.
"""

__author__="Johann-Mattis List"
__date__="2014-10-17"


from bibtex import *
import markdown
import json

md = markdown.Markdown()

bib = BibTex('references.bib')

for b in bib:
    if bib[b]['eprint'] and not bib[b]['url']:
        bib[b]['url'] = bib[b]['eprint']


        
clists = [b for b in bib if bib[b]['type'] == 'conceptlist']

ref2idf = {}
for k in clists:
    crefs = [c.strip() for c in bib[k]['entryset'].split(',')]
    for cref in crefs:
        bib[k]['reference'] += '<p class="reference">'
        bib[k]['reference'] += bib.format(cref, template='html')
        bib[k]['reference'] += ' <sup><a class="evobib" href="http://bibliography.lingpy.org?key='+cref+'" target="_blank">REF</a></sup></p>'
    
    # make identifier
    if not bib[k]['shortauthor']:
        idf = bib[k]['author_str'].split(',')[0].strip()
    else:
        idf = bib[k]['shortauthor']

    if bib[k]['note']:
        if '@' in bib[k]['note']:
            bib[k]['note'] = bib[k]['note'].replace('@','lists.html?conceptlist=')

        bib[k]['note'] = md.convert(bib[k]['note'])

    
    idf += '-' + bib[k]['year']
    idf += '-' + bib[k]['items']
    idf += bib[k]['list_suffix']
    
    bib[k]['identifier'] = idf
    bib[k]['source_url'] = k
    ref2idf[k] = idf
    
out = ''
with open('../list_include.md') as f:
    out += f.read()+'\n'

out += '<div style="display:inline;min-width:400px;float:left">\n' 


idf2ref = {}
count = 1
out += '<table id="conceptlists" class="dataTable clists"><tr><th>No.</th><th>Compiler</th><th>Date</th><th>Items</th><th>INFO</th></tr><tbody>'
for k in sorted(clists, key=lambda x: (bib[x]['author'], bib[x]['year'],
    bib[x]['items'])):
    
    fmt = bib.format(k, template='html')
    
    idf2ref[bib[k]['identifier']] = fmt
    
    out +='<tr id="{0}">'.format(bib[k]['identifier'])
    out += '<td>{0}</td>'.format(count)
    count += 1
    out += '<td>' + bib[k]['author_short'] + '</td>'
    out += '<td>' + bib[k]['year'] + '</td>'
    out += '<td>' + bib[k]['items'] + '</td>'
    out += '<td><button class="btn-xs btn" onclick="showReference(\''+bib[k]['identifier']+'\')">?</button></td>'
    out += '</tr>'


# write idf2ref to file
with open('../media/identifiers.js','w') as f:
    f.write('var ref2idf = '+json.dumps(ref2idf)+';\n')
    
out += '</tbody></table></div>'
out += '<div style="position:absolute;float:left;display:inline" id="popup"></div>\n'
out += '<script>'
out += 'var REFS = ' + json.dumps(idf2ref)+';\n'
out += r"""
function showReference(ref) {

  var div = document.getElementById('popup');
  var text = REFS[decodeURI(ref)];
  div.innerHTML = '<div class="outerreference"><div class="innerreference">'+text+'</div></div>';
  
  var tab = document.getElementById('conceptlists');
  for(var i=0,line; line=tab.rows[i]; i++) {
    line.style.backgroundColor = "white";
  }
  document.getElementById(decodeURI(ref)).style.backgroundColor = "Crimson";
}

var url = document.URL;
if(url.indexOf('=') != -1) {
  var query = url.split('?')[1];
  var keyvals = query.split('&');
  var params = {};
  for (var i=0; i<keyvals.length; i++) {
    var keyval = keyvals[i].split('=');
    params[keyval[0]] = keyval[1];
  }
  if(typeof params['conceptlist'] != 'undefined') {
    showReference(params['conceptlist']);
  }
}
"""
out += '</script>'

with open('../lists.md','w') as f:

    f.write('---\nlayout: default\nstatus: toplevelnc\ntitle: Lists\n---\n')
    f.write('<div style="display:none">t5</div>\n\n')
    f.write(out)
