import numpy as np
import os
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# path=os.path.abspath('data.txt')
with open('preprocessing\data.txt','r',encoding='UTF-8') as f1:
    txt=f1.read()

def preprocess(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    text = text.lower()
    return text

def build_word_frequency(text):
    words = word_tokenize(text)
    st = set(stopwords.words('english'))
    words = [re.sub(r'[^\w]', '', word) for word in words]
    filtered = [word for word in words if word != '' and word not in st]
    lem = WordNetLemmatizer()
    lemmatized = [lem.lemmatize(word) for word in filtered]
    return Counter(lemmatized)

def rank_sentences(text, word_freq):
    sentences = sent_tokenize(text)
    st = set(stopwords.words('english'))
    lem = WordNetLemmatizer()
    sent_score = {}
    for i, s in enumerate(sentences):
        words_in_sent = word_tokenize(s)
        words_in_sent = [re.sub(r'[^\w]', '', word) for word in words_in_sent]
        words_in_sent = [word for word in words_in_sent if word != '' and word not in st]
        words_in_sent = [lem.lemmatize(word) for word in words_in_sent]
        if len(words_in_sent) == 0:
            continue
        score = (sum(word_freq[word] for word in words_in_sent)/ len(words_in_sent))
        sent_score[s] = (i, score)
    sent_score = sorted(sent_score.items(),key=lambda x: x[1][1],reverse=True)
    max_sent = math.ceil(len(sent_score) * 0.2)
    top_sent = []
    for s in sent_score:
        similar = False
        for chosen in top_sent:
            try:
                vectors = CountVectorizer().fit_transform([s[0], chosen[0]])
                similarity = cosine_similarity(vectors[0:1],vectors[1:2])[0][0]
            except ValueError:
                continue
            if similarity > 0.65:
                similar = True
                break
        if not similar:
            top_sent.append(s)

            if len(top_sent) == max_sent:
                break

    top_sent = sorted(
        top_sent,
        key=lambda x: x[1][0]
    )
    return top_sent

def generate_summary(text):
    text = preprocess(text)
    word_freq = build_word_frequency(text)
    top_sent = rank_sentences(text,word_freq)
    summary = ""
    for sentence in top_sent:
        summary += sentence[0].capitalize()
        summary += "\n"
    return summary