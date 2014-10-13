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
      //console.log(option,key);
      try {
	keys[key].push(option); // = CNC[option][key]['GLOSS'];
      }
      catch (e) {
	keys[key] = [];
	keys[key].push(option);
	//keys[key][option] = CNC[option][key]['GLOSS'];
      }
    }
  }
  console.log('keys',keys); 
  // create table object that has all keys which occur in the set
  var mytable = [];
  for (key in keys) {
    var tmp = [];
    tmp.push(key);
    try {
      tmp.push(concepticon[key]['GLOSS']);
    }
    catch (e) {
      tmp.push('<font color="red">???</font>');
    }
    
    tmp.push(keys[key].length);
    var cnt = 0;
    for (var j=0,option; option=selected[j]; j++) {
      if (keys[key].indexOf(option) != -1) {
	try {
	  tmp.push(
	      '<span style="cursor:pointer" onclick="showEntry(this.id);" id="' + option + '_' + key+ '" class="entry">' + 
	      CNC[option][key]['GLOSS'].join(' / ') + '</span>'
	      );
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

  for (var i=0,cell; cell=selected[i]; i++) {cols.push({'title':cell.toUpperCase()});}
  
  mytable.sort(function(x,y){return parseInt(y[2]) - parseInt(x[2]);});

  console.log('bis hier');

  $('#datatable').html('<table cellpadding="0" style="width:80%;max=width:1000px" cellspacing="0" border="0" class="display" id="datatab"></table>');

  console.log(cols,mytable);
  
  $('#datatab').dataTable({"data": mytable, "columns": cols});
  
  console.log('after');
}

function showEntry(eid) {
  var tmp = eid.split('_');
  var dset = tmp[0];
  var key = tmp[1];
  
  var txt = '<table class="mytable">';
  for (k in CNC[dset][key]) {
    txt += '<tr>';
    txt += '<th>' + k + '</th>';
    txt += '<td>' + CNC[dset][key][k] + '</td>';
    txt += '</tr>';
  }
  txt += '</table>';
  document.getElementById('showentry').innerHTML = txt;
}

