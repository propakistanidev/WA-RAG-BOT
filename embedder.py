# # embedder.py
# import torch
# from transformers import AutoTokenizer, AutoModel

# # Load a HuggingFace embedding model (can be changed if needed)
# HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# # Initialize tokenizer and model once (not every function call)
# tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
# model = AutoModel.from_pretrained(HF_MODEL)

# def get_embedding(text: str):
#     """
#     Generate an embedding vector for the given text using HuggingFace model.
#     """
#     # Tokenize the input text
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

#     # Disable gradient calculation for efficiency
#     with torch.no_grad():
#         outputs = model(**inputs)

#     # Mean pooling → average across tokens
#     embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

#     # Convert tensor to Python list
#     return embeddings.tolist()

# embedder.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Hugging Face embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def get_embedding(text: str):
    if not isinstance(text, str):
        raise ValueError("Input to get_embedding must be a string.")
    
    # Handle empty or very short text
    if not text.strip():
        raise ValueError("Input text cannot be empty or whitespace only.")
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
        embedding = embeddings[0].numpy()
        
        # Validate embedding values
        if np.any(np.isnan(embedding)) or np.any(np.isinf(embedding)):
            raise ValueError("Generated embedding contains NaN or infinite values")
        
        return embedding