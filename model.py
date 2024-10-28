from huggingface_hub import login

login("import_your_token")

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict

#Initialize the summarization pipeline
model_name="sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization",model=model_name)

def chunk_text(text, max_length=1024):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
def similarity(documents,similarity_threshold,c):
  if c==False:
    for j in range(len(documents)):
      d = {j: documents[j] for j in range(len(documents))}
      doc_indices = {j: [j] for j in range(len(documents))}
    return d,doc_indices
  vectorizer=TfidfVectorizer()
  X=vectorizer.fit_transform(documents)
  cos_sim=cosine_similarity(X)
  cos_sim[cos_sim < similarity_threshold] = 0
  clustering_model = AgglomerativeClustering(linkage='average')
  labels = clustering_model.fit_predict(1 - cos_sim)  # Use 1 - cosine similarity to transform to distance
  dic = defaultdict(list)
  for i, cluster_id in enumerate(labels):
    dic[cluster_id].append(i)
  concatenated_docs = {}
  for cluster_id in dic:  # No need to use np.unique(cluster) since dic already contains unique cluster IDs
    concatenated_docs[cluster_id] = " ".join(documents[j] for j in dic[cluster_id])
  return concatenated_docs,dic

def summarize_documents(documents,max_length,min_length,similarity_threshold,c):
  docs,doc_id=similarity(documents,similarity_threshold,c)
  summaries=[]
  for key, doc in docs.items():
        # Chunk the document
        chunks = list(chunk_text(doc, max_length=500))  # Adjust max_length as needed
        chunk_summaries = []
        for chunk in chunks:
            # Summarize each chunk
            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            chunk_summaries.append(summary[0]['summary_text'])
        summaries.append({"doc_ids": doc_id[key], "summary_text": " ".join(chunk_summaries)})

  return summaries