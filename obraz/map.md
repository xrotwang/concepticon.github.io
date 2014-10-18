---
layout: default
status: toplevelnc
title: Map
---
<div style="display:none">t3</div>
<script type="text/javascript" src="media/jquery.js"></script>
<script type="text/javascript" src="media/vendor/sorttable.js"></script>
<script type="text/javascript" src="media/vendor/filesaver.js"></script>
<script type="text/javascript" src="media/compare.js"></script>
<div id="storeA" style="display:none"></div>
<div id="storeB" style="display:none"></div>
<p>
<div style="overflow:hidden;border:2px solid Darkblue;padding:10px;display:block;background-color:white;border-radius:10px;">
<div class="btn-group">
<input type="file" id="file" name="file" accept=".tsv" class="btn" />
<input style="margin-right:5px" type="button" id="showstuff" name="showstuff" value="SHOW" onclick="showData();" class="btn"/>
<input style="margin-right:5px" type="button" id="showstuff" name="showstuff" value="EXPORT" onclick="exportData();" class="btn"/>
</div>
<div id="db"></div>
<script src="media/compare.action.js"></script>
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


