#!/home/luscaa/anaconda3/bin/python
import time
import nltk
from nltk.corpus import stopwords


nltk.download('punkt')
nltk.download('stopwords')


def token_count(df):
    '''
    Function to cont the tokens and types of our corpus or the sections of corpus 
    before de processing where some words will be removed
    '''
    initialtime = time.time()
    doc = ' '.join(df['section'].tolist())
    doc = ' '.join(df['title'].tolist())
    doc = ' '.join(df['text'].tolist())
    doc = nltk.word_tokenize(doc)


    print(f'Our corpus contains: {len(doc)} tokens ')
    print(f'Our corpus contains: {len(set(doc))} types')

    m,s = divmod(time.time() - initialtime, 60)
    print(f'Time spent: {m:.0f} minutes and {s:.0f} seconds')

def preprocessing(df, process):
    '''
    Function to remove stopwords(most common words), punctuation and 
    special characters. this function is also responsible for returning the tokenized corpus
    '''
    initialtime = time.time()
    special = ['!', '.', ',', ';', ':', '?', '*', '&', '%', '{', '}', '[', ']',
                 '<', '>', '(', ')', '...', '$', '-', '"', "'", '–']
    doc = ' '.join(df[process].tolist())
    doc = doc.lower()

    
    sentences = nltk.sent_tokenize(doc)
    doc = [nltk.word_tokenize(sentence) for sentence in sentences]
    for i in range(len(doc)):     
        doc[i] = [w for w in doc[i] if w  not  in special]
    for i in range(len(doc)):
        doc[i] = [w for w in doc[i] if w  not  in stopwords.words('portuguese')]

    m,s = divmod(time.time() - initialtime, 60)
    print(f'Time spent:{m:.0f} minutes and {s:.0f} seconds')
    return doc

