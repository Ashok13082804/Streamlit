import os
import streamlit as st
import numpy as np
import google.generativeai as genai
import pypdf
import io

def extract_text_from_file(uploaded_file):
    """
    Extracts text from an uploaded TXT or PDF file.
    """
    file_name = uploaded_file.name.lower()
    if file_name.endswith('.txt'):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    elif file_name.endswith('.pdf'):
        pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    else:
        try:
            return uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            return ""

def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Splits text into overlapping chunks of a given character size.
    """
    chunks = []
    if not text:
        return chunks
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks

def cosine_similarity(a, b):
    """
    Computes cosine similarity between two vectors.
    """
    a = np.array(a)
    b = np.array(b)
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))

def keyword_search(query, chunks, top_k=3):
    """
    Simple word-matching fallback when Gemini embeddings API is unavailable.
    """
    words = [w.lower() for w in query.split() if len(w) > 2]
    if not words:
        return chunks[:top_k]
    
    scored_chunks = []
    for chunk in chunks:
        score = 0
        chunk_lower = chunk.lower()
        for word in words:
            score += chunk_lower.count(word)
        scored_chunks.append((score, chunk))
    
    # Sort descending by word match count
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:top_k]]

def process_and_cache_document(uploaded_file):
    """
    Processes the uploaded file: chunks it, generates embeddings using Gemini,
    and caches the results in the Streamlit session state to avoid redundant work.
    """
    if "rag_file_name" in st.session_state and st.session_state.rag_file_name == uploaded_file.name:
        # Already processed this file in this session
        return
        
    with st.spinner("Extracting text and splitting into chunks..."):
        text = extract_text_from_file(uploaded_file)
        chunks = chunk_text(text)
        
    st.session_state.rag_file_name = uploaded_file.name
    st.session_state.rag_chunks = chunks
    st.session_state.rag_embeddings = []
    
    if not chunks:
        st.warning("Could not extract any readable text from the uploaded file.")
        return

    # Attempt to pre-compute embeddings
    with st.spinner("Embedding text chunks for semantic search..."):
        try:
            embeddings = []
            for chunk in chunks:
                response = genai.embed_content(
                    model="models/text-embedding-004",
                    content=chunk,
                    task_type="retrieval_document"
                )
                embeddings.append(response['embedding'])
            st.session_state.rag_embeddings = embeddings
            st.success(f"Successfully processed {len(chunks)} chunks semantically!")
        except Exception as e:
            st.session_state.rag_embeddings = []
            st.warning(
                f"Could not pre-compute semantic embeddings (API quota or key issue). "
                f"Falling back to local keyword matching search. Error: {e}"
            )

def retrieve_context(query, top_k=3):
    """
    Retrieves the top_k most relevant chunks for a given query.
    Uses semantic vector similarity if embeddings are available,
    otherwise falls back to local term-frequency keyword matching.
    """
    chunks = st.session_state.get("rag_chunks", [])
    embeddings = st.session_state.get("rag_embeddings", [])
    
    if not chunks:
        return ""
        
    # Semantic similarity search
    if embeddings and len(embeddings) == len(chunks):
        try:
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query"
            )
            query_emb = response['embedding']
            
            similarities = [cosine_similarity(query_emb, emb) for emb in embeddings]
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            relevant_chunks = [chunks[i] for i in top_indices]
            return "\n\n".join(relevant_chunks)
        except Exception as e:
            st.warning(f"Semantic search failed during query ({e}). Falling back to keyword search.")
            
    # Term-frequency match fallback
    relevant_chunks = keyword_search(query, chunks, top_k)
    return "\n\n".join(relevant_chunks)
