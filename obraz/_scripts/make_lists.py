# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-17 09:51
# modified : 2014-10-17 09:51
"""
Make documentatin from bibtex file for all Swadesh lists in the sample.
"""

__author__="Johann-Mattis List"
__date__="2014-10-17"


from lingpyd.plugins.bibtex.bibtex import *
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
        bib[k]['reference'] += ' <a class="evobib" href="http://bibliography.lingpy.org?key='+cref+'" target="_blank">REF</a>' 
        bib[k]['reference'] += ' <a class="evobib" href="https://github.com/concepticon/lists/blob/master/sources/' + cref + '.pdf?raw=true" target="_blank">PDF</a>'
        bib[k]['reference'] += '</p>'
    
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

out += '<table style="border:0px solid white;width:100%"><tr><td style="border:0px solid white;vertical-align:top;width:50%">'
out += '<div style="display:inline;float:left">\n' 


idf2ref = {}
count = 1
out += '<table id="conceptlists" class="">'
out += '<tbody>'
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
    
out += '</tbody></table></div></td><td style="border:0px solid white;vertical-align:top;">'
out += '<div style="float:left;display:inline" id="popup"></div>\n'
out += '</td></tr></table>\n'
out += '<script src="media/vendor/jquery.dataTables.js"></script>\n'
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
var cols = [
    {"title": "No."},
    {"title": "Compiler"},
    {"title": "Date"},
    {"title" : "Item"},
    {"title" : "Info"}
];
$("#conceptlists").dataTable({"columns":cols});
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

print("Finished stuff")
