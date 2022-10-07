import requests,re
from scripts import ranking

class searcher:
    def __urlify(self,s):
    
        # Remove all non-word characters (everything except numbers and letters)
        s = re.sub(r"[^\w\s]", '', s)
    
        # Replace all runs of whitespace with a single dash
        s = re.sub(r"\s+", '+', s)
    
        return s

    def searchIEEE(self,query='',title='',author=''):
        apiKey='9vqueb4y34a36354ghwfjjavNivas'
        querytosend = query
        title=self.__urlify(title)
        author=self.__urlify(author)
        query=self.__urlify(query)
        link=f'http://ieeexploreapi.ieee.org/api/v1/search/articles?apikey={apiKey}&format=json&max_records=200&start_record=1&sort_order=asc&sort_field=article_number&querytext={query}&article_title={title}&author={author}'
        result=requests.get(link)
        ranking.ranking(querytosend)
# # Prints: I-cant-get-no-satisfaction"
#     print(urlify("I can't get no satisfaction!"))