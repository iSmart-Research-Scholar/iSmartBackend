from gensim.parsing.preprocessing import remove_stopwords # this helps to remove the stop words
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import json

def ranking(data, query, choosen):
    totalRetrieved = data['total_records']
    totalSearched = data['total_searched']
    articles = data['articles']
    query = remove_stopwords(query).lower()
    listWords = query.split(' ')
    for index, word in enumerate(listWords):
        listWords[index] = word
    listStore = []
    dictScore = {}
    # Calculating the IDF for each word
    dictIDFTitle = {}
    dictIDFWord = {}
    for i in range(len(articles)):
        title = articles[i]['title']
        abstract = articles[i]['abstract']
        title = ps.stem(remove_stopwords(title).lower())
        abstract = ps.stem(remove_stopwords(abstract).lower())
        for word in listWords:
            if title.count(word) > 0:
                if word not in dictIDFTitle:
                    dictIDFTitle[word] = 1
                else:
                    dictIDFTitle[word] += 1
            if abstract.count(word) > 0:
                if word not in dictIDFWord:
                    dictIDFWord[word] = 1
                else:
                    dictIDFWord[word] += 1
    

    for i in range(len(articles)):
        weight = 0
        title = articles[i]['title']
        abstract = articles[i]['abstract']
        citations = articles[i]['citing_paper_count']
        title = ps.stem(remove_stopwords(title).lower())
        abstract = ps.stem(remove_stopwords(abstract).lower())
        for word in listWords:
            countTitle = title.count(word)
            countAbstract = abstract.count(word)
            totalTitle = len(title.split(' '))
            totalAbstract = len(abstract.split(' '))
            if word in dictIDFTitle:
                weight += (totalRetrieved/(dictIDFTitle[word]+1)) * (countTitle/totalTitle)
            if word in dictIDFWord:
                weight += (totalRetrieved/(dictIDFWord[word]+1)) * (countAbstract/totalAbstract)
        
        weight = weight + citations*0.5
        weight = round(weight, 2)
        listStore.append([weight, articles[i]['publication_year'], articles[i]['citing_paper_count'], i])
    if choosen == 1:
        listStore = sorted(listStore, key = lambda x:(x[1], x[0]), reverse=True)
    elif choosen == 2:
        listStore = sorted(listStore, key = lambda x:(x[1], x[0]), reverse=True)
    else: 
        listStore = sorted(listStore, key = lambda x : x[0], reverse = True)
    for i in range(len(listStore)):
        if i not in dictScore:
            dictScore[i] = articles[listStore[i][3]]
    dictScore = json.dumps(dictScore, ensure_ascii=False).encode('utf-8')
    dictScore = json.loads(dictScore)
    return dictScore
