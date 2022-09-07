#!/home/luscaa/anaconda3/bin/python
import sys
import numpy as np
import plotly.graph_objects as go
from gensim.models import KeyedVectors
from gensim.models.fasttext import  load_facebook_model
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from plotly.graph_objs import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

'''
on execution if not import please provide the following information formatted as requested 
and in the order requested:
word1,word2,word3... model_type model_path

eg: experiências,amizades,amor,mãozinha word2vec Data/embeddings/w2v_skip300.txt 
'''


def loading(directory_model, types):
    '''
    loading model  with information provided
    '''
    if types == 'glove':
        glove_file = datapath(directory_model)
        tmp_file = get_tmpfile("glove_word2vec.txt")
        _ = glove2word2vec(glove_file, tmp_file)
        model = KeyedVectors.load_word2vec_format(tmp_file)
        return model


    elif types == 'w2v':
        model = KeyedVectors.load_word2vec_format(directory_model,
                                          binary=False,unicode_errors='ignore')
        return model

    elif types == 'fasttext':
        model = load_facebook_model(directory_model)
        return model


    else:
        print('enter the correct type: ')
        print('glove:  GloVe')
        print('w2v: Word2Vec')
        print('fasttext: FastText')
    


def neighbours(directory_model, words, types):
    '''
    get nearest neighbours of model
    '''
    model = loading(directory_model, types)
    if types == 'glove' or types == 'w2v':
        for word in words:
            print(f'\nnearest neighbours for {word}:')
            print(model.most_similar(word))       


    elif types == 'fasttext':
        for word in words:
            print(f'\nnearest neighbours for {word}:')
            print(model.wv.most_similar(word))

    else:
        print('enter the correct type: ')
        print('glove:  GloVe')
        print('w2v: Word2Vec')
        print('fasttext: FastText')



def append_list(sim_words, words):
    
    list_of_words = []
    
    for i in range(len(sim_words)):
        
        sim_words_list = list(sim_words[i])
        sim_words_list.append(words)
        sim_words_tuple = tuple(sim_words_list)
        list_of_words.append(sim_words_tuple)
        
    return list_of_words

def preparing_data(model, words):
    result_word = []
    for word in words:    
        sim_words = model.most_similar(word, topn = 5)
        sim_words = append_list(sim_words, word)
            
        result_word.extend(sim_words)
    
    similar_word = [word[0] for word in result_word]
    similarity = [word[1] for word in result_word] 
    similar_word.extend(words)
    labels = [word[2] for word in result_word]
    label_dict = dict([(y,x+1) for x,y in enumerate(set(labels))])
    color_map = [label_dict[x] for x in labels]
    return similar_word, similarity, labels, label_dict, color_map

def display_tsne_scatterplot(directory_model, types, user_input=None, topn=5, sample=10):

    model = loading(directory_model, types)
    words, similarity, label, label_dict, color_map = preparing_data(model, user_input) 
    word_vectors = np.array([model[w] for w in words])
    


    two_dim = TSNE(n_components = 2, random_state=0, perplexity = 5, learning_rate = 500, n_iter = 10000).fit_transform(word_vectors)[:,:2]

    data = []


    count = 0
    for i in range (len(user_input)):

                trace = go.Scatter(
                    x = two_dim[count:count+topn,0], 
                    y = two_dim[count:count+topn,1],  
                    text = words[count:count+topn],
                    name = user_input[i],
                    textposition = "top center",
                    textfont_size = 20,
                    mode = 'markers+text',
                    marker = {
                        'size': 10,
                        'opacity': 0.8,
                        'color': 2
                    }
       
                )
                
            
                data.append(trace)
                count = count+topn

    trace_input = go.Scatter(
                    x = two_dim[count:,0], 
                    y = two_dim[count:,1],  
                    text = words[count:],
                    name = 'Selected terms',
                    textposition = "top center",
                    textfont_size = 20,
                    mode = 'markers+text',
                    marker = {
                        'size': 10,
                        'opacity': 1,
                        'color': 'black'
                    }
                    )
            
    data.append(trace_input)
    
# Configure the layout
    titulo = "tSNE projection for " + types + " Nearest Neighbors selected words"

    layout = go.Layout(
        title = titulo,
        margin = {'l': 0, 'r': 0, 'b': 0, 't': 30},
        showlegend=False,
        #autosize = True
        width = 750,
        height = 750
        )

    plot_figure = go.Figure(data = data, layout = layout)
    plot_figure.show()

def wordcloud(df):
    special = ['!', '.', ',', ';', ':', '?', '*', '&', '%', '{', '}', '[', ']',
                 '<', '>', '(', ')', '...', '$', '-', '"', "'", '–']
    text = df['title'] + ' ' + df['text'] 
    text = ' '.join(text)
    text = text.lower()
    for word in stopwords.words('portuguese'):
        text = text.replace(" "+ word + " ", " ")
    for especial in special:
        text = text.replace(especial + " ", " ")
    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(text)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


if __name__ == 'main':
    words = list(sys.argv[1].split(','))
    model_type = sys.argv[2]
    model_path = sys.argv[3]
    neighbours(model_path, words, model_type)
    display_tsne_scatterplot(model_path,model_type,words)