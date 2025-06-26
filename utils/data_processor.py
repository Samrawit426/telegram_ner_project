import re
import pandas as pd
from typing import List, Tuple, Dict

def preprocess_amharic_text(text: str) -> str:
    """Preprocess Amharic text by cleaning and normalizing.
    
    Args:
        text: Raw Amharic text string
        
    Returns:
        Cleaned and normalized text
    """
    if not text:
        return ""
        
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove phone numbers (Ethiopian format)
    text = re.sub(r'(?:\+251|0)(?:9|7)\d{8}', '', text)
    
    # Remove Telegram handles
    text = re.sub(r'@\w+', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_entities(text: str) -> List[Tuple[str, str]]:
    """Extract potential entities from text based on patterns.
    
    Args:
        text: Preprocessed Amharic text
        
    Returns:
        List of (token, predicted_label) tuples
    """
    tokens = []
    
    # Split text into words
    words = text.split()
    
    for word in words:
        # Price patterns (Ethiopian Birr)
        if re.search(r'\d+(?:\.\d+)?\s*(?:ብር|birr|ETB)', word, re.IGNORECASE):
            tokens.append((word, 'B-PRICE'))
            continue
            
        # Product indicators
        if any(indicator in word.lower() for indicator in ['ዋጋ', 'price', 'product', 'item']):
            tokens.append((word, 'B-PRODUCT'))
            continue
            
        # Location indicators
        if any(indicator in word.lower() for indicator in ['አድራሻ', 'location', 'ቦታ']):
            tokens.append((word, 'B-LOC'))
            continue
            
        # Default case
        tokens.append((word, 'O'))
        
    return tokens

def convert_to_conll(tokens: List[Tuple[str, str]]) -> str:
    """Convert tokens to CoNLL format.
    
    Args:
        tokens: List of (token, label) tuples
        
    Returns:
        String in CoNLL format
    """
    conll_lines = [f'{token}\t{label}' for token, label in tokens]
    return '\n'.join(conll_lines) + '\n\n'

def process_telegram_data(csv_path: str, output_path: str):
    """Process Telegram data and convert to CoNLL format.
    
    Args:
        csv_path: Path to CSV file with Telegram messages
        output_path: Path to save CoNLL formatted output
    """
    # Read CSV file
    df = pd.read_csv(csv_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for message in df['message']:
            if not isinstance(message, str):
                continue
                
            # Preprocess text
            clean_text = preprocess_amharic_text(message)
            
            # Extract entities
            tokens = extract_entities(clean_text)
            
            # Convert to CoNLL format
            conll_text = convert_to_conll(tokens)
            
            # Write to file
            f.write(conll_text)