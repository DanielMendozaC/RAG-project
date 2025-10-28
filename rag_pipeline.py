# rag_pipeline.py
import ollama
import chromadb

EMBEDDING_MODEL = 'nomic-embed-text'
LANGUAGE_MODEL = 'llama3.2:latest'

def retrieve(query, top_n=3):
    """Retrieve top N most relevant chunks using ChromaDB"""
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="ml_wikipedia")
    
    # Get query embedding
    query_embedding = ollama.embed(
        model=EMBEDDING_MODEL, 
        input=query
    )['embeddings'][0]
    
    # ChromaDB does cosine similarity
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )
    
    return results['documents'][0]  # Returns list of top N chunks

def generate_answer(query, context_chunks):
    """Generate answer using Llama 3.2"""
    
    # Build context from retrieved chunks
    context = '\n\n'.join([f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)])
    
    # System prompt
    system_prompt = f"""You are a helpful AI assistant. Answer the question based ONLY on the following context from a Machine Learning Wikipedia article.

Context:
{context}

If the answer is not in the context, say "I don't have enough information to answer that."
"""
    
    # Generate response
    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': query}
        ]
    )
    
    return response['message']['content']

def generate_answer_no_rag(query):
    """Generate answer using Llama 3"""
    
    # System prompt
    system_prompt = f"""You are a helpful AI assistant. Please help the user to answer the 
question.
"""
    
    # Generate response
    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': query}
        ]
    )
    
    return response['message']['content']

def rag_query(query):
    """Full RAG pipeline: retrieve + generate"""
    
    print(f"\n Query: {query}\n")
    
    # Step 1: Retrieve
    print(" Retrieving relevant chunks.")
    chunks = retrieve(query, top_n=3)
    
    print(f" Retrieved {len(chunks)} chunks\n")
    for i, chunk in enumerate(chunks):
        print(f" Chunk {i+1}: {chunk[:100]}...")
    
    # Step 2: Generate
    print("\n Generating answer\n")
    answer = generate_answer(query, chunks)
    
    print(" ANSWER:")
    print(f' {answer}')

if __name__ == "__main__":
    # Test queries

    test_queries = [
        "Who coined the term 'machine learning' in 1959?",
        "What is Tom M. Mitchell's formal definition of machine learning?",
        "What was the 'Cybertron' machine developed by Raytheon Company in the 1960s?"
    ]
    print("\n\n**Testing RAG system**")
    
    for i, query in enumerate(test_queries):
        print(f'\n\nQuery {i+1}')
        rag_query(query)

    print("\n\n\n**Testing without using the RAG systems**")

    for i, query in enumerate(test_queries):
        print(f'\n\nQuery {i+1}\n')
        response = generate_answer_no_rag(query=query)
        print(f'{response}')
