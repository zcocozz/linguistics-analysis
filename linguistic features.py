###1）STTR
from nltk.corpus import PlaintextCorpusReader
corpus_root = r"/Users/cocoz/Desktop/driven/all"
corpora = PlaintextCorpusReader(corpus_root, ['DeepL.txt'])
myfiles = corpora.words('DeepL.txt')
text = [word.lower() for word in myfiles if word.isalpha()]
 
cumulativeTTR = 0
TTR = 0
num_of_thousand = int(len(text)/1000)
count_sum = 0
temp_list = []
residual_list = text[num_of_thousand*1000:len(text)]
residualTTR = len(set(residual_list))/len(residual_list)
for i in range(num_of_thousand):
    temp_list = text[i*1000:(i+1)*1000]
    TTR = len(set(temp_list))/len(temp_list)
    cumulativeTTR = cumulativeTTR + TTR
totalTTR = cumulativeTTR + residualTTR
stdTTR = totalTTR/(num_of_thousand + 1)
print ('--Results--')                               
print ('      Tokens:', len(text))                  
print ('       Types:', len(set(text)))             
print ('Types/Tokens:', len(set(text))/len(text))  
print ('        STTR:', stdTTR)                     
###
import prettytable as pt
tb = pt.PrettyTable()
tb.field_names = [ "items", "result"]
tb.add_row(["Tokens",len(text)])
tb.add_row(["Types",len(set(text))])
tb.add_row(["Types/Tokens", len(set(text))/len(text)])
tb.add_row(["STTR", stdTTR])
print(tb)


###2）Lexical Density
###2-1：data
path = r'/Users/cocoz/Desktop/driven/youdao'
import os, nltk
filenameList = os.listdir(path)
filesList = []
for filename in filenameList:
    file = open(path + '/' + filename, encoding='utf-8',errors='ignore').read()
    filesList.append(file)
###2-2：function words
f = open(r'/Users/cocoz/Desktop/Python/171101_stopword_list_density.txt', encoding='utf8')
f_read = f.read()
f.close()
stopwords_list = f_read.split(', ')
###2-3：density
wordDensityList = []
for fileI in filesList:
    fileText = nltk.word_tokenize(fileI)
    fileClean = [word for word in fileText if word.isalpha()]
    fileClean2 = [word for word in fileClean if word not in stopwords_list]
    wordDensity = len(fileClean2) / len(fileClean)
    wordDensityList.append(round(wordDensity, 4))
wordDensityList.insert(0,'Lexical Density')
print(wordDensityList)
###2-4：text name
textList = []
for text in filenameList:
    textName = text.split()[0]
    textList.append(textName)
textList.insert(0, 'variant')
###2-5：Excel
import pandas as pd
df = pd.DataFrame(columns=textList)
add = pd.DataFrame(dict(zip(textList, wordDensityList)), index=[1])
df.reset_index(drop=True, inplace=True)
df = pd.DataFrame(dict(zip(textList, wordDensityList)), index=[1])
path = r'/Users/cocoz/Desktop/youdao.xlsx'
writer = pd.ExcelWriter(path)
df.to_excel(writer, index = None)
writer.save()

###3）Lexical uniqueness
###3-1：pos tagging
path = r'/Users/cocoz/Desktop/driven/youdao'
import nltk
def find_pos(text):
    pos = nltk.pos_tag(nltk.word_tokenize(text), tagset='universal')
    tags = []
    for i in pos:
        if i[1][0].lower() == 'a':
            tags.append('a')
        elif i[1][0].lower() == 'r':
            tags.append('r')
        elif i[1][0].lower() == 'v':
            tags.append('v')
        else:
            tags.append('n')
    return tags
###3-2：lemmatize
import os, nltk
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
files = os.listdir(path)
filesListC = []
for file in files:
    readFile = open(path + '/' + file, encoding="UTF-8-sig",errors='ignore').read()
    tokens = nltk.word_tokenize(readFile.lower())
    tags = find_pos(readFile)
    lemma_words = []
    for i in range(0, len(tokens)):
        lemma_words.append(wnl.lemmatize(tokens[i], tags[i]))
    text2 = [word.lower() for word in lemma_words if word.isalpha()]
    filesListC.append(text2)
