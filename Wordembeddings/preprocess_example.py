#!/home/luscaa/anaconda3/bin/python
import os
import pandas as pd
from itertools import chain
from preprocessing import *



actual_path = os.getcwd()
json_path =  actual_path +"/Data/JSON"
embedding_path =  actual_path +"/Data/embeddings/"

'''reading all the json, transforming each one into a dataframe,
 then concatenating them into one
'''
dfs = []
for file in os.listdir(json_path):
    if file.endswith("json"): 
        json = json_path + '/' + file
        print(file)
        data = pd.read_json(json)
        dfs.append(data)
df = pd.concat(dfs, ignore_index=True)

'''
Lower the section 'section' and 'title' for analisis
print the first columns and rows and check some infos of our dataframe
'''
df['section'] = df['section'].str.lower()
print('\nDataframe head: \n')
print(df.head())
print('\ndf info: \n')
print(df.info())
print('\ncheckin  how many itens is null: \n')
print(df.isna().sum())
'''
creating dataframe for each section of magazine for future analyze'''

amar = df.loc[df['section'] == 'amar']
aprender = df.loc[df['section'] == 'aprender']
brincar = df.loc[df['section'] == 'brincar']
roberta = df.loc[df['section'] == 'carta da roberta']
editor = df.loc[df['section'] == 'carta do editor']
comer = df.loc[df['section'] == 'comer']
como_faço = df.loc[df['section'] == 'como eu faço?']
como_vai = df.loc[df['section'] == 'como vai você?']
conhecer = df.loc[df['section'] == 'conhecer']
conviver = df.loc[df['section'] == 'conviver']
crescer = df.loc[df['section'] == 'crescer']
cuidar = df.loc[df['section'] == 'cuidar']
descobrir = df.loc[df['section'] == 'descobrir']
dia_util = df.loc[df['section'] == 'dia útil']
editorial = df.loc[df['section'] == 'editorial']
educar = df.loc[df['section'] == 'educar']
envolver = df.loc[df['section'] == 'envolver']
gente_faz = df.loc[df['section'] == 'gente que faz']
lugar_comum = df.loc[df['section'] == 'lugar em comum']
manual = df.loc[df['section'] == 'manual prático']
movimentar = df.loc[df['section'] == 'movimentar']
nota = df.loc[df['section'] == 'nota 10']
prazeres = df.loc[df['section'] == 'prazeres simples']
proteger = df.loc[df['section'] == 'proteger']
trabalhar = df.loc[df['section'] == 'trabalhar']
mesa = df.loc[df['section'] == 'tá na mesa']
valores = df.loc[df['section'] == 'valores essenciais']
viajar = df.loc[df['section'] == 'viajar']
mudar = df.loc[df['section'] == 'dá pra mudar?']
acao = df.loc[df['section'] == 'ação e diversão']

''' Start the preprocessing whit the functions avaliable in preprocessing.py'''

print('\n')
print(token_count(df))

token_count(amar)
token_count(aprender)
token_count(brincar)
token_count(roberta)
token_count(editor)
token_count(comer)
token_count(como_faço)
token_count(como_vai)
token_count(conhecer)
token_count(conviver)
token_count(crescer)
token_count(cuidar)
token_count(descobrir)
token_count(dia_util)
token_count(editorial)
token_count(educar)
token_count(envolver)
token_count(gente_faz)
token_count(lugar_comum)
token_count(manual)
token_count(movimentar)
token_count(nota)
token_count(prazeres)
token_count(proteger)
token_count(trabalhar)
token_count(mesa)
token_count(valores)
token_count(viajar)
token_count(mudar)
token_count(acao)


print('\n part of text before processing: \n')
print(df.text)

'''
in the first line of the code sequence we preprocess the "text" section 
while in the next two we preprocess the "title" section and merge it with 
what we had before just from the "text" section
'''
doc = preprocessing(df, 'text')
doc2 = preprocessing(df, 'title')
doc = [*doc, *doc2]
print('\n part of corpus post-processing: ')
print(doc[0:10])

'''
getin tokens and types of processed corpus:
'''
flatten_doc =  list(chain.from_iterable(doc))

print(f'\ntokens of processed corpus: {len(flatten_doc)}')
print(f'types of processed corpus: {len(set(flatten_doc))}')

