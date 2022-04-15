import sys
import os

chunk_size = 10000000
NO_OF_DOCS = 1000000
def compressSentence(sentence):

    if len(sentence) == 0 or sentence.isspace():
        return sentence
    sentence = sentence.split(' ',1)
    new_sentence = sentence[0]

    sentence = sentence[1].split()
    idf = 0
    for i in sentence:
        if i[0] >='0' and i[0]<='9':
            idf+=1
    new_sentence += " " + str(idf)

    idf = 0
    for i in sentence:
        if i[0] >='0' and i[0]<='9':
            idf+=1
            if idf > NO_OF_DOCS:
                break
        new_sentence += " " + i

    new_sentence+="\n"
    return new_sentence

if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

f = open(sys.argv[1],'r')

line = f.readline()
filename = line.split(' ',1)[0]
total_byte_cnt = len(line)
filetemp = open(os.path.join(sys.argv[2],filename),'w')

total_tokens = 0
while True:
    if not line :
        break

    if total_byte_cnt > chunk_size :

        filetemp.close()

        total_byte_cnt = len(line)
        filename = line.split(' ',1)[0]
        filetemp = open(os.path.join(sys.argv[2],filename),'w')

    total_tokens += 1
    filetemp.write(line)
    line = compressSentence(f.readline())
    total_byte_cnt += len(line)

print(total_tokens)
filetemp.close()
f.close()