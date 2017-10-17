"""A script for reading in and cleaning the dataset."""

import re
import string
import pickle
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.datasets import fetch_20newsgroups


def get_articles():
    FN0 = 'tokens'
    with open('data/%s.pkl'%FN0, 'rb') as fp:
        heads, desc, keywords = pickle.load(fp) # keywords are not used in this project
    return heads, desc

def grab_body_headline(article):
    """Grab the headline and body text from the inputted article text. 

    The article is one long string, and the parts to grab are stored within certain
    fields, denoted by the name of the field followed by a colon ("Subject:" for 
    the headline, "Lines:" for the body). 

    Args: 
    ----
        article: str

    Return: 
    ------
        (body, headline): tuple of strings
            Returns (None, None) if no body and/or headline is found. 
    """

    found_headline = re.findall("(?<=Subject:)(.*)", article)
    found_body = re.findall("(?<=Lines:)(?s)(.*)", article)

    # For 58 of the 18,846 articles in the data, no headline and/or body was found.  
    if found_headline and found_body: 
        headline = found_headline[0]
        body = found_body[0]
        return (body, headline)
    else: 
        # Return (None, None) to allow continuation of the pipline, and filter later.
        return (None, None)
    
def clean_raw_txt(body, headline, punct_remove=False, stopwrds_remove=False): 
    """Clean the body and headline to remove punctuation, stopwords, etc.

    Args: 
    ----
        body: str
        headline: str
        punct_dct (optional): dict 
            Translation dict resulting from a `str.maketrans()` call             
        stopwords_set (optional): set  

    Return: 
    ------
        (body, headline): tuple
    """
    punct_dct = str.maketrans({punct_mark: "" for punct_mark in string.punctuation})
    stopwrds_set = set(stopwords.words('english'))
    
    if punct_remove: 
        body = body.translate(punct_dct)
        headline = headline.translate(punct_dct)

    body_wrds = word_tokenize(body)
    headline_wrds = word_tokenize(headline)

    stopwrds_set = stopwrds_set if stopwrds_remove else set()

    body_wrds = [wrd.lower() for wrd in body_wrds if wrd.lower() not in stopwrds_set] 
    headline_wrds = [wrd.lower() for wrd in headline_wrds if wrd.lower() not in stopwrds_set]

    return (body_wrds, headline_wrds)

if __name__ == '__main__': 
    cats = ['alt.atheism',
 'comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x',
 'misc.forsale',
 'rec.autos',
 'rec.motorcycles',
 'rec.sport.baseball',
 'rec.sport.hockey',
 'sci.crypt',
 'sci.electronics',
 'sci.med',
 'sci.space',
 'soc.religion.christian',
 'talk.politics.guns',
 'talk.politics.mideast',
 'talk.politics.misc',
 'talk.religion.misc']
    #articles = fetch_20newsgroups(subset='all', categories=['rec.autos', 'comp.graphics']).data
    #bodies_n_headlines = [grab_body_headline(article) for article in articles]
    heads, desc = get_articles()
    
    punct_dct = str.maketrans({punct_mark: "" for punct_mark in string.punctuation})
    stopwrds_set = set(stopwords.words('english'))
    
    cleaned_bodies = []
    cleaned_headlines = []
    for i, txt in enumerate(heads): 
        if heads[i] and desc[i]: 
            body, headline = clean_raw_txt(desc[i], heads[i], punct_dct, stopwrds_set)
            cleaned_bodies.append(body)
            cleaned_headlines.append(headline)
    
    body_fp = 'data/bodies.pkl'
    headline_fp = 'data/headlines.pkl'

    with open(body_fp, 'wb+') as f: 
        pickle.dump(cleaned_bodies, f)
    with open(headline_fp, 'wb+') as f: 
        pickle.dump(cleaned_headlines, f)
