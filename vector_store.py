# # vector_store.py
# import os
# import numpy as np
# from embedder import get_embedding
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# load_dotenv()

# # Pinecone config
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")  # e.g., "us-east-1"
# PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# # Create Pinecone client instance
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Create index if not exists
# if PINECONE_INDEX not in pc.list_indexes().names():
#     pc.create_index(
#         name=PINECONE_INDEX,
#         dimension=384,  # adjust to your embedding size
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
#     )

# # Connect to the index
# index = pc.Index(PINECONE_INDEX)


# def upsert_embeddings(texts, namespace="default"):
#     """
#     Generate embeddings and upsert to Pinecone.
#     """
#     vectors = []
#     for i, t in enumerate(texts):
#         emb = get_embedding(t)
#         vectors.append({
#             "id": f"doc-{i}",
#             "values": emb,
#             "metadata": {"text": t}
#         })

#     index.upsert(vectors=vectors, namespace=namespace)
#     return len(vectors)


# def query_embeddings(query, top_k=5, namespace="default"):
#     """
#     Search Pinecone index for similar embeddings.
#     """
#     q_emb = get_embedding(query)
#     results = index.query(
#         vector=q_emb, top_k=top_k, include_metadata=True, namespace=namespace
#     )
#     return [(item["metadata"]["text"], item["score"]) for item in results["matches"]]

# search = query_embeddings

# vector_store.py
# vector_store.py
import os
from pinecone import Pinecone, ServerlessSpec
from embedder import get_embedding
from dotenv import load_dotenv


load_dotenv() 

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX_NAME", "rag-whatsapp-bot")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists
existing_indexes = pc.list_indexes().names()
if PINECONE_INDEX not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=384,  # Hugging Face all-MiniLM-L6-v2 embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to the index
index = pc.Index(PINECONE_INDEX)  # use client to get Index object

# Upsert embeddings
def upsert_embeddings(docs: list[str], namespace: str = "default"):
    vectors = []
    for i, doc in enumerate(docs):
        try:
            embedding = get_embedding(doc)
            vectors.append({"id": f"doc-{i}", "values": embedding.tolist(), "metadata": {"text": doc}})
        except Exception as e:
            print(f"Error processing document {i}: {e}")
            continue
    
    if vectors:
        index.upsert(vectors=vectors, namespace=namespace)
        print(f"Upserted {len(vectors)} docs into Pinecone.")
    else:
        print("No valid documents to upsert.")

# Query embeddings
def query_embeddings(query: str, top_k: int = 3, namespace: str = "default"):
    try:
        vector = get_embedding(query).tolist()
        results = index.query(vector=vector, top_k=top_k, include_metadata=True, namespace=namespace)
        return [match["metadata"]["text"] for match in results["matches"]]
    except Exception as e:
        print(f"Error querying embeddings: {e}")
        return []