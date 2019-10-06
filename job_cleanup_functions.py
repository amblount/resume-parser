import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import gensim
import re
import os
from bs4 import BeautifulSoup

#nltk.download('punkt')

def fix_numbers(x):

    for i in range(1,26):
        replace = str(i) + '\+|' + str(i) + "\s\+"
        replace2 = str(i)

        reok

def clean_html(strings):
    new_strings = BeautifulSoup(strings, 'html.parser').get_text()
    return(new_strings)

def split_skills(row, column):
    new_val = row[column]

    new_val = re.sub('●', '', new_val)
    new_val = re.sub(r'\n', ' ', new_val)

    text_split = new_val.split('<p> | <li>')
    list_strings = [clean_html(x) for x in text_split]
    list_strings = [x for x in list_strings]

    list_strings = " ".join(list_strings).strip()

    list_strings = re.sub(r'http\S+', ' ', list_strings, flags=re.MULTILINE)
    list_strings = re.sub("-", " ", list_strings)
    list_strings = re.sub("d3.js", "dthree.js", list_strings)
    list_strings = re.sub(re.escape("c++"), "cplusplus", list_strings)
    list_strings = re.sub(re.escape("c#"), "csharp", list_strings)
    list_strings = re.sub(re.escape(".net"), "dotnet", list_strings)
    list_strings = re.sub("java 8", "java eight", list_strings)
    list_strings = re.sub("python 3", "python three", list_strings)
    list_strings = re.sub("python 2", "python two", list_strings)
    list_strings = re.sub(r"\&", "and", list_strings)
    list_strings = re.sub(r"\\", "", list_strings)
    list_strings = re.sub(r"\/", "", list_strings)

    return(list_strings)

def clean_text(row, column):

    new_val = row[column]

    list_strings = nltk.sent_tokenize(new_val)
    #list_strings = [x for x in list_strings]
    list_strings = " ".join(list_strings).strip()

    list_strings = re.sub(r'[^a-zA-Z\.]', ' ', list_strings)

    if not (list_strings.endswith('.')):
        list_strings = list_strings + '.'

    list_strings = list_strings.strip()

    return(list_strings)
