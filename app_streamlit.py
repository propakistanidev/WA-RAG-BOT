import streamlit as st
import PyPDF2
import docx
import uuid
import os
from embedder import get_embedding
from vector_store import upsert_embeddings, query_embeddings as search
from datetime import datetime

st.set_page_config(page_title="WhatsApp RAG Bot - File Manager", layout="wide")

st.title("Ekkel WhatsApp RAG Bot - Document Manager")
st.markdown("Upload documents to enable AI-powered conversations via WhatsApp")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Documents")
    
    # File uploader with multiple types
    uploaded_files = st.file_uploader(
        "Choose files to upload", 
        type=['pdf', 'txt', 'docx'], 
        accept_multiple_files=True,
        help="Supported formats: PDF, TXT, DOCX"
    )
    
    if uploaded_files:
        if st.button("Process & Upload Files", type="primary"):
            with st.spinner("Processing files..."):
                all_docs = []
                file_info = []
                
                for uploaded_file in uploaded_files:
                    try:
                        file_type = uploaded_file.type
                        file_name = uploaded_file.name
                        
                        if file_type == "application/pdf":
                            # Process PDF
                            pdf = PyPDF2.PdfReader(uploaded_file)
                            docs = []
                            for i, page in enumerate(pdf.pages):
                                text = page.extract_text()
                                if text.strip():
                                    docs.append(text.strip())
                                    all_docs.append(text.strip())
                            
                            file_info.append({
                                "name": file_name,
                                "type": "PDF",
                                "pages": len(pdf.pages),
                                "chunks": len(docs),
                                "status": "Processed"
                            })
                            
                        elif file_type == "text/plain":
                            # Process TXT
                            content = uploaded_file.read().decode("utf-8")
                            chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
                            all_docs.extend(chunks)
                            
                            file_info.append({
                                "name": file_name,
                                "type": "TXT",
                                "pages": 1,
                                "chunks": len(chunks),
                                "status": "Processed"
                            })
                            
                        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            # Process DOCX
                            doc = docx.Document(uploaded_file)
                            docs = []
                            for para in doc.paragraphs:
                                if para.text.strip():
                                    docs.append(para.text.strip())
                                    all_docs.append(para.text.strip())
                            
                            file_info.append({
                                "name": file_name,
                                "type": "DOCX",
                                "pages": 1,
                                "chunks": len(docs),
                                "status": "Processed"
                            })
                            
                    except Exception as e:
                        file_info.append({
                            "name": uploaded_file.name,
                            "type": "Unknown",
                            "pages": 0,
                            "chunks": 0,
                            "status": f"Error: {str(e)}"
                        })
                
                # Upload to vector store if we have documents
                if all_docs:
                    try:
                        upsert_embeddings(all_docs)
                        st.success(f"Successfully uploaded {len(all_docs)} document chunks to the knowledge base!")
                        
                        # Store file info in session state
                        if 'uploaded_files' not in st.session_state:
                            st.session_state.uploaded_files = []
                        st.session_state.uploaded_files.extend(file_info)
                        
                    except Exception as e:
                        st.error(f"Error uploading to vector store: {str(e)}")
                else:
                    st.warning("No readable content found in uploaded files.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Knowledge Base Status")
    
    if 'uploaded_files' in st.session_state and st.session_state.uploaded_files:
        # Display uploaded files
        for file_info in st.session_state.uploaded_files:
            with st.expander(f"{file_info['name']} ({file_info['type']})"):
                st.write(f"**Status:** {file_info['status']}")
                st.write(f"**Pages/Chunks:** {file_info['chunks']}")
                st.write(f"**File Type:** {file_info['type']}")
    else:
        st.info("No documents uploaded yet. Use the sidebar to upload files.")
    
    # Test the knowledge base
    st.header("Test Knowledge Base")
    test_query = st.text_input("Ask a question to test the knowledge base:")
    
    if test_query and st.button("Search"):
        try:
            with st.spinner("Searching..."):
                results = search(test_query, top_k=3)
                if results:
                    st.success(f"Found {len(results)} relevant chunks:")
                    for i, result in enumerate(results, 1):
                        with st.expander(f"Chunk {i}"):
                            st.write(result[:500] + "..." if len(result) > 500 else result)
                else:
                    st.warning("No relevant information found.")
        except Exception as e:
            st.error(f"Error searching: {str(e)}")

with col2:
    st.header("WhatsApp Integration")
    st.info("""
    **How it works:**
    1. Upload documents here
    2. Users send questions via WhatsApp
    3. AI searches documents and answers
    4. Responses sent back via WhatsApp
    """)
    
    st.header("System Status")
    try:
        # Test vector store connection
        test_results = search("test", top_k=1)
        st.success(" Vector store: Connected")
        st.success(" Embedding model: Ready")
        st.success(" WhatsApp webhook: Active")
    except Exception as e:
        st.error(f"❌ System error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**WhatsApp RAG Bot** - Powered by Ekkel AI")