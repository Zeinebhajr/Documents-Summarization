# Documents-Summarization
# Document Summarization and Clustering

This project provides a tool for summarizing and clustering text documents. Using a combination of TF-IDF for document vectorization, Agglomerative Clustering for similarity grouping, and a Hugging Face transformer model for summarization, this pipeline helps users generate concise summaries for each document cluster. Designed for applications where large document corpora need to be quickly summarized and clustered by thematic similarity, this tool can assist in data analysis, research, and content curation.

## Features
- **Document Summarization**: Summarizes each text document or cluster of similar documents using a Hugging Face transformer model.
- **Document Clustering**: Groups similar documents using cosine similarity and agglomerative clustering, allowing for more organized summaries.
- **Chunking Support**: Long documents are automatically split into smaller chunks to enable efficient summarization without exceeding model length limitations.
- **Configurable Parameters**: Adjust the summarization length, clustering threshold, and model selection to suit different use cases.