len(filesListC)
###3-3：compute
originalList = []
for n in range(len(filesListC)):
    numList = list(range(len(filesListC)))
    numList.remove(n)
    otherList = []
    for i in numList:
        otherList += filesListC[i]
    oneList = []
    for word in filesListC[n]:
        if word not in otherList:
            oneList.append(word)
            ratio = len(oneList) / len(filesListC[n])
    originalList.append(round(ratio, 4))
    numList.insert(n, n)
originalList.insert(0, 'uniqueness')
'''
###loop
a = [0,1,2,3]
for n in a:
    a.remove(n)
    print(a)
    a.insert(n,n)
'''
###3-4：Excel
import pandas as pd
path2 = r'/Users/cocoz/Desktop/youdao.xlsx'
df4 = pd.read_excel(path2)
add4 = pd.DataFrame(dict(zip(textList, originalList)), index=[1])
df4 = df4.append(add4, ignore_index=True)
writer = pd.ExcelWriter(path2)
df4.to_excel(writer, index = None)
writer.save()

###4）mean word length
###4-1：data clean
import nltk
import numpy as np
filesListClean = []
for line in filesList:
    line2 = [w for w in nltk.word_tokenize(line) if w.isalpha()]
    wordLength = []
    for word in line2:
        wordLength.append(len(word))
    filesListClean.append(wordLength)
wordMeanList = []
for item in filesListClean:
    mean = np.mean(item)
    wordMeanList.append(round(mean, 4))
wordMeanList.insert(0, 'mean word length')
###4-2：Excel
import pandas as pd
path2 = r'/Users/cocoz/Desktop/youdao.xlsx'
df5 = pd.read_excel(path2)
add5 = pd.DataFrame(dict(zip(textList, wordMeanList)), index=[1])
df5 = df5.append(add5, ignore_index=True)
writer = pd.ExcelWriter(path2)
df5.to_excel(writer, index = None)
writer.save()

###5）mean/median sentence length
###5-1：paragraph/sentence tokenize
sentWholeList = []
for line in filesList:
    sentList = []
    para = line.split('\n')
    for item in para:
        sent = nltk.sent_tokenize(item)
        sentList += sent
    sentWholeList.append(sentList)
###5-2：calculate
sentMeanList = []
sentMedianList = []
for item in sentWholeList:
    item2 = [len(sent.split()) for sent in item]
    mean = np.mean(item2)
    median = np.median(item2)
    sentMeanList.append(round(mean, 4))
    sentMedianList.append(round(median, 4))
sentMeanList.insert(0, 'mean sentence length')
sentMedianList.insert(0, 'median sentence length')
###5-3：Excel
import pandas as pd
path2 = r'/Users/cocoz/Desktop/youdao.xlsx'
df71 = pd.read_excel(path2)
add71 = pd.DataFrame(dict(zip(textList, sentMeanList)), index=[1])
df71 = df71.append(add71, ignore_index=True)
writer = pd.ExcelWriter(path2)
df71.to_excel(writer, index = None)
writer.save()
df72 = pd.read_excel(path2)
add72 = pd.DataFrame(dict(zip(textList, sentMedianList)), index=[1])
df72 = df72.append(add72, ignore_index=True)
writer = pd.ExcelWriter(path2)
df72.to_excel(writer, index = None)
writer.save()

###6）Text readability
###6-1：textstat
import textstat
readabilityList = []
for item in filesList:
    score = textstat.flesch_reading_ease(item)
    readabilityList.append(score)
readabilityList.insert(0, 'Text readability')
###6-2：Excel
import pandas as pd
path2 = r'/Users/cocoz/Desktop/youdao.xlsx'
df8 = pd.read_excel(path2)
add8 = pd.DataFrame(dict(zip(textList, readabilityList)), index=[1])
df8 = df8.append(add8, ignore_index=True)
writer = pd.ExcelWriter(path2)
df8.to_excel(writer, index = None)
writer.save()

