from pyvi.ViTokenizer import tokenize
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


try:
    vietnamese_model = SentenceTransformer('vietnamese_search/VietnameseSimCSE')
    
except:
    vietnamese_model = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
    vietnamese_model.save('model/VietnameseSimCSE')


data = pd.read_excel('data/data.xlsx')
# option = data.columns.values[0]


def get_results_vi(query, vietnamese_model, data):
    options = data.columns.values
    index = faiss.read_index('data/data.index')
    query = tokenize(query.encode('utf-8').decode('utf-8'))
    top_k_IDs, score = search_vi(vietnamese_model, index, query, 2)
    results = [data[options[1]][i] for i in top_k_IDs]
    return {"results": results, "score": float(score)}


def search_vi(model, index, query, top_k):
    query_vector = model.encode([query])
    top_k = index.search(query_vector, top_k)
    top_k_ids = top_k[1].tolist()[0]
    top_k_ids = list(np.unique(top_k_ids))
    return top_k_ids, top_k[0][0][0]
