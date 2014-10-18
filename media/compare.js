var destination = 'store';
function fileSelect(dest)
{
  if(typeof dest == 'undefined'){destination = 'store';}
  else{destination = dest;}
  return handleFileSelect;
}
/* file-handler function from http://www.html5rocks.com/de/tutorials/file/dndfiles/ */
function handleFileSelect(evt)
{
  dest = destination;

  db = document.getElementById('db');
  db.innerHTML = ''; //dest;

  var files = evt.target.files; /* FileList object */

  var file = files[0];
  var store = document.getElementById(dest);
  
  /* create file reader instance */
  var reader = new FileReader();
  reader.onload = function(e){store.innerText = reader.result;}
  reader.readAsText(file);
}

/* read csv data from destination and return a searchable hash object */
function getCSV(dest)
{
  if(typeof dest == 'undefined'){dest = 'store';}

  var store = document.getElementById(dest);
  var data = store.innerText;
  var lines = data.split(/\n|\r\n/);
  var counter = 0;
  var start = 0;
  var CSV = {};

  var db =document.getElementById('db');

  for(i=0;i<lines.length;i++)
  {
    line = lines[i];
    
    if(line[0] != '#' && line.length > 0 && line[0] != ' ')
    {
      if(start == 1)
      {
        points = line.split('\t');
        counter += 1;
        var filler = {};
        for(j=0,p;p=points[j];j++)
        {
          filler[header[j]] = p; 
        }
        CSV[counter] = filler;
      }
      else
      {
        console.log(line);
        start = 1;
        counter = 1;
        var points = line.split('\t');
        var header = {};


        for(var j=0, p; p = points[j]; j++)
        {
          header[j] = p.toLowerCase();
        }
      }
    }
  }
  CSV['header'] = header;
  console.log(header);
  console.log(CSV);

  return CSV;
}


function loadFile(url,wait,dest)
{
  $.ajax({
    async: wait,
    type: "GET",
    url: url,
    dataType: "text",
    success: function(data) { storeText(data,dest); }
  });
}

function storeText(data, dest)
{
  if(typeof dest == 'undefined'){dest = 'store';}
  var store = document.getElementById(dest);
  store.innerText = data;
}

