# check_overlap.py
import json

with open('data/chunks.json', 'r') as f:
    chunks = json.load(f)

# Check first 3 consecutive chunks for overlap
for i in range(min(3, len(chunks)-1)):
    chunk1 = chunks[i]['text']
    chunk2 = chunks[i+1]['text']
    
    # Get last 100 chars of chunk1
    end_of_chunk1 = chunk1[-100:]
    
    # Check if beginning of chunk2 contains any of this
    print(f"\n=== Checking Chunk {i} → Chunk {i+1} ===")
    print(f"End of Chunk {i}: ...{end_of_chunk1}")
    print(f"\nStart of Chunk {i+1}: {chunk2[:100]}...")
    
    # Simple overlap check
    has_overlap = any(end_of_chunk1[j:j+20] in chunk2 for j in range(0, 80, 5))
    print(f"\nOverlap detected: {has_overlap}")
    print("-" * 80)