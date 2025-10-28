# data_processing.py
import pymupdf
import re

def extract_pdf_text_ordered(pdf_path: str) -> str:
    """Extract text"""
    doc = pymupdf.open(pdf_path)
    full_text = ""
    for page in doc:
        text = page.get_text(sort=True)
        full_text += text + "\n"
    doc.close()
    return full_text

def remove_references(text: str) -> str:
    """Remove references section"""
    patterns = [
        r'\bReferences\b',
        r'See also',
        r'External links',
        r'Notes',
        r'Bibliography'
    ]
    
    earliest_pos = len(text)
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()
    
    if earliest_pos < len(text):
        print(f"Removed references section ({len(text) - earliest_pos} chars)")
        return text[:earliest_pos]
    
    print("No references section found")
    return text

def remove_headers_footers(text: str) -> str:
    """Remove Wikipedia page headers and footers"""
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip if line matches header/footer patterns
        if (
            # Date + time stamps (10/26/25, 8:57 PM)
            re.match(r'^\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}\s+[AP]M', line_stripped) or
            
            # Wikipedia title headers (Machine learning - Wikipedia)
            'Machine learning - Wikipedia' in line_stripped or
            
            # URL footers (https://en.wikipedia.org/...)
            re.match(r'^https?://en\.wikipedia\.org/', line_stripped) or
            
            # Page numbers (1/41, 2/41, etc.)
            re.match(r'^\d+/\d+$', line_stripped) or
            
            # Just page numbers
            (line_stripped.isdigit() and len(line_stripped) <= 3)
        ):
            continue
        
        cleaned_lines.append(line)
    
    result = '\n'.join(cleaned_lines)
    removed = len(text) - len(result)
    if removed > 0:
        print(f"✓ Removed headers/footers (~{removed} chars)")
    
    return result

def clean_text(text: str) -> str:
    """Final text cleaning"""
    # Remove citation numbers [1], [2]
    text = re.sub(r'\[\d+\]', '', text)
    
    # Remove citation markers like ": 488"
    text = re.sub(r':\s*\d{3,}', '', text)
    
    # Clean excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

if __name__ == "__main__":
    pdf_path = "data/Machine Learning - Wikipedia.pdf"
    
    print("Starting PDF processing...")
    
    # Extract text
    raw = extract_pdf_text_ordered(pdf_path)
    print(f"1. Extracted: {len(raw)} chars")
    
    # Remove headers/footers
    no_headers = remove_headers_footers(raw)
    print(f"2. After removing headers/footers: {len(no_headers)} chars")
    
    # Remove references
    no_refs = remove_references(no_headers)
    print(f"3. After removing references: {len(no_refs)} chars")
    
    # Clean
    clean = clean_text(no_refs)
    print(f"4. After final cleaning: {len(clean)} chars")
    
    # Save
    with open("data/ml_clean.txt", "w", encoding="utf-8") as f:
        f.write(clean)
    
    print(f"\nSaved to ml_clean.txt")
    print(f"Total reduction: {len(raw) - len(clean)} chars ({100*(len(raw)-len(clean))/len(raw):.1f}%)")