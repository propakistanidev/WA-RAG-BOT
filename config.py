import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Anthropic Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Pinecone Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")

# WhatsApp Configuration
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "OCR1988")

# HuggingFace Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Legacy support (keeping for backward compatibility)
VERIFY_TOKEN = WHATSAPP_VERIFY_TOKEN