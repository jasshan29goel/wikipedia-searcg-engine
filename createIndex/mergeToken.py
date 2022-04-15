import sys


def compressSentence(sentence):

    freq_of_docs = []
    
    sentence = sentence.split()

    document_id = 0
    freq = [0,0,0,0,0,0,0,0]
    for item in sentence:
        if item[0] == 't':
            freq[0] = int(item[1:])
        elif item[0] == 'i':
            freq[1] = int(item[1:])
        elif item[0] == 'c':
            freq[3] = int(item[1:])
        elif item[0] == 'r':
            freq[4] = int(item[1:])
        elif item[0] == 'e':
            freq[5] = int(item[1:])
        elif item[0] == 'b':
            freq[6] = int(item[1:])
        else:
            if document_id !=0:
                freq [2] = freq[3]+freq[4]+freq[5]+freq[6]
                freq_of_docs.append(freq)
            
            document_id = int(item)
            freq = [0,0,0,0,0,0,0,0]
            freq[7] = document_id
    freq [2] = freq[3]+freq[4]+freq[5]+freq[6]
    freq_of_docs.append(freq)

    freq_of_docs = sorted(freq_of_docs,reverse = True)

    new_sentence = ""

    for i in range(0,len(freq_of_docs)):
        new_sentence += str(freq_of_docs[i][7]) + " "

        if freq_of_docs[i][0] != 0:
            new_sentence += 't' + str(freq_of_docs[i][0]) + " "
        if freq_of_docs[i][1] != 0:
            new_sentence += 'i' + str(freq_of_docs[i][1]) + " "
        if freq_of_docs[i][3] != 0:
            new_sentence += 'c' + str(freq_of_docs[i][3]) + " "
        if freq_of_docs[i][4] != 0:
            new_sentence += 'r' + str(freq_of_docs[i][4]) + " "
        if freq_of_docs[i][5] != 0:
            new_sentence += 'e' + str(freq_of_docs[i][5]) + " "
        if freq_of_docs[i][6] != 0:
            new_sentence += 'b' + str(freq_of_docs[i][6]) + " "
    return new_sentence

f = open(sys.argv[1],'r')
file1 = open(sys.argv[2],'w')
sentence = ""
token = ""
while True:
    line = f.readline()
    if not line :
        break
    line = line.split(' ',1)
    line[1]=line[1].strip()
    if line[0] == token:
        sentence = sentence + " " + line[1]
    elif len(token) == 0:
        token = line[0]
        sentence = line[1]
    else :
        sentence = compressSentence(sentence)
        file1.write(token + " " + sentence + "\n")
        token = line[0]
        sentence = line[1]

f.close()
if len(token) != 0:
    
    sentence = compressSentence(sentence)
    file1.write(token + " " + sentence + "\n")
file1.close()




    