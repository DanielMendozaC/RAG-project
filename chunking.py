# chunking.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

def create_chunks(text: str) -> list:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    
    Parameters:
    - chunk_size: ~800 chars (roughly 200 tokens)
    - chunk_overlap: 200 chars (maintains context between chunks)
    - separators: paragraph → line → sentence → word → character
    """
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    # Split the text
    text_chunks = splitter.split_text(text)
    
    # Add metadata
    chunks = []
    for i, chunk in enumerate(text_chunks):
        chunks.append({
            'id': i,
            'text': chunk,
            'char_count': len(chunk)
        })
    
    return chunks

if __name__ == "__main__":
    # Load preprocessed text
    with open('data/ml_clean.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    print("Creating chunks...")
    chunks = create_chunks(text)
    
    # Preview
    print(f"\nCreated {len(chunks)} chunks")
    print(f"Average size: {sum(c['char_count'] for c in chunks) // len(chunks)} chars\n")
    
    # Show first 3 chunks
    for chunk in chunks[:3]:
        print(f"Chunk {chunk['id']}:")
        print(f"  Size: {chunk['char_count']} chars")
        print(f"  Text: {chunk['text'][:150]}...")
        print()
    
    # Save
    with open('data/chunks.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)
    
    print(f"Saved to data/chunks.json")