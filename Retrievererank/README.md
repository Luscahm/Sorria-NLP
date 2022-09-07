# Sorria Retrieve & Re-rank

---

## DISCLAIMER
Código original utilizado no google Colab: https://colab.research.google.com/drive/1F4NY1afXN0DVMgWvNeHcivB1oy-O155i?authuser=1#scrollTo=eg-mS4IG2TXi


Original code in google colab: https://colab.research.google.com/drive/1F4NY1afXN0DVMgWvNeHcivB1oy-O155i?authuser=1#scrollTo=eg-mS4IG2TXi

## Contents
- [Sorria Retrieve & Re-rank](#sorria-retrieve--re-rank)
  - [DISCLAIMER](#disclaimer)
  - [Contents](#contents)
  - [Usage](#usage)
    - [Query](#query)
    - [Salvar corpus e embedding](#salvar-corpus-e-embedding)
    - [Query](#query-1)
    - [Save corpus and embeddings](#save-corpus-and-embeddings)

---

## Usage
###  Query
Aqui temos o exato código utilizado para gerar todas os modelos e testar-los.
Para testar alguma modelo primeiramente é necessario  executar a célular com a função BM25 e a celula com a função search, pois são ambas que irão realizar as buscas.

Por termos varios modelos é necessario que para a busca funcionar rode apenas  a celula daquela que deseja utilar, no nosso caso a que se saiu melhor encontra-se dentro da seção  bertimbau + cross-encoder/ms-marco-MiniLM-L-6-v2

Após executar a celular que ira realizar o treinamento desse retrieve & re-rank   , ja temos algumas pesquisas realizadas utilizando eles, para realizar outras basta criar uma célula de código com o seguinte código, substituindo o sua query pela query que deseja
```
search(query = "Sua query")
```

### Salvar corpus e embedding
Para salvar o corpus e a embedding do corpus para utilzar na interface, é necessario tomar o mesmo cuidado que o tomado na query, de executar por ultimo a célula do Retrieve&Re-rank que deseja-se salvar, no nosso caso é o que está na seção bertimbau + cross-encoder/ms-marco-MiniLM-L-6-v2

Após isso basta executar o código do pickle que o mesmo salvara o corpus_embedding.pkl e o corpus.pkl dentro da raiz do projeto, e será necessario mover-lo caso queira utilizar na interface Web
### Query
Here we have the exact code used to generate all models and test them.
To test any model it is first necessary to run the cell with the BM25 function and the cell with the search function, because they are both the ones that will perform the searches.

Because we have several models, it is necessary for the search to run only the cell you want to use, in our case the one that worked best is in the section bertimbau + cross-encoder/ms-marco-MiniLM-L-6-v2

After running the cell that will train this retrieve & re-rank, we already have some searches performed using them, to perform others just create a code cell with the following code, replacing your query with the query you want
```
search(query = "Your query")
```

### Save corpus and embeddings

To save the corpus and the embedding corpus to be used in the interface, you must take the same care as you did with the query, to execute last the Retrieve&Re-rank cell that you want to save, in our case it's the one in the bertimbau + cross-encoder/ms-marco-MiniLM-L-6-v2 section

After that, just execute the pickle code and it will save the corpus_embedding.pkl and the corpus.pkl inside the project's root, and it will be necessary to move it if you want to use in the web  interface 

