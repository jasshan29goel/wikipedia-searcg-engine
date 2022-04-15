# WikiPedia-Search-Engine
Search  engine for entire wikipedia corpus made as minor project in course taken in semester 7, Information Retrieval and Extraction course at IIIT Hyderabad.

## Utility

* indexer.py -: it parses the xml dump and puts the sorted index into chunks of 50 mb each

* mergeIndex.py -: It merges those seperate chunks

* mergeToken.py -: it merges the same token in the seperate chunks into the same line

* split.py -: it splits the sorted index into seprate chunks of 10mb each

* stopwords.txt -: it contains the stopwords 

* search.py -: it searches the inverted index for the query

## Data
Data used is entire wikipedia corpus which is passed in indexer, and indexed results are searched while queries.

## Constructing the Inverted Index
* BasicStages(inorder):
* XML parsing: SAX parser used
* Data preprocessing 
: NLTK used
  * Tokenization 
  * Case folding
  * Stop words removal
  * Stemming
* Posting List / Inverted Index Creation
* Optimize

## Features:
* Support for Field Queries . Fields include Title, Infobox, Body, Category, Links, and
References of a Wikipedia page. This helps when a user is interested in searching for
the movie ‘Up’ where he would like to see the page containing the word ‘Up’ in the title
and the word ‘Pixar’ in the Infobox. You can store field type along with the word when
you index.
* Index size should be less than 1⁄4 of dump size. 
* Scalable index construction 
* Search Functionality
  * Index creation time: less than 60 secs for Java, CPP and for python it’s less than 150
secs.
  * Inverted index size: 1/4th of entire wikipedia corpus
* Advanced search as mentioned above.



## References
https://en.m.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia