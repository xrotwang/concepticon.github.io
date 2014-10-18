document.getElementById('file').addEventListener('change', fileSelect('storeB'), false);
loadFile('concepticonS.tsv',false,'storeA');
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
          var textf = '%'; 
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
          text += '\t?\tNA\n';
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
  head += '\tOMEGAWIKI\tCONCEPTICON_GLOSS\n';
  db.innerHTML = count+' direct matches (+)<br>'+scount+' multiple matches (!)<br>'+vcount+' indirect matches (?)<br>'+fcount+' fuzzy matches (%)<br>'+mcount+' mismatches (-)'; 
  db.innerHTML += '<br><textarea style="font-size:12px;padding:20px;border:2px solid Crimson;background-color: lightgray;" id="mytext" rows="80" cols="100">'+head+commons+'</textarea>';
}
function exportData()
{
  var storeB = document.getElementById('mytext');
  new_text = storeB.value;
  var blob = new Blob([new_text], {type: "text/plain;charset=utf-8"});
  saveAs(blob, 'merged.tsv');  
}

