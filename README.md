# Sorria Corpora word embeddings

This repository consists of preprocessing and evaluation scripts used in the paper entitled Sorria corpus: a Brazilian Portuguese corpus of colloquial language.

The preprocessing script cleaned corpora, tokenized and count tokens and types of a corpora in a pandas dataframe.
generate_model script generate the wordembeddings for the tokenized corpus obtained via preprocessing corpus.

Evaluation scripts can be used to measure the representativeness of a word embedding model.

Visualization is the scrip reponsible for all visualization of word embeddings, scatter plots via tsne and word clouds for the corpus

the preprocess_example.py is a example of the execution of preprocessing.py script

the .ipynb is the original Google Colab code with the outputs,  that originated the scripts presented here

Data directory contains the word embeddings

---

## Disclaimer
The JSON of our corpus will be available in the future

---

### Contents

* [Usage](#usage)
  * [Preprocessing ](#preprocessing)
  * [generate_model](#generate_model)

  * [Evaluation](#evaluation)
  * [Visualizations](#Visualizations)

---

## Usage
###  Preprocessing
For preprocessing a corpus, you will need to import the code to your own script, because it uses pandas dataframe for de preprocessing, for example of how to do that, see the preprocess_example.py

### generate model
For generate, you will need to import the code to your own script, because it uses the pre processing corpus that preprocessing scrpit returns.

this script only generates word2vec and fasttext, GloVe as their own script

### Evaluation
The evaluation is done through Syntactic and Semantic analogies evaluation then, if you are not importing the code, run it as follows:
```
python evaluate.py <model_type><model><analogies>

```
and for model_type parameter we have:

* glove &#8594; GloVe
* w2v &#8594; word2vec
* fasttext &#8594; Fast Text

e.g.
```
python evaluate.py w2v Data/embeddings/w2v_skip300.txt Data/analogies/analogies.txt
```
### Visualizations

```
python visualizations.py <word1,word2,word...><model_type><model>
```
eg:
```
experiências,amizades,amor,mãozinha w2v Data/embeddings/w2v_skip300.txt 
```
the wordcloud code needs to be imported for implemented, because they utilizes the pandas datafame  

