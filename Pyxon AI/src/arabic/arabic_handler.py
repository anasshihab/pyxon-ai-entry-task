"""
Arabic Text Handler Module
Handles Arabic text normalization, diacritics, and text processing
"""

import re
from typing import Optional
import unicodedata


class ArabicHandler:
    """
    Comprehensive Arabic text processing
    Handles normalization, diacritics, and special characters
    """
    
    # Arabic character ranges
    ARABIC_RANGE = (0x0600, 0x06FF)
    ARABIC_SUPPLEMENT_RANGE = (0x0750, 0x077F)
    
    # Diacritics (Tashkeel/Harakat)
    DIACRITICS = [
        '\u064B',  # Fathatan
        '\u064C',  # Dammatan
        '\u064D',  # Kasratan
        '\u064E',  # Fatha
        '\u064F',  # Damma
        '\u0650',  # Kasra
        '\u0651',  # Shadda
        '\u0652',  # Sukun
        '\u0653',  # Maddah
        '\u0654',  # Hamza above
        '\u0655',  # Hamza below
        '\u0656',  # Subscript alef
        '\u0657',  # Inverted damma
        '\u0658',  # Mark noon ghunna
        '\u0670',  # Superscript alef
    ]
    
    def __init__(self, preserve_diacritics: bool = True):
        """
        Initialize Arabic handler
        
        Args:
            preserve_diacritics: Whether to preserve diacritics
        """
        self.preserve_diacritics = preserve_diacritics
    
    def normalize(self, text: str) -> str:
        """
        Normalize Arabic text
        
        Args:
            text: Arabic text to normalize
            
        Returns:
            Normalized text
        """
        # Remove diacritics if not preserving
        if not self.preserve_diacritics:
            text = self.remove_diacritics(text)
        
        # Normalize Arabic letters
        text = self.normalize_arabic_letters(text)
        
        # Normalize whitespace
        text = self.normalize_whitespace(text)
        
        return text
    
    def remove_diacritics(self, text: str) -> str:
        """
        Remove Arabic diacritics (tashkeel)
        
        Args:
            text: Text with diacritics
            
        Returns:
            Text without diacritics
        """
        for diacritic in self.DIACRITICS:
            text = text.replace(diacritic, '')
        return text
    
    def preserve_diacritics_in_text(self, text: str) -> str:
        """
        Ensure diacritics are properly encoded
        
        Args:
            text: Arabic text
            
        Returns:
            Text with preserved diacritics
        """
        # Normalize unicode
        text = unicodedata.normalize('NFC', text)
        return text
    
    def normalize_arabic_letters(self, text: str) -> str:
        """
        Normalize variations of Arabic letters
        
        Args:
            text: Arabic text
            
        Returns:
            Normalized text
        """
        # Normalize Alef variations
        text = re.sub('[إأآا]', 'ا', text)
        
        # Normalize Teh Marbuta and Heh
        text = re.sub('ة', 'ه', text)
        
        # Normalize Yeh variations
        text = re.sub('ى', 'ي', text)
        
        return text
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text
        
        Args:
            text: Text with whitespace
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def is_arabic(self, text: str) -> bool:
        """
        Check if text is primarily Arabic
        
        Args:
            text: Text to check
            
        Returns:
            True if text is Arabic
        """
        if not text:
            return False
        
        arabic_chars = sum(
            1 for char in text 
            if self.ARABIC_RANGE[0] <= ord(char) <= self.ARABIC_RANGE[1]
        )
        
        total_chars = sum(1 for char in text if char.isalpha())
        
        if total_chars == 0:
            return False
        
        return arabic_chars / total_chars > 0.5
    
    def count_diacritics(self, text: str) -> int:
        """
        Count diacritics in text
        
        Args:
            text: Arabic text
            
        Returns:
            Number of diacritics
        """
        count = sum(text.count(diacritic) for diacritic in self.DIACRITICS)
        return count
    
    def has_diacritics(self, text: str) -> bool:
        """
        Check if text contains diacritics
        
        Args:
            text: Arabic text
            
        Returns:
            True if diacritics present
        """
        return self.count_diacritics(text) > 0
    
    def reshape_for_display(self, text: str) -> str:
        """
        Reshape Arabic text for proper display
        Handles right-to-left and character joining
        
        Args:
            text: Arabic text
            
        Returns:
            Reshaped text
        """
        try:
            from arabic_reshaper import reshape
            from bidi.algorithm import get_display
            
            # Reshape Arabic characters
            reshaped_text = reshape(text)
            
            # Apply bidirectional algorithm
            display_text = get_display(reshaped_text)
            
            return display_text
        except ImportError:
            # Return original if libraries not available
            return text
    
    def tokenize_arabic(self, text: str) -> list:
        """
        Simple Arabic tokenization
        
        Args:
            text: Arabic text
            
        Returns:
            List of tokens
        """
        # Remove diacritics for tokenization
        text_no_diacritics = self.remove_diacritics(text)
        
        # Split by whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text_no_diacritics)
        
        return tokens
    
    def clean_for_embedding(self, text: str) -> str:
        """
        Clean Arabic text for embedding generation
        
        Args:
            text: Arabic text
            
        Returns:
            Cleaned text
        """
        # Normalize text
        text = self.normalize(text)
        
        # Remove extra punctuation
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        
        # Normalize whitespace
        text = self.normalize_whitespace(text)
        
        return text
