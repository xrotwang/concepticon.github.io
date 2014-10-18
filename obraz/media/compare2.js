/* basic function to load a given set of concept lists */
function getStuff() {
  var selector = document.getElementById('selectlists');
  var selected = [];
  for (var i=0,option; option=selector[i]; i++) {
    if (option.selected) {
      selected.push(option.value);
    }
  }
  if(!selected) {return;}

  var keys = {};
  // get all keys in the data
  for (var i=0,option; option = selected[i]; i++) {
    for (key in CNC[option]) {
      try {
	keys[key].push(option);
      }
      catch (e) {
	keys[key] = [];
	keys[key].push(option);
      }
    }
  }
  console.log('keys',keys); 
  // create table object that has all keys which occur in the set
  var mytable = [];
  for (key in keys) {
    var tmp = [];
    tmp.push('<a target="_blank" href="http://www.omegawiki.org/DefinedMeaning:'+key+'">'+key+'</a>');
    try {
      var gloss = concepticon[key]['GLOSS'];
      tmp.push('<span style="cursor:pointer" onclick="showConcepticon(\''+key+'\');">'+gloss+'</span>');
    }
    catch (e) {
      tmp.push('<font color="red">?'+key+'?</font>');
    }
    tmp.push(keys[key].length);
    var cnt = 0;
    for (var j=0,option; option=selected[j]; j++) {
      if (keys[key].indexOf(option) != -1) {
	      try {
          
          /* check for multilinks */
          var tmp_gloss = CNC[option][key]['GLOSS'].join(' / ');
          var tmp_txt = '<span style="cursor:pointer;';
          if (tmp_gloss in MULTIGLOSS[option]) {
            tmp_txt += 'color:Green;';
          }
          if (key in MULTIKEY[option]) {
            tmp_txt += 'font-weight:bold;';
          }
          tmp_txt += '" onclick="showEntry(this.id);" id="' + option + ':' + key + '" class="entry">'
            + tmp_gloss + '</span>';

	        tmp.push(tmp_txt);
	      }
	      catch (e) {
	        tmp.push('<font color="red">???</font>');
	      }
	      cnt += 1;
      }
      else {
	      tmp.push('-');
      }
    }
    tmp[2] = cnt;
    mytable.push(tmp);
  }
  var cols = [{'title':'KEY'}, {'title':'GLOSS'}, {'title':'OCCS'}];

  for (var i=0,cell; cell=selected[i]; i++) {cols.push({'title':ref2idf[cell]});}
  
  mytable.sort(function(x,y){return parseInt(y[2]) - parseInt(x[2]);});

  console.log('bis hier');
  
  document.getElementById('datatable').style.display = 'block';
  $('#datatable').html('<table cellpadding="0" style="width:80%;max=width:1000px" cellspacing="0" border="0" class="displayb" id="datatab"></table>');

  console.log(cols,mytable);
  
  $('#datatab').dataTable({"data": mytable, "columns": cols});
  
  console.log('after');
}

function showEntry(eid) {
  var tmp = eid.split(':');
  var dset = tmp[0];
  var key = tmp[1];
  
  var txt = '<table class="clists dataTable">';
  for (k in CNC[dset][key]) {
    txt += '<tr>';
    txt += '<th>' + k + '</th>';
    if (k == "URL") {
      txt += '<td><a target="_blank" href="'+CNC[dset][key][k]+'">'+CNC[dset][key][k]+'</a></td>';
    }
    else {
      txt += '<td>' + CNC[dset][key][k] + '</td>';
    }
    txt += '</tr>';
  }
  txt += '</table>';
  
  var out_txt = '<div class="outerpopup" onclick="document.getElementById(\'popup\').innerHTML=\'\';"><div class="innerpopup">' + txt + '</div></div>';
  document.getElementById('popup').innerHTML = out_txt;
}

function showConcepticon(key) {
  
  var txt = '<table class="clists dataTable">';
  for (k in concepticon[key]) {
    txt += '<tr>';
    txt += '<th>'+k+'</th>';
    if(k == 'WOLD') {
      txt += '<td><a target="_blank" href="http://wold.clld.org/meaning/'+concepticon[key][k][0].replace(/\./,'-')+'">'+concepticon[key][k][0]+'</a></td>';
    }
    else {
      txt += '<td style="max-width:400px;">'+concepticon[key][k][0]+'</td>';
    }
    txt += '</tr>';
  }
  txt += '</table>';
  var out_txt = '<div class="outerpopup" onclick="document.getElementById(\'popup\').innerHTML=\'\';"><div class="innerpopup">' + txt + '</div></div>';
  document.getElementById('popup').innerHTML = out_txt;

  //document.getElementById('showentry').innerHTML = txt;
}


