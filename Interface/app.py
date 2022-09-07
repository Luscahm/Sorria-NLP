import pickle
import io                                                                                                                                                                                                                                                                                                                                                                                                   
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder, util
from flask import render_template, request, Flask

CROSS_PATH = 'data/cross.pkl'
CORPUS_PATH = 'data/corpus.pkl'
EMBEDDING_PATH = 'data/corpus_embedding.pkl'

TOP_K = 50


class CPU_Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else:
            return super().find_class(module, name)


def load_archives():
    file = open(CORPUS_PATH, 'rb')
    corpus = pickle.load(file)
    bi_encoder = SentenceTransformer('neuralmind/bert-large-portuguese-cased')
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    file = open(EMBEDDING_PATH, 'rb')
    corpus_embeddings = CPU_Unpickler(file).load()
    return corpus, bi_encoder, cross_encoder, corpus_embeddings



def search(query):
    result = []
    print(query)
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True, device='cpu')
    hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=TOP_K)
    hits = hits[0]  # Get the hits for the first query
    ##### Re-Ranking #####
    # Now, score all retrieved corpus with the cross_encoder
    cross_inp = [[query, corpus[hit['corpus_id']]] for hit in hits]
    cross_scores = cross_encoder.predict(cross_inp)
    # Sort results by the cross-encoder scores
    for idx in range(len(cross_scores)):
        hits[idx]['cross-score'] = cross_scores[idx]
    hits = sorted(hits, key=lambda x: x['cross-score'], reverse=True)

    for hit in hits[0:10]:
        result.append(corpus[hit['corpus_id']].replace("\n", " "))
    return result


corpus, bi_encoder, cross_encoder, corpus_embeddings = load_archives()
app = Flask(__name__)


@app.route('/')
def home():
    """ This is the homepage of our API.
    It can be accessed by http://127.0.0.1:5000/
    """
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
 
    query = request.form['message']
    #data = pd.Series(message)
    #vect = preprocess(data)
    my_prediction = search(query)

    res = render_template('result.html', prediction1=my_prediction[0],prediction2=my_prediction[1],prediction3=my_prediction[2] )
    return res


if __name__ == '__main__':
    app.run(debug=True)
