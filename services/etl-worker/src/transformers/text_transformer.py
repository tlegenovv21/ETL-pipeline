from .base import BaseTransformer
import re
import nltk
from nltk.tokenize import word_tokenize
from langdetect import detect, LangDetectException

# Download required NLTK data (runs silently)
nltk.download('punkt', quiet=True)

class TextTransformer(BaseTransformer):
    def transform(self, data):
        if not data or 'summary' not in data:
            return None
        
        raw_text = data['summary']
        
        # 1. Cleaning: Remove special characters and lowercase
        clean_text = re.sub(r'[^\w\s]', '', raw_text.lower())
        
        # 2. Tokenization
        tokens = word_tokenize(clean_text)
        
        # 3. Language Extraction
        try:
            language = detect(raw_text)
        except LangDetectException:
            language = "unknown"

        # Prepare specific metadata
        specific_metadata = {
            "language": language,
            "word_count": len(tokens),
            "tokens": tokens[:10], # Store first 10 tokens as a sample
            "original_title": data.get("title")
        }

        # Return using the unified schema
        return self.unify_metadata(
            raw_id=data.get("title"), 
            source_type="wikipedia",
            data_type="text",
            content=clean_text,
            metadata=specific_metadata
        )