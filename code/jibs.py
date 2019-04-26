import requests
from scrapy import Selector

def get_keywords_abstract(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Connection error: {}".format(url))
        return "", ""
    selector = Selector(text=r.text) 
    keywords = selector.css('.Keyword::text').extract()
    abstracts = selector.css('#Abs1 p::text').extract()
    abstract = ''.join(abstracts)
    return keywords, abstract

#test_url = 'https://link.springer.com/article/10.1057%2Fs41267-019-00235-7'
#keywords, abstract = get_keywords_abstract(test_url)
#print(keywords)
#print(abstract)

import pandas as pd

articles = pd.read_csv('../data/jibs_articles.csv', sep=',')
type(articles) # <class 'pandas.core.frame.DataFrame'>
articles.shape # (442, 10)
articles.columns # 列名
articles.head() # 打印前5行

urls = articles['URL']
keywords = pd.Series(index=articles.index)
abstract = pd.Series(index=articles.index)
for i, url in enumerate(urls):
    keywords[i], abstract[i] = get_keywords_abstract(url)
    print("Finish article: {}".format(i))

articles['keywords'] = keywords
articles['abstract'] = abstract
articles.columns # 数据表中增加了keywords和abstract两列
articles.to_csv('../data/jibs_keywords_abstract.csv', sep=',', header=True)

import pickle
with open("../data/articles.pickle", "wb") as f:
    pickle.dump(articles, f)