from langchain.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def splitting_text_recursive(documents, chunk_size=1000, chunk_overlap=200, add_start_index=True):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=add_start_index
    )
    all_splits = text_splitter.split_documents(documents)

    return all_splits


def retrieve_from_chroma(vector_chroma, query_vector, metric='cosine', top_k=5, collection_name='default_collection'):
    """
    Retrieves the top_k most similar vectors from Chroma collection using the specified metric.
    
    Parameters:
    - query_vector: list, the query vector for which to find similar vectors.
    - metric: str, the similarity metric to use ('cosine', 'euclidean', 'manhattan').
    - top_k: int, the number of top similar results to retrieve.
    - collection_name: str, the name of the collection to use or create if none exist.
    
    Returns:
    - results: list of dictionaries, each containing the id and similarity score of the retrieved vectors.
    """
    if metric not in ['cosine', 'euclidean', 'manhattan']:
        raise ValueError("Unsupported metric. Choose from 'cosine', 'euclidean', 'manhattan'.")

    metric_map = {
        'cosine': 'cosine',
        'euclidean': 'l2',
        'manhattan': 'l1'
    }
    
    results = vector_chroma.similarity_search_with_score(
        query=query_vector,
        k=top_k
        # distance_metric=metric_map[metric]
    )

    return results