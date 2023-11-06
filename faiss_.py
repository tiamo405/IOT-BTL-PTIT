import os
import faiss
import numpy as np
from PIL import Image
from s3_minio.minio_ import Minio_Client

def faiss_search(emb, threshold= 0.5 , device= 'cpu', k = 1):
  minio_client = Minio_Client()
  embs = minio_client.get_embs()
  
  if device == 'cpu' :
    model_faiss = faiss.IndexFlatL2(512)
  else :
    model_faiss = faiss.IndexFlatL2(512)
  model_faiss.add(embs)
  D, I = model_faiss.search(emb, k)
  index = I[0][0]
  similarity_score = 1 / (1 + D[0][0])
  if similarity_score > threshold :
    return index
  else :
    return -1

# def index2person(index):


if __name__ == "__main__":  
  emb = np.load('tmp/emb.npy')
  print('index: ',faiss_search(emb= emb))

