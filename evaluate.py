from gensim.models import KeyedVectors
from gensim.models.fasttext import  load_facebook_model
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec
import sys

'''
on execution please provide the following information formatted as requested 
and in the order requested:
model_type model_path analogies_path

eg: w2v Data/embeddings/w2v_skip300.txt Data/analogies/analogies.txt
'''


def return_tuples(analogy, vocab):
    incorrect = []
    notfound = []
    correct= [analogy[1][i]['correct'][j] for i in range(len(analogy[1])) for j in range(len(analogy[1][i]['correct']))]
    score = analogy[0] * 100
    for i in range(len(analogy[1])):
        for k in range(len(analogy[1][i]['incorrect'])):
            if (analogy[1][i]['incorrect'][k][0].lower() not in vocab or analogy[1][i]['incorrect'][k][1].lower()  not in vocab or 
                analogy[1][i]['incorrect'][k][2].lower() not in vocab):
                 notfound.append(analogy[1][i]['incorrect'][k])
            else:
                incorrect.append(analogy[1][i]['incorrect'][k])

    return score, correct, incorrect, notfound


def print_infos(score, correct, incorrect, notfound, vocab):
    
    print(f'For this wordembedding we have the following statistics ')
    print(f'Total words: {len(vocab)}')
    print(f'Score: {score}')
    print(f'Correct words: {len(correct)}')
    print(f'Missing words: {len(notfound)}')
    print(f'Incorrect words: {len(incorrect)}')



def scores(types, directory_model,directory_analogies):
    if types == 'glove':
        glove_file = datapath(directory_model)
        tmp_file = get_tmpfile("glove_word2vec.txt")
        _ = glove2word2vec(glove_file, tmp_file)
        model = KeyedVectors.load_word2vec_format(tmp_file)
        vocab = list(model.index_to_key)
        scores = model.evaluate_word_analogies(directory_analogies, dummy4unknown=False)

    elif types == 'w2v':
        model = KeyedVectors.load_word2vec_format(directory_model,
                                          binary=False,unicode_errors='ignore')
        vocab = list(model.index_to_key)
        scores = model.evaluate_word_analogies(directory_analogies, dummy4unknown=False)

    elif types == 'fasttext':
        model = load_facebook_model(directory_model)
        vocab = list(model.wv.index_to_key)
        scores = model.wv.evaluate_word_analogies(directory_analogies, dummy4unknown=False)
    else:
        print('insira o tipo correto')
        print('glove:  GloVe')
        print('w2v: Word2Vec')
        print('fasttext: FastText')

    score, correct, incorrect, notfound = return_tuples(scores, vocab)
    print_infos(score, correct, incorrect, notfound, vocab)

if __name__ == 'main':
    model_type = sys.argv[1]
    model_path = sys.argv[2]
    analogies = sys.argv[3]
    scores(model_type, model_path, analogies)
