#!/usr/bin/python

import os
import sys
import xml.sax
import re
from collections import defaultdict
from Stemmer import Stemmer

regex_store = [
    "\{\{Infobox(.+?)\}\}",
    "\[\[Category:(.+?)\]\]",
    "External links==(.+?\n\n|.+?$)",
    "<ref>(.+?)<\/ref>",
    ]

stop_words = set()
stemmer = Stemmer('porter')
chunk_size = 140000000




class WikiHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.tag = ""
        self.title = ""
        self.text = ""
        self.data = ""
        self.documentId = 0
        self.words = defaultdict(dict)
        self.titleIdMap = defaultdict()
        self.total_size = 0

    def storeInIndex(self,title,text,infobox,category,external_links,referances,cnt):
        allWordsSet=set(title.keys())
        for i in text.keys():
            allWordsSet.add(i)
        total_words = 0
        docid=str(cnt)
        for i in allWordsSet:
            freq=[]
            if title.get(i):
                freq.append(title[i])
            else :
                freq.append(0)
            if text.get(i):
                freq.append(text[i])
            else :
                freq.append(0)
            if infobox.get(i):
                freq.append(infobox[i])
            else :
                freq.append(0)
            if category.get(i):
                freq.append(category[i])
            else :
                freq.append(0)
            if external_links.get(i):
                freq.append(external_links[i])
            else :
                freq.append(0)
            if referances.get(i):
                freq.append(referances[i])
            else :
                freq.append(0)
            total_words += len(docid) + 4*len(freq)
            self.words[i][docid] = freq
        return total_words
            
    def dostuff(self,content):
        filteredContent = defaultdict(int)
        for sentence in content:
            bufword=""
            sentence+=" "
            for i in sentence:
                if i>='a' and i<='z' :
                    bufword+=i
                elif i>='0' and i<='9':
                    bufword+=i
                elif i>='A' and i<='Z':
                    bufword+=i.lower()
                else: 
                    stemmedWord = stemmer.stemWord(bufword)
                    if len(bufword)>=3 and len(bufword)<=16 and  bufword not in stop_words and stemmedWord not in stop_words:
                        filteredContent[stemmedWord]+=1
                    bufword = ""
        return filteredContent 

    # extract data from text in form of a list
    def extractDataFromText(self,flag):
        if flag == 0 or flag == 2:
            regex_object=re.findall(regex_store[flag],self.text,re.DOTALL)
        else : 
            regex_object=re.findall(regex_store[flag],self.text)
        if regex_object:
            return regex_object
        return []

    def storeInFile(self,filename,titleFilename):

        f = open(filename, 'w')

        number_of_tokens=0
        list_of_words = sorted(self.words.keys())
        for word in list_of_words:
            s=word
            freq_of_word = 0
            for doc in self.words[word].keys():
                s+=" "+doc
                temp=self.words[word][doc]
                for freq_in_doc in temp:
                    freq_of_word +=freq_in_doc
                if temp[0] > 0:
                    s+=" t"+str(temp[0])
                if temp[1] > 0:
                    s+=" b"+str(temp[1])
                if temp[2] > 0:
                    s+=" i"+str(temp[2])
                if temp[3] > 0:
                    s+=" c"+str(temp[3])
                if temp[4] > 0:
                    s+=" e"+str(temp[4])
                if temp[5] > 0:
                    s+=" r"+str(temp[5])
            s+="\n"
            if freq_of_word > 2:
                number_of_tokens+=1
                f.write(s)

        f.close()

        f = open(titleFilename, 'a')

        list_of_documentId = sorted(self.titleIdMap.keys())
        for documentId in list_of_documentId:
            f.write(str(documentId) + " " + self.titleIdMap[documentId] + "\n")
        f.close()

        return number_of_tokens

    def startElement(self, tag, attributes):
        self.tag = tag

    def endElement(self, tag):
        if tag == "page":
            # title text

            self.documentId += 1
            self.titleIdMap[self.documentId] = self.title
            
            infobox = self.dostuff(self.extractDataFromText(0))            
            category = self.dostuff(self.extractDataFromText(1))            
            external_links = self.dostuff(self.extractDataFromText(2))            
            referances = self.dostuff(self.extractDataFromText(3))            
            text = self.dostuff([self.text])
            title = self.dostuff([self.title])
            
            self.total_size += self.storeInIndex(title,text,infobox,category,external_links,referances,self.documentId)

            if self.total_size > chunk_size:
                filename = os.path.join(sys.argv[2], str(self.documentId)+".txt")
                titleFilename = sys.argv[3]
                number_of_tokens = self.storeInFile(filename,titleFilename)
                print(self.documentId)
                self.words.clear()
                self.titleIdMap.clear()
                self.total_size = 0


            self.title = ""
            self.text = ""
        elif self.tag == "title":
            self.title = self.data.strip()
        elif self.tag == "text":
            self.text = self.data.strip()
        self.tag = ""
        self.data = ""

    def endDocument(self):
        filename = os.path.join(sys.argv[2], str(self.documentId)+".txt")
        titleFilename = sys.argv[3]
        number_of_tokens = self.storeInFile(filename,titleFilename)
        self.words.clear()
        self.titleIdMap.clear()

    def characters(self, content):
        self.data += content



    

if ( __name__ == "__main__"):


    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = WikiHandler()
    parser.setContentHandler( Handler )


    fstopwords = open("stopwords.txt",'r')
    line = fstopwords.readline().split()
    for i in line:
        stop_words.add(i)
    fstopwords.close()

    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])

    parser.parse(sys.argv[1])



