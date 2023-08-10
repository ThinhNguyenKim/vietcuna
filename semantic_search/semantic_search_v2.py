from pyvi.ViTokenizer import tokenize
import pandas as pd
import faiss
import numpy as np
from torch import nn
import math
from sentence_transformers import SentenceTransformer, CrossEncoder


bi_encoder = SentenceTransformer("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
cross_encoder = CrossEncoder("VoVanPhuc/unsup-SimCSE-VietNamese-phobert-base")
data = pd.read_excel('data/data.xlsx')
option = data.columns.values[1]


class Search:
    def __init__(self, data, option, query, top_hits, bi_encoder, cross_encoder):
        self.data = data
        self.option = option
        self.query = tokenize(query.encode('utf-8').decode('utf-8'))
        self.top_hits = top_hits
        self.bi_encoder = bi_encoder
        self.cross_encoder = cross_encoder

    def fetch(self):
        ##### Sematic Search #####
        # Encode the query using the bi-encoder and find potentially relevant passages
        query_vector = self.bi_encoder.encode([self.query])
        top_k = self.index.search(query_vector, self.top_hits)
        top_k_ids = top_k[1].tolist()[0]
        top_k_ids = list(np.unique(top_k_ids))

        ##### Re-Ranking #####
        # Now, score all retrieved passages with the cross_encoder
        cross_inp = [[self.query, self.data[self.option][hit]] for hit in top_k_ids]
        bienc_op=[self.data[self.option][hit] for hit in top_k_ids]
        cross_scores = self.cross_encoder.predict(cross_inp)
       
        # Output of top_hits from re-ranker
        top_hits_cross_encoder = [top_k_ids[hit] for hit in np.argsort(np.array(cross_scores))[::-1]]
        cross_scores = np.sort(cross_scores)[::-1].tolist()

        return top_hits_cross_encoder, cross_scores

    def search(self):

        print(self.query) 
        # Read index file
        self.index=faiss.read_index('data/data.index')

        # Search
        top_hits_cross_encoder, cross_scores = self.fetch()
        dicts = self.data.iloc[top_hits_cross_encoder].to_dict('records')
        result = [{**d} for d in dicts]

        for item in result:
            for key, value in item.items():
                if isinstance(value, float) and math.isnan(value):
                    item[key] = None

        return result
    


query = 'Nhân vật chính Phùng trong tác phẩm chiếc thuyền ngoài xa làm nghề gì?'
engine = Search(data, option, query, 1, bi_encoder, cross_encoder)
print(engine.search()[0].get('Output 2'))