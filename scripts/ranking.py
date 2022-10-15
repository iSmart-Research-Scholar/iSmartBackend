import re
from gensim.parsing.preprocessing import remove_stopwords # this helps to remove the stop words
from nltk.stem import PorterStemmer
import requests  # for using API
import xml.etree.ElementTree as ET  # for parsing XML
import json


ps = PorterStemmer()
import json

def ranking(data, query, choosen):
    Articles = []
    totalRetrieved = data['total_records']
    totalSearched = data['total_searched']
    articles = data['articles']
    query = remove_stopwords(query).lower()
    listWords = query.split(' ')
    for index, word in enumerate(listWords):
        listWords[index] = word
    listStore = []
    dictIDFTitle = {}
    dictIDFWord = {}
    for i in range(len(articles)):
        title = articles[i]['title']
        abstract = ''
        if 'abstract' in articles[i]:
            abstract = articles[i]['abstract']
        title = ps.stem(remove_stopwords(title).lower())
        if 'abstract' in articles[i]:
            abstract = ps.stem(remove_stopwords(abstract).lower())
        for word in listWords:
            if title.count(word) > 0:
                if word not in dictIDFTitle:
                    dictIDFTitle[word] = 1
                else:
                    dictIDFTitle[word] += 1
            if abstract != '':
                if abstract.count(word) > 0:
                    if word not in dictIDFWord:
                        dictIDFWord[word] = 1
                    else:
                        dictIDFWord[word] += 1
    
    citationsWeight = 2

    for i in range(len(articles)):
        weight = 0
        title = articles[i]['title']
        if 'abstract' in articles[i]:
            abstract = articles[i]['abstract']
        citations = articles[i]['citing_paper_count']
        title = ps.stem(remove_stopwords(title).lower())
        abstract = ps.stem(remove_stopwords(abstract).lower())
        countTitle = 0
        countAbstract = 0
        for word in listWords:
            for titleWord in title:
                if titleWord.find(word) != -1:
                    countTitle += 1
            if 'abstract' in articles[i]:
                for abstractWord in abstract:
                    if abstractWord.find(word) != -1:
                        countAbstract += 1
            totalTitle = len(title.split(' '))
            if 'abstract' in articles[i]:
                totalAbstract = len(abstract.split(' '))
            if word in dictIDFTitle:
                weight += (totalRetrieved/(dictIDFTitle[word]+1)) * (countTitle/totalTitle)
            if word in dictIDFWord and 'abstract' in articles[i]:
                weight += (totalRetrieved/(dictIDFWord[word]+1)) * (countAbstract/totalAbstract)

        
        if 'index_terms' in articles[i] and 'ieee_terms' in articles[i]['index_terms']:
            indexTermsWeight = 3
            presentIndex = 0
            totalIndex = 0 
            listIndexTerms = articles[i]['index_terms']['ieee_terms']['terms']
            for term in listIndexTerms:
                term = remove_stopwords(term).lower()
                for wordTerm in term:
                    if ps.stem(wordTerm) in listWords:
                        presentIndex += 1
                    totalIndex += 1
            weight = weight + (presentIndex/totalIndex)*indexTermsWeight


        if 'index_terms' in articles[i] and 'author_tems' in articles[i]['index_terms']:
            authorTermsWeight = 2
            presentAuthor = 0
            totalAuthor = 0
            listAuthorTerms = articles[i]['index_terms']['author_terms']['terms']
            for term in listAuthorTerms:
                term = remove_stopwords(term).lower()
                for wordTerm in term:
                    if ps.stem(wordTerm) in listWords:
                        presentAuthor += 1
                    totalAuthor += 1
            weight = weight + (presentAuthor/totalAuthor)*authorTermsWeight
            
        weight = weight + citations*citationsWeight
        weight = round(weight, 2)

        if 'issn' in articles[i]:
            issn = articles[i]['issn']

            jsonObject = requests.get(f"https://api.elsevier.com/content/serial/title/issn/{issn}?apiKey=d719ef4dd2aa7050b35dfdf383582e75&field=SJR,SNIP&view=STANDARD")

            jsonObject = jsonObject.text
            result = json.loads(jsonObject)
            if 'serial-metadata-response' in result and 'entry' in result['serial-metadata-response'] and len(result['serial-metadata-response']['entry']) > 0 and 'SNIPList' in result['serial-metadata-response']['entry'][0] and 'SNIP' in result['serial-metadata-response']['entry'][0]['SNIPList'] and len(result['serial-metadata-response']['entry'][0]['SNIPList']['SNIP']) > 0 and '$' in result['serial-metadata-response']['entry'][0]['SNIPList']['SNIP'][0]:
                impactFactor = result['serial-metadata-response']['entry'][0]['SNIPList']['SNIP'][0]['$']
            else:
                impactFactor = 0
            
            if 'serial-metadata-response' in result and 'entry' in result['serial-metadata-response'] and len(result['serial-metadata-response']['entry']) > 0 and 'SJRList' in result['serial-metadata-response']['entry'][0] and 'SJR' in result['serial-metadata-response']['entry'][0]['SJRList'] and len(result['serial-metadata-response']['entry'][0]['SJRList']['SJR']) > 0 and '$' in result['serial-metadata-response']['entry'][0]['SJRList']['SJR'][0]:
                influenceScore = result['serial-metadata-response']['entry'][0]['SJRList']['SJR'][0]['$']
            else:
                influenceScore = 0

        else:
            impactFactor = 0
            influenceScore = 0
        
        listStore.append([weight, articles[i]['publication_year'], articles[i]['citing_paper_count'], i, impactFactor, influenceScore])

    if choosen == 1:
        listStore = sorted(listStore, key = lambda x:(x[1], x[0]), reverse=True)
    elif choosen == 2:
        listStore = sorted(listStore, key = lambda x:(x[1], x[0]), reverse=True)
    else: 
        listStore = sorted(listStore, key = lambda x : x[0], reverse = True)
    for i in range(len(listStore)):
        articles[listStore[i][3]]['impactFactor'] = listStore[i][4]
        articles[listStore[i][3]]['influenceScore'] = listStore[i][5]
        articles[listStore[i][3]]['rank'] = i+1
        Articles.append(articles[listStore[i][3]])
    return {'articles' : Articles}
