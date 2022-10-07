# importing json so to use it to open the json file which we got from the
import json
import pathlib
import os
from gensim.parsing.preprocessing import remove_stopwords # this helps to remove the stop words
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
def ranking(data, query):
    block_size = 100

    # Creating the temporary files and storing the data in the temporary files after storing them in the temporary files
    # later I will merge them into one file which will be used for the ranking the documents    
    
    currentBlock = 0
    
    curr_dir = pathlib.Path(__file__).parent.resolve()
    
    directory = "TextFiles"
    
    path = os.path.join(curr_dir, directory)
    os.mkdir(path)
    
    total_retrieved = data['total_records']
    total_search = data["total_searched"]
    
    currentFile = 1
    articles = data['articles']
    
    for i in range(len(articles)):
        title = articles[i]['title']
        abstract = articles[i]['abstract']
        citations = articles[i]['citing_paper_count']
        articleNumber = articles[i]['article_number']
        publicationYear = articles[i]['publication_year']
        pdfUrl = articles[i]['pdf_url']
        fileName = path + f"/file{currentFile}.txt"
        with open(fileName, "a") as f:
            f.write(title + "\n")
            f.write("@" + "\n")
            f.write(abstract + "\n")
            f.write("#" + "\n")
            f.write(str(citations) + "\n")
            f.write("$" + "\n")
            f.write(str(articleNumber)+"\n")
            f.write("^" + "\n")
            f.write(str(publicationYear)+"\n")
            f.write("&" + "\n")
            f.write(pdfUrl + "\n")
            f.write("---" + "\n")
            currentBlock += 1
        if currentBlock == block_size-1:
            currentBlock = 0
            fileName += 1
    
    with open(path + "/merged.txt", 'w') as f:
        for i in range(1, currentFile + 1):
            with open(path + f"/file{i}.txt", 'r') as file:
                for line in file:
                    f.write(line)
            os.remove(path + f"/file{i}.txt")

    dictStore = {}
    prev = ''
    current = ''
    listIs = []
    currentId = 0
    with open("D:/Hackathons/Backend/iSmartBackend/scripts/TextFiles/merged.txt", 'r') as f:
        for line in f:
            prev = line
            prev = prev.replace('\n','')
            prev = prev.strip()
            if prev == '---':
                currentId += 1
                dictStore[currentId] = listIs
                listIs = []
            elif prev == '@' or prev == '#' or prev == '$' or prev == '&' or prev == '^':
                listIs.append(ps.stem(remove_stopwords(current)).lower())
                current = ''
            else:
                if(line.endswith('\n')):
                    line = line[:-1]
                current = current + line

    # Defining the weights to incorporate the values

    titleWeight = 0.3
    abstractWeight = 0.4
    citationsWeight = 0.1
    dictWeightId = {}

    query = ps.stem(remove_stopwords(query)).lower()
    listWords = query.split(' ')

    for keyVal in dictStore:
        weight = 0
        titleIs = dictStore[keyVal][0]
        abstractIs = dictStore[keyVal][1]
        citationsIs = int(dictStore[keyVal][2])
        year = int(dictStore[keyVal][4])/1000
        countInTitleWords = []
        countInAbstractWords = []
        for word in listWords:
            countInTitle = titleIs.count(word)
            countInAbstract = abstractIs.count(word)
            countInTitleWords.append(countInTitle)
            countInAbstractWords.append(countInAbstract)
            weight += countInTitle*titleWeight + countInAbstract*abstractWeight
        dictWeightId[keyVal] = [weight+year+citationsIs*citationsWeight, dictStore[keyVal][3], countInTitle, countInAbstract, countInTitleWords, countInAbstractWords]


    dictWeightId = dict(sorted(dictWeightId.items(), key = lambda x:(x[1][0], x[0]), reverse = True))

    print(dictWeightId)

    os.remove(path + "/merged.txt")
    os.rmdir(path)