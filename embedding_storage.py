# embedding_storage.py
import json
import ollama
import chromadb

EMBEDDING_MODEL = 'nomic-embed-text'  

def create_and_store_embeddings():
    """
    1. Load chunks
    2. Create embeddings using Ollama
    3. Store in ChromaDB
    """
    
    print("Loading chunks...")
    with open('data/chunks.json', 'r') as f:
        chunks = json.load(f)
    
    print(f"Loaded {len(chunks)} chunks\n")
    
    # Initialize ChromaDB
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    collection = client.get_or_create_collection(
        name="ml_wikipedia",
        metadata={"description": "Machine Learning Wikipedia chunks"}
    )
    print("ChromaDB initialized\n")
    
    # Create embeddings using Ollama
    print(f"Creating embeddings for {len(chunks)} chunks using Ollama...")
    
    embeddings = []
    texts = []
    ids = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        # Get embedding from Ollama
        embedding = ollama.embed(
            model=EMBEDDING_MODEL, 
            input=chunk['text']
        )['embeddings'][0]
        
        embeddings.append(embedding)
        texts.append(chunk['text'])
        ids.append(str(chunk['id']))
        metadatas.append({'char_count': chunk['char_count']})
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(chunks)} chunks")
    
    # Store in ChromaDB
    print("\nStoring in ChromaDB...")
    collection.add(
        embeddings=embeddings,
        documents=texts,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"\nSuccessfully stored {len(chunks)} chunks!")
    print(f"Database saved to ./chroma_db/\n")
    
    print(" Quick Test ")
    test_query = "What is machine learning?"
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=test_query)['embeddings'][0]
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    print(f"Query: '{test_query}'")
    print(f"Top result: {results['documents'][0][0][:150]}...")

if __name__ == "__main__":
    create_and_store_embeddings()