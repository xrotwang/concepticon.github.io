---
layout: default
status: toplevelnc
title: Browse
---
<div style="display:none">t2</div>

# Browse the Concepticon

The table below lists all concepts which our Concepticon contains so far.
If you want to read the full definitions for the various concepts, just click on the field of the definition you want to view.
You can sort the table by clicking on the headers, and search the entries with help of the search field below.


<script type="text/javascript" src="media/vendor/jquery.dataTables.js"></script>
<script type="text/javascript" src="media/concepticon.js"></script>
<script>
  console.log('láuft');
</script>
<div id="popup"></div>
<div style="padding:10px;border: 2px solid DarkBlue; border-radius:10px;"><table id="datatable" style="width:100%;" cellspacing="0" cellpadding="0" border="0" class="display" ></table></div>

<script>
function showFullText(text) {
  
  var div = document.getElementById('popup');
  div.innerHTML = '<div class="outerpopup" onclick="document.getElementById(\'popup\').innerHTML=\'\';"><div class="innerpopup">'+text+'</div></div>';
}
  var cols = ['OMEGAWIKI','SEEALSO',"GLOSS","SEMANTICFIELD", "DEFINITION","POS","WOLD"];
  var table = [];
  for(key in concepticon) {
    var tmptxt = '<a href="http://www.omegawiki.org/DefinedMeaning:'+key+'" target="_blank">'+key+'</a>';
    var line = [tmptxt];
    for(var i=1,entry; entry=cols[i]; i++) {
      var tmp = concepticon[key][entry];
      if (typeof tmp != 'undefined') {
        var txt = '';
        if (entry == 'SEEALSO') {
          tmpl = tmp[0].split(';');
          for (var j=0; j < tmpl.length; j++) {
            tmpx = tmpl[j];
            txt += '<a href="http://www.omegawiki.org/DefinedMeaning:'+tmpx+'" target="_blank">' + 
              tmpx + '</a> ';
          }
        }
        else if (entry == 'DEFINITION') {
          var stxt = tmp[0].slice(0,20) + '...';
          var ftxt = tmp[0].replace(/"/g,'&quot;').replace(/'/g,'&quot;');
          txt += '<span onclick="showFullText(\''+ftxt+'\')">'+stxt+'</span>';
        }
        else if (entry == 'WOLD') {
          tmpx = tmp[0].split(';')
          for (var j=0,wld; wld=tmpx[j]; j++) {
            txt += '<a href="http://wold.clld.org/meaning/'+wld.replace(/\./,'-')+'" target="_blank">' + 
              wld + '</a> ';
          }
        }
        else {
          txt = tmp[0];
        }

        line.push(txt);
      }
      else {
        line.push('-');
      }
    }
    table.push(line);
  }
var ncols = [];
for (var i=0,col; col=cols[i]; i++) {
  if (col != 'SEMANTICFIELD' && col != 'POS') {
    ncols.push({"title":col});
  }
  else {
    ncols.push({"title":col,"bSearchable": false});
  }
}
console.log('table',table);

  var mytab = $('#datatable').dataTable({
    "data" : table,
    "columns": ncols,
  });

</script>
