---
layout: default
status: toplevelnc
title: Compare
---
<div style="display:none;">t4</div>

<script src="media/vendor/jquery.dataTables.js" type="text/javascript"></script>
<script src="media/concepticon.js"></script>
<script src="media/bootstrap-multiselect.js"></script>

<script src="media/compare2.js"></script>
<script src="media/identifiers.js"></script>
<link rel="stylesheet" type="text/css" href="css/jquery.dataTables.css" />
  
# Concept Comparison

<div id="popup"></div>

<div style="display:block">
<div style="float:left; display: inline;" id="selector"></div>
<button class="btn btn-default" style="margin-left: 10px;" id="start" value="OK" 
  onclick="var sel = getStuff(); console.log(sel);">OK</button>
<div id="showentry" style="float:left; display: inline"></div>
</div>
<br><br>
<div style="float:left; display: none; padding:20px; border:2px solid DarkBlue;border-radius:10px;margin-top:20px;" id="datatable"></div>
<script>
var selector = document.getElementById('selector');
var txt = '';
main_list.sort();
for (var i=0,lst; lst=main_list[i]; i++) {
  var name = ref2idf[lst];
  if (name != 'undefined') {
    txt += '<option value="'+lst+'" id="id_'+lst+'">'+name+'</option>';
  }
  else {
    txt += '<option value="'+lst+'" id="id_'+lst+'">'+lst+'!'+'</option>';
  }
}
selector.innerHTML = '<select multiple id="selectlists">'+txt+'</select>';
console.log(CNC);
var url = document.URL;
if(url.indexOf('=') != -1) {
  var query = url.split('?')[1];
  var keyvals = query.split('&');
  var params = {};
  for (var i=0; i<keyvals.length; i++) {
    var keyval = keyvals[i].split('=');
    params[keyval[0]] = decodeURI(keyval[1]);
  }
  if(typeof params['conceptlist'] != 'undefined') {
    var selector = document.getElementById('selectlists');
    for (var i=0,option; option=selector[i]; i++) {
      if (option.innerHTML == params['conceptlist']) {
        option.selected = true;
      }
      else {
        option.selected = false;
      }
    }
    getStuff();//showReference(params['conceptlist']);
  }
}
$('#selectlists').multiselect({
    disableIfEmpty: true,
    includeSelectAllOption : true,
    enableFiltering: true,
    buttonClass : 'btn btn-primary',
    enableCaseInsensitiveFiltering: true,
    maxHeight: window.innerHeight-100,
    buttonText: function (options, select) {
      return 'Select concept lists <b class="caret"></b>';
    }
});
</script>
 
<p style="display:block;float:left; width:100%;">
In order to compare different concept lists with each other, just select the concept lists you want to compare
from the select box above and press OK. When comparing two or more lists, just click on the cells to see more details
for the respective cell of the concept list.
</p>
