---
layout: default
status: toplevelnc
title: Map
---
<div style="display:none">t3</div>

<script type="text/javascript" src="javascripts/vendor/jquery-1.11.1.min.js"></script>
<script type="text/javascript" src="javascripts/vendor/sorttable.js"></script>
<script type="text/javascript" src="javascripts/vendor/filesaver.js"></script>
<script type="text/javascript" src="javascripts/compare.js"></script>
<style>
table {
  border: 2px solid black;
}
td {
  max-width: 250px;
}
.DEFINITION {
  border: 1px solid gray;
  max-width: 400px;
  font-size: 80%;
}
/* Sortable tables */
table.sortable thead {
  background-color:lightgray;
  color:#000000;
  //font-weight: bold;
  cursor: pointer;
}

span.hovera{
  color: red;
  font-weight: bold;
}
div.hoverb{
  display:none;
}
span.hovera:hover .hoverb{
  display: block;
  font-weight: normal;
  background-color: CornFlowerBlue;
  color: white;
}
tr {
  border: 1px solid black;
}
</style>
<script>
if (window.File && window.FileReader && window.FileList && window.Blob) 
{
}
else
{
  alert("The File APIs are not fully supported in this browser.");
}

</script>
<div id="storeA" style="display:none"></div>
<div id="storeB" style="display:none"></div>
<p>
<div style="border:2px solid Darkblue;padding:10px;display:block;background-color:white;border-radius:10px;">
<div class="btn-group">
<input type="file" id="file" name="file" accept=".tsv" class="btn" />
<input style="margin-right:5px" type="button" id="showstuff" name="showstuff" value="SHOW" onclick="showData();" class="btn"/>
<input style="margin-right:5px" type="button" id="showstuff" name="showstuff" value="EXPORT" onclick="exportData();" class="btn"/>
</div>
<div id="db"></div>
<script>
document.getElementById('file').addEventListener('change', fileSelect('storeB'), false);
</script>
<script>
loadFile('data/concepticonF.tsv',false,'storeA');
function showData()
{
  var db = document.getElementById('db');
  var csv1 = getCSV('storeA');
  var csv2 = getCSV('storeB');

  // extract glosses
  var glossesA = {};
  for(key in csv1)
  {
    if(key != 'header')
    {
      var fgloss = csv1[key]['fgloss'];
      if(fgloss in glossesA)
      {
        glossesA[fgloss] = glossesA[fgloss]+'/'+key;
      }
      else
      {
        glossesA[fgloss] = key;
      }
    }
  }
  var commons = '';
  var count = 0;
  var scount = 0;
  var vcount = 0;
  var fcount = 0;
  var mcount = 0;

  var glossesB = [];
  for(key in csv2)
  {
    commons += '\n';
    if(key != 'header')
    {
      var gloss = csv2[key]['gloss'].toLowerCase();
      if(gloss in glossesA)
      {
        var textf = ''; //'\t'+key+'\t'+gloss;
        var text = '';
        for(k in csv2[key])
        {
          textf += '\t'+csv2[key][k];
        }
        if(glossesA[gloss].indexOf('/') != -1)
        {
          var keys = glossesA[gloss].split('/');
          for(var i=0,k;k=keys[i];i++)
          {
            text += '!' + textf + '\t' + csv1[k]['omegawiki']+'\t'+csv1[k]['gloss']+'\n';
          }
          scount += 1;
        }
        else
        {
          count += 1;
          text = '+'+textf+'\t'+csv1[glossesA[gloss]]['omegawiki']+'\t'+csv1[glossesA[gloss]]['gloss'] + '\n';
        }
        commons += text;
      }
      else if(gloss.replace(/^to /,'').replace(/[?!\.]/,'') in glossesA)
      {
        vcount += 1;
        var ngloss = gloss.replace(/^to /,'').replace(/[?!]/,'');
        var textf = '?';
        var text = '';
        for(k in csv2[key])
        {
          textf += '\t'+csv2[key][k];
        }
        if(glossesA[ngloss].indexOf('/') != -1)
        {
          var keys = glossesA[ngloss].split('/');
          for(var i=0,k;k=keys[i];i++)
          {
            text += textf + '\t' + csv1[k]['omegawiki']+'\t'+csv1[k]['gloss']+'\n';
          }
        }
        else
        {
          text += textf + '\t'+csv1[glossesA[ngloss]]['omegawiki']+'\t'+csv1[glossesA[ngloss]]['gloss']+'\n';
        }
        commons += text;
      }
      else
      {
        // try to split the stuff and to search for indirect matches
        var ngloss = gloss.replace(/^to /,'').replace(/[?!()]/,'').replace(/\//,',');
        var nglosses = ngloss.split(/[\/\s,;]+/g);
        var matches = [];
        for(i=0;i<nglosses.length;i++)
        {
          k = nglosses[i].replace(/\s/g,'');
          
          if(k in glossesA)
          {
            matches.push(k.toLowerCase())
          }
        }
        if(matches.length >= 1)
        {
          fcount += 1;
          var textf = '%'; //+'\t'+key+'\t'+gloss;
          var text = '';
          for(k in csv2[key])
          {
            textf += '\t'+csv2[key][k];
          }
          var texta = '';
          for(var i=0;i<matches.length;i++)
          {
            var m = matches[i];
            if(glossesA[m].indexOf('/') != -1)
            {
              var keys = glossesA[m].split('/');
              for(var j=0,k;k=keys[j];j++)
              {
                text += textf+'\t'+csv1[k]['omegawiki']+'\t'+csv1[k]['gloss']+'\n'
              }
            }
            else
            {
              texta += textf+'\t'+csv1[glossesA[m]]['omegawiki']+'\t'+csv1[glossesA[m]]['gloss']+'\n';
            }
          }
          commons += text + texta; // + '\t'+texts.join('; ')+'\n';
        }
        else
        {
          var text = '-';
          for(k in csv2[key])
          {
            text += '\t'+csv2[key][k];
          }
          text += '\t?\n';
          commons += text;
          mcount += 1;
        }
      }
    }
  }
  var head = 'MATCH';
  for(k in csv2["header"])
  {
    head += '\t'+csv2['header'][k].toUpperCase();
  }
  head += '\tOMEGAWIKI\tCGLOSS\n';
  db.innerHTML = count+' direct matches (+)<br>'+scount+' multiple matches (!)<br>'+vcount+' indirect matches (?)<br>'+fcount+' fuzzy matches (%)<br>'+mcount+' mismatches (-)'; 

  db.innerHTML += '<br><textarea style="padding:20px;border:2px solid Crimson;background-color: lightgray;" id="mytext" rows="80" cols="60">'+head+commons+'</textarea>';
}

function exportData()
{
  var storeB = document.getElementById('mytext');
  new_text = storeB.value;
  var blob = new Blob([new_text], {type: "text/plain;charset=utf-8"});
  saveAs(blob, 'merged.tsv');  
}
</script>
</div></p> 

# Mapping concept lists to the Concepticon

Suppose you are currently compiling a dataset which you want to explore with help of computational tools. If you do so, you will probably have some kind
of concept list which determines the initial selection of cognate sets. 
Mapping this concept list the the Concepticon will offer many advantages:
You can

* easily extract sublist of other database projects and compare their findings with yours (provided these projects are also mapped to the Concepticon),
* easily retrieve stability indices for concepts which are less prone to change than others, since the Concepticon provides mappings to ranked concept lists, like, for example, the *Leipzig Jakarta Index* of the [WOLD project](wold.clld.org).
* make full use of other kinds of data provided along with the Concepticon, like definitions of concepts, links to other resources, etc.

# How to map a concept list to the concepticon

All you need to make an initial mapping from your concept list to the Concepticon is a tab-separated value file which stores all your concepts.
This file can contain as many columns as you want, as long as one of the columns is named "GLOSS" (this is what we need to carry out an initial mapping). You also need to make sure that the first line gives all column names, while the following lines give the data. 
As a simple example for such a format, consider the following example:

<pre><code>NUMBER	GLOSS
1	HAND
2	FOOT
3	LEG
</code></pre>

If you browse this data with help of our concept mapper, it will give you the following output (which you can download):
<pre><code>MATCH	NUMBER	GLOSS	OMEGAWIKI	CGLOSS
!	1	hand	1527192	CARRY IN HAND
!	1	hand	5616	HAND
!	1	hand	529277	PALM OF HAND  
+	2	foot	5672	FOOT  
!	3	leg	156660	CALF OF LEG
!	3	leg	5665	LEG
!	3	leg	1541261	LOWER LEG
!	3	leg	1543636	UPPER LEG
</code></pre>

The column on the left displays the kind of mapping, our method could find. We distinguish:

* direct matches (+)
* multiple matches (!)
* indirect matches (?)
* fuzzy matches (%), and
* mismatches (-)

The last two columns give you:

* the link to the Concepticon (in case one possible mapping could be found), and 
* the basic gloss we use to denote the concept.

As you can see from the example, the concept mapper searches for quite a few different mapping possibilities. 
So you will have to edit the file yourself by deleting those lines which do not quite match with the concepts you had in mind. However, making the mapping procedure more exact will also force you to look for missing concepts youself. Currently, we think it is more useful to provide more mapping possibilities than less.

# Using the concept mapper

In order to use the concept mapper, follow the following steps:

* Upload a file with help of the BROWSE button on the left.
* Load the file-content by pressing the SHOW button.
* Edit the text in the browser according to your wishes (remove multiple matches, add
	missing matches, etc.).
* Save the edited file content by pressing the EXPORT button and specifying a
	download location.


