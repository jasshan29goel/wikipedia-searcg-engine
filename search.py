#!/usr/bin/python3
import os, sys , time
import bisect
from collections import defaultdict
from Stemmer import Stemmer
import math

stemmer = Stemmer('porter')
stop_words = set()

TOTAL_PAGES = 21384756
DOCS_TO_CONSIDER  = 200000

def getFilenameContainingWord(fileList,word):
    i = bisect.bisect_left(fileList, word)
    if i != len(fileList) and fileList[i] == word:
        return fileList[i]
    elif i>0:
        return fileList[i-1]
    else:
        return None

def getFieldOfQueryWord(list_of_query_word):
    field_of_query_word = {}
    query_word = []

    field = '-'
    for i in list_of_query_word:
        if len(i) >= 2:
            if i[1] == ":":
                word = i[2:]
                field = i[0]
            else:
                word = i
            word = stemmer.stemWord(word.lower())
            if len(word) > 1 and word not in stop_words:
                query_word.append(word)
                field_of_query_word[word] = field

    return sorted(query_word) , field_of_query_word

def getIndexOfWords(query_word,fileList):
    
    word_dict = {}
    no_of_words = len(query_word)
    current_word = 0

    filename = getFilenameContainingWord(fileList,query_word[current_word])
    f=open(os.path.join(sys.argv[1], filename),'r')

    while True:
        line = f.readline()
        if not line:
            f.close()
            current_word += 1
            if current_word == no_of_words:
                return word_dict
            filename = getFilenameContainingWord(fileList,query_word[current_word])
            f=open(os.path.join(sys.argv[1], filename),'r')
            f.readline()

        line = line.split(' ',1)
        if line[0] == query_word[current_word]:
            word_dict[query_word[current_word]] = line[1]
            current_word += 1
            if current_word == no_of_words:
                f.close()
                return word_dict
            tempFilename = getFilenameContainingWord(fileList,query_word[current_word])
            if tempFilename != filename:
                f.close()
                filename = tempFilename
                f=open(os.path.join(sys.argv[1], filename),'r')


def getTitleCorrespondingToDocument(score_of_documents,fileList):

    top_docs = sorted(score_of_documents, key=score_of_documents.get,reverse=True)
    if len(top_docs) <= 10:
        for i in range(1,11-len(top_docs)):
            top_docs.append(i)

    titles = []
    cnt =0
    for docid in top_docs:
        filename = str(getFilenameContainingWord(fileList,docid))
        f=open(os.path.join(sys.argv[3], filename),'r')

        while True:
            line = f.readline()
            if not line:
                f.close()
                break
            line = line.split(' ',1)
            if int(line[0]) == docid:
                if line[1].startswith("Wikipedia:"):
                    pass
                else:
                    cnt+=1
                    titles.append(line[0]+ ", " + line[1])
                f.close()
                break
        if cnt ==10:
            break
    return titles
     


def calTfWeight(freq):
    return math.log(1+freq)

def calIdfWeight(total_docs):
    return math.log(TOTAL_PAGES/total_docs)

def getScoreOfDocuments(word_index,field_of_query_word):

    score_of_documents = defaultdict(int)

    for token in word_index.keys():
        
        index = word_index[token]
        index = index.split()
        
        if field_of_query_word[token] =='l':
            field_of_query_word[token] = 'e'

        if field_of_query_word[token] == '-':
            field_of_current_word = {'t':80,'b':1,'i':10,'c':4,'r':4,'e':1}
        else:
            field_of_current_word = {'t':0,'b':0,'i':0,'c':0,'r':0,'e':0}
            field_of_current_word[field_of_query_word[token]] = 100


        idfWeight = calIdfWeight(int(index[0]))
        index = index[1:]

        document_id = 0
        sum_freq = 0

        cnt = 0

        for item in index:
            if item[0] >='a' and item[0]<='z':
                sum_freq += int(item[1:])*field_of_current_word[item[0]]
            else:
                if sum_freq > 0 :
                    score_of_documents[document_id]+= calTfWeight(sum_freq)*idfWeight
                    sum_freq = 0
                    
                document_id = int(item)
                cnt+=1

            if cnt > DOCS_TO_CONSIDER:
                break
            
        score_of_documents[document_id]+= calTfWeight(sum_freq)*idfWeight
    return score_of_documents


# importing the list of files in the index
fileList = sorted(os.listdir(sys.argv[1]))

# importing the list of files contaning document id title map 
titleFilelist = os.listdir(sys.argv[3])
for i in range(0,len(titleFilelist)):
    titleFilelist[i] = int(titleFilelist[i])
titleFilelist = sorted(titleFilelist)

# importing stop words file in a set
fstopwords = open("stopwords.txt",'r')
line = fstopwords.readline().split()
for i in line:
    stop_words.add(i)
fstopwords.close()

# opening query file
file_query = open(sys.argv[2],'r')

# opening results file
file_result = open('queries_op.txt','w')

# running the query file
while True:
    line = file_query.readline()

    if not line:
        file_query.close()
        break
    if len(line) == 0 or line.isspace():
        continue
    
    start = time.time()

    query_word,field_of_query_word = getFieldOfQueryWord(line.split())
    if len(query_word) == 0:
        ans = getTitleCorrespondingToDocument({},titleFilelist)
    else :        
        word_index = getIndexOfWords(query_word,fileList)
        score_of_documents = getScoreOfDocuments(word_index,field_of_query_word)
        ans = getTitleCorrespondingToDocument(score_of_documents,titleFilelist)

    for i in ans:
        file_result.write(i)

    end = time.time()
    
    if (end-start) > 5:
        print("warning")

    file_result.write(str(end-start) + "\n\n")
file_result.close()    

