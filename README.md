# 🤖 WhatsApp RAG Bot

A powerful WhatsApp chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions based on uploaded documents. Built with FastAPI, Streamlit, Anthropic Claude, and Pinecone.

## ✨ Features

- **📱 WhatsApp Integration**: Receive and respond to messages via WhatsApp
- **📄 Multi-format Support**: Upload PDF, TXT, and DOCX files
- **🧠 AI-Powered**: Uses Anthropic Claude for intelligent responses
- **🔍 Smart Search**: Vector search through document content using Pinecone
- **🌐 Web Interface**: Streamlit dashboard for file management and testing
- **📊 Real-time Status**: Monitor system health and document status

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env` file in the project root:

```env
# WhatsApp Configuration
WHATSAPP_TOKEN=your_whatsapp_token_here
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=us-east-1
PINECONE_INDEX_NAME=rag-whatsapp-bot

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional
TOKENIZERS_PARALLELISM=false
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the System

#### Start the WhatsApp Webhook (FastAPI)
```bash
uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload
```

#### Start the File Manager (Streamlit)
```bash
streamlit run app_streamlit.py
```

## 📋 Prerequisites

### WhatsApp Business API
1. Create a Meta Developer account
2. Set up a WhatsApp Business app
3. Configure webhook endpoints
4. Get your access token and phone number ID

### Pinecone
1. Sign up for Pinecone
2. Create a new index
3. Get your API key
4. Note your index name

### Anthropic
1. Sign up for Anthropic
2. Get your API key for Claude

## 🔧 Configuration

### WhatsApp Webhook Setup
1. Set your webhook URL to: `https://your-domain.com/webhook`
2. Verify token should match your `WHATSAPP_VERIFY_TOKEN` in `.env`
3. Subscribe to `messages` events
4. Non-message events (e.g., delivery/read receipts) are safely ignored by the webhook

### Pinecone Index
- **Dimension**: 384 (for all-MiniLM-L6-v2 embeddings)
- **Metric**: cosine
- **Cloud**: AWS (us-east-1)
- Uses Pinecone v2 serverless API

## 📱 Usage

### 1. Upload Documents
- Open the Streamlit interface
- Upload PDF, TXT, or DOCX files
- Click "Process & Upload Files"
- Monitor upload status

### 2. WhatsApp Interaction
- Users send questions via WhatsApp
- Bot searches uploaded documents (via Pinecone) for relevant context
- AI generates contextual responses using Anthropic Claude
- Replies sent back via WhatsApp
- Only text messages are processed; other message types are ignored

### 3. Test Knowledge Base
- Use the Streamlit interface to test queries
- Verify document retrieval
- Monitor system performance

## 🏗️ Architecture

```
User Uploads → Streamlit → Vector Store (Pinecone)
                                    ↓
WhatsApp Message → FastAPI → RAG Pipeline → Anthropic Claude
                                    ↓
Response → WhatsApp API → User
```

## 🔍 API Endpoints

### GET `/webhook`
- WhatsApp webhook verification
- Returns challenge token

### POST `/webhook`
- Receives WhatsApp messages
- Processes RAG pipeline
- Sends responses back

## 📁 File Structure

```
RAG-Bot/
├── app_fastapi.py          # WhatsApp webhook server
├── app_streamlit.py        # File management interface
├── vector_store.py         # Pinecone operations
├── embedder.py            # Text embedding generation
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Environment Variables Missing**
   - Check `.env` file exists
   - Verify all required variables are set

2. **Pinecone Connection Error**
   - Verify API key and index name
   - Check index exists and is accessible

3. **WhatsApp Webhook Issues**
   - Verify webhook URL is accessible
   - `WHATSAPP_VERIFY_TOKEN` must match the token configured in Meta
   - Ensure SSL certificate is valid
   - Error `Error parsing WhatsApp message: 'messages'`: occurs on non-message events; the handler ignores these.

4. **File Upload Errors**
   - Check file format support
   - Verify file size limits
   - Monitor error logs

5. **Anthropic 400: Unexpected role "system"**
   - Use Messages API with top-level `system` field, not a `system` role inside `messages`.

6. **Pinecone 400: invalid value for QueryVector**
   - Use v2 query signature: `index.query(vector=..., top_k=..., include_metadata=True, ...)`
   - Validate embeddings (no NaN/Inf) and correct dimension (384)

7. **ModuleNotFoundError: No module named 'exceptions' when importing docx**
   - Caused by a stray `docx.py` overshadowing `python-docx`; ensure only `python-docx` is installed and no local `docx.py` exists.

8. **NameError: JSONResponse is not defined**
   - Add `from fastapi.responses import JSONResponse`.

## 🔒 Security Notes

- Keep API keys secure
- Use HTTPS for production
- Implement rate limiting
- Monitor API usage

## 📈 Scaling

- Use multiple Pinecone indexes for different document types
- Implement caching for frequent queries
- Add monitoring and logging
- Consider load balancing for high traffic

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review error logs
- Verify configuration
- Test individual components

---

**Built with ❤️ using FastAPI, Streamlit, Anthropic Claude, and Pinecone**
# Whatsapp-RAG-BOT
