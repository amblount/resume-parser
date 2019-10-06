import pandas as pd
import logging
import string
import json
import re
import bs4

import nltk
from nltk import (
    ne_chunk, 
    pos_tag, 
    word_tokenize
)
from nltk.corpus import stopwords
from nltk.tree import Tree

SO_TAGS_REMOVE = [
    "CLICK",
    "SEARCH",
    "KEY",
    "TIME",
    "RESPONSE",
    "SUBMIT",
    "APPLY",
    "OBJECT",
    "GLOBAL",
    "BUILD",
    "UNION",
    "JERSEY",
    "ACTION",
    "THIS",
    "SIZE",
    "AUDIO",
    "MONITORING",
    "TITLE",
    "PRIVATE",
    "DIVISION",
    "EXPECT",
    "VIEW",
    "FIXED",
    "MEMBER",
    "STORE",
    "PRODUCT",
    "ENVIRONMENT",
    "SCHEDULE",
    "NEXT",
    "DEVISE",
    "SEND",
    "DATE",
    "SELECT",
    "CALCULATOR",
    "POINT",
    "CREDENTIALS",
    "PROJECT",
    "RELEASE",
    "ACCESS",
    "HOST",
    "DIAGRAM",
    "MAX",
    "MIN",
    "SERIES",
    "PROCESSING",
    "PUBLIC",
    "ENDPOINT",
    "PRODUCTION",
    "ACCOUNT",
    "RANKING",
    "RANK",
    "MATCH",
    "SET",
    "INSTALL",
    "ADMIN",
    "NOTIFICATIONS",
    "CONTACT",
    "PERFORMANCE",
    "TESTING",
    "SCALE",
    "DOCUMENTATION",
    "USING",
    "MODELS",
    "JOIN",
    "METHODS",
    "STACK",
    "ORIENTATION",
    "TABS",
    "FIELD",
    "SCREEN",
    "COM",
    "EXPRESSION",
    "DRAW",
    "POSITION",
    "TRANSPARENCY",
    "REPORT",
    "FOCUS",
    "CONTAINERS",
    "PROTOTYPE",
    "COMPONENTS",
    "BACKGROUND",
    "CLIENT",
    "SERVICE",
    "TRANSFORM",
    "PROCESS",
    "INCLUDE",
    "COMMAND",
    "DIRECTORY",
    "LESS",
    "REPORTING",
    "EVENTS",
    "CENTER",
    "PATH",
    "WHERE",
    "SHARE",
    "TASK",
    "STATE",
    "POST",
    "LIST",
    "DIFF",
    "EACH",
    "UNIQUE",
    "LOADING",
    "UPDATES",
    "RESOURCES",
    "INTEGRATION",
    "SYSTEM",
    "RETURN",
    "INPUT",
    "COPY",
    "SCOPE",
    "STREAMING",
    "SCRIPTING",
    "ARCHITECTURE",
    "FRAMEWORKS",
    "DYNAMIC",
    "LAYOUT",
    "RESPONSIVE",
    "MODULE",
    "MAPS",
    "CELL",
    "CONNECTION",
    "LOCATION",
    "ATTRIBUTES",
    "VERSION",
    "LOGGING",
    "AUTHENTICATION",
    "CLASS",
    "ACCESSIBILITY"
]

SO_TAGS_AGG = [
    "AWS",
    "REACT",
    "KAFKA",
    "POSTGRES",
    "INTELLIJ",
    "UI",
    "UX",
    "BABEL",
    "EMBER",
    "BACKBONE",
    "ES6",
    "KARMA",
    "DATAFLOW",
    "BIGQUERY",
    "VUE",
    "MONGO",
    "EC2"
]

def remove_html_tags(text):
    clean_text = bs4.BeautifulSoup(
        text, 'html.parser'
    ).get_text()
    
    return clean_text

def clean_text(text):
    new_val = re.sub('-', '', text)
    
    text_split = new_val.split('<p>')
    list_strings = [remove_html_tags(x) for x in text_split]
    list_strings = [x for x in list_strings]

    list_strings = "".join(list_strings).strip()

    return list_strings

def preprocess_stackoverflow_tags(tags, min_count):
    """ Preprocesses stackoverflow tags taken from:
            https://data.stackexchange.com/stackoverflow/query/new
        using the query:
        
            Select TagName, [Count]
            From Tags
            Order By Count Desc;
    """
    
    # Remove 
    for tag in SO_TAGS_REMOVE:
        tags = tags[tags.TagName != tag]
        
    count_names = []
    for tag in SO_TAGS_AGG:
        count_names.append(
            tags[tags.TagName.str.contains(tag)][
                "Count"
            ].sum()
        )
    
    tags = pd.concat([
        tags,
        pd.DataFrame(
            {"TagName": SO_TAGS_AGG, "Count": count_names}
        )
    ])
    
    tags.TagName = tags.TagName.apply(
        lambda x: x.replace('.', '')
    )
    tags = tags[tags.Count > min_count]
    
    return tags


def get_stackoverflow_tags_from_text(text, tags):   
    """ Return list of stackoverflow tags found in the input string.
    
    Parameters
    ----------
    text : str
        Text containing job description or resume information
    tags : pandas dataframe
        Contains list of stackoverflow tags
        
    Returns
    ----------
    str
        List of stackoverflow tags ordered by popularity (i.e. Count)
    """
    
    # Remove HTML Tags
    entities = get_continuous_pos_chunks(text)
    
    # Replace sequence words (and, or) with commas
    for word in [' and', ' or', ' ,', '\\', "/"]:
        text = text.replace(word, ', ')
        
    # Remove punctuations
    punctuations = "".join(
        list(
            set(string.punctuation) - set(["#", "+", "-", ".", ","])
        )
    )
    text = " ".join([
        token.translate(
            str.maketrans(" ", " ", punctuations)
        )
        for token in text.split()
    ])
    
    # Get all words that are either in uppercase or part of a sequence 
    entities.extend([
        token.replace(',', '').replace('.', '')
        for token in text.split()
        if token[0].isupper() or ',' in token
    ])
    
    # Convert all unique entities to uppercase 
    entities = [
        entity.upper() for entity in list(set(entities))
    ]

    # Remove stopwords and replace spaces with dashes
    tokens = [
        token.replace(" ", "-")
        for token in entities
        if token not in stopwords.words("english")
    ]
    
    # Get intersection bet. stackoverflow tags and extracted entities
    token_tags = set.intersection(
        set(tokens), set(tags.TagName.values)
    )
    
    # Get the corresponding count per tag
    token_tags = [(
        token_tag,
        tags[tags.TagName == token_tag].Count.values[0],
    )
    for token_tag in token_tags
    ]
    
    return (
        sorted(
            token_tags, key=lambda x: x[1], reverse=True
        )
    )


def get_continuous_pos_chunks(text):
    """
    Code for getting continuous POS chunks: 
        https://stackoverflow.com/a/24410967/4777141
    """
    
    chunked = ne_chunk(
        pos_tag(word_tokenize(text))
    )
    
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(
                " ".join(
                    [token for token, pos in i.leaves()]
                )
            )
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    if continuous_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            continuous_chunk.append(named_entity)
    
    return continuous_chunk
