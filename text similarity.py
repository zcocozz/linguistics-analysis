###8）text similarity
###1：input
import os
path = r"/Users/cocoz/Desktop/driven/1.txt"
filenameList = os.listdir(path)
filesList = []
for filename in filenameList:
    file = open( path +'/' +filename, encoding = 'utf-8',errors='ignore').read()
    filesList.append(file)
###2:reference text
import nltk
allList = []
for line in filesList:
    lineList = [word for word in nltk.word_tokenize(line)]
    allList.append(lineList)
sentTest = filesList[1]
testList = [word for word in nltk.word_tokenize(sentTest)]
###3：apply gensim  
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary(allList)
corpus = [dictionary.doc2bow(line) for line in allList]
testVec = dictionary.doc2bow(testList)
tfidf = models.TfidfModel(corpus)
###4：text similarity
index = similarities.SparseMatrixSimilarity(tfidf[corpus],
                                            num_features = len(dictionary.keys()))
simValue = index[tfidf[testVec]]
sorted(enumerate(simValue), key = lambda item: -item[1])
