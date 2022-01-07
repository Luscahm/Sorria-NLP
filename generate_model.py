#!/home/luscaa/anaconda3/bin/python
import time
from gensim.models import Word2Vec, FastText
from gensim.models.fasttext import save_facebook_model


def w2v(doc, embedding_path):
    '''
    Function to generate our word2vec model via gensim
    '''
    dims = [50, 100, 300, 600, 1000]
    print(f'Generating word2vec Skip-Gram with dimensions 50, 100, 300, 600 and 1000')
    for i in dims:
        initialtime = time.time()
        w2v_skip = Word2Vec(doc,min_count=1, vector_size=i, sg=1 )
        temp_path = embedding_path + 'w2vskip' +str(i)+'.txt'
        w2v_skip.wv.save_word2vec_format(temp_path, binary = False)
        m,s = divmod(time.time() - initialtime, 60)
        print(f'Time spent:{m:.0f} minutes and {s:.0f} seconds')
   
    print(f'Generating word2vec CBOW with dimensions 50, 100, 300, 600 and 1000') 
    for i in dims:
        initialtime = time.time()
        w2v_cbow = Word2Vec(doc,min_count=1, vector_size=i, sg=0 )
        temp_path = embedding_path + 'w2vcbow' +str(i)+'.txt'
        w2v_cbow.wv.save_word2vec_format(temp_path, binary = False)
        m,s = divmod(time.time() - initialtime, 60)
        print(f'Time spent:{m:.0f} minutes and {s:.0f} seconds')

def fst(doc, embedding_path):
    '''
    Function to generate our FastText model via gensim
    '''
    dims = [50, 100, 300, 600, 1000]
    print(f'Generating FastText Skip-Gram with dimensions 50, 100, 300, 600 and 1000')
    for i in dims:
        initialtime = time.time()
        fst_skip = FastText(doc,min_count=1, vector_size=i, sg=1 )
        temp_path = embedding_path + 'fstskip' +str(i)+'.bin'
        save_facebook_model(fst_skip, 'temp_path')
        m,s = divmod(time.time() - initialtime, 60)
        print(f'Time spent:{m:.0f} minutes and {s:.0f} seconds')
   
    print(f'Generating FastText CBOW with dimensions 50, 100, 300, 600 and 1000') 
    for i in dims:
        initialtime = time.time()
        fst_bow = FastText(doc,min_count=1, vector_size=i, sg=0 )
        temp_path = embedding_path + 'fstcbow' +str(i)+'.bin'
        save_facebook_model(fst_bow, 'temp_path')
        fst_bow.wv.save_word2vec_format(temp_path, binary = False)
        m,s = divmod(time.time() - initialtime, 60)
        print(f'Time spent:{m:.0f} minutes and {s:.0f} seconds')