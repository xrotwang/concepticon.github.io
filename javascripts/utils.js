/* Basic script for browsing the concepticon
 *
 * author   : Johann-Mattis List
 * email    : mattis.list@lingulist.de
 * created  : 2014-08-16 19:48
 * modified : 2014-08-16 19:48
 *
 */

/* global variable for storing the data */
var STORE = '';

function loadConcepticon()
{
  /* load the concepticon */
  $.ajax({
    async: false,
    type: "GET",
    url: "concepticon.tsv",
    dataType: "text",
    success: function(data) { STORE=data; }
  });

  /* make hash from data */
  var lines = STORE.split(/\n/);
  var concepticon = {};
  for(var i=0,row;row=lines[i];i++)
  {
    var cells = row.split('\t');
    concepticon[cells[0]] = cells.slice(1,cells.length);
  }
  return concepticon;
}
