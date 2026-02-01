"""
Strategy Selector Module
Automatically selects the best chunking strategy based on document analysis
"""

from typing import Dict, Any
import re
from statistics import stdev, mean


class StrategySelector:
    """
    Analyzes document and selects optimal chunking strategy
    """
    
    def __init__(self):
        """Initialize strategy selector"""
        self.thresholds = {
            'uniformity': 0.3,  # Lower = more uniform
            'semantic_variance': 0.5  # Higher = more variance
        }
    
    def select_strategy(self, text: str) -> str:
        """
        Analyze text and select best chunking strategy
        
        Args:
            text: Document text to analyze
            
        Returns:
            Strategy name ('fixed' or 'dynamic')
        """
        # Analyze document characteristics
        analysis = self.analyze_document(text)
        
        # Decision logic
        uniformity_score = analysis['uniformity_score']
        semantic_variance = analysis['semantic_variance']
        has_clear_structure = analysis['has_clear_structure']
        
        # Fixed chunking is better for uniform, structured documents
        if uniformity_score < self.thresholds['uniformity'] and has_clear_structure:
            return 'fixed'
        
        # Dynamic chunking for variable structure
        if semantic_variance > self.thresholds['semantic_variance']:
            return 'dynamic'
        
        # Default to dynamic for mixed content
        return 'dynamic'
    
    def analyze_document(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive document analysis
        
        Args:
            text: Document text
            
        Returns:
            Dictionary with analysis metrics
        """
        # Split into paragraphs
        paragraphs = self._split_paragraphs(text)
        
        # Calculate metrics
        uniformity_score = self._calculate_uniformity(paragraphs)
        semantic_variance = self._calculate_semantic_variance(paragraphs)
        has_clear_structure = self._detect_structure(text)
        avg_paragraph_length = mean([len(p) for p in paragraphs]) if paragraphs else 0
        
        return {
            'uniformity_score': uniformity_score,
            'semantic_variance': semantic_variance,
            'has_clear_structure': has_clear_structure,
            'num_paragraphs': len(paragraphs),
            'avg_paragraph_length': avg_paragraph_length,
            'total_length': len(text)
        }
    
    def _split_paragraphs(self, text: str) -> list:
        """Split text into paragraphs"""
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _calculate_uniformity(self, paragraphs: list) -> float:
        """
        Calculate uniformity score based on paragraph length variance
        Lower score = more uniform
        
        Args:
            paragraphs: List of paragraph texts
            
        Returns:
            Uniformity score (0-1)
        """
        if len(paragraphs) < 2:
            return 0.0
        
        lengths = [len(p) for p in paragraphs]
        
        if not lengths:
            return 0.0
        
        # Calculate coefficient of variation
        avg_length = mean(lengths)
        if avg_length == 0:
            return 0.0
        
        std_dev = stdev(lengths)
        cv = std_dev / avg_length
        
        # Normalize to 0-1 range
        return min(cv, 1.0)
    
    def _calculate_semantic_variance(self, paragraphs: list) -> float:
        """
        Calculate semantic variance (simplified version)
        Higher score = more topic variation
        
        Args:
            paragraphs: List of paragraph texts
            
        Returns:
            Semantic variance score (0-1)
        """
        if len(paragraphs) < 2:
            return 0.0
        
        # Use sentence count variation as proxy for semantic variance
        sentence_counts = [self._count_sentences(p) for p in paragraphs]
        
        if not sentence_counts or mean(sentence_counts) == 0:
            return 0.0
        
        avg_sentences = mean(sentence_counts)
        std_sentences = stdev(sentence_counts) if len(sentence_counts) > 1 else 0
        
        variance = std_sentences / avg_sentences if avg_sentences > 0 else 0
        
        return min(variance, 1.0)
    
    def _count_sentences(self, text: str) -> int:
        """Count sentences in text"""
        # Split by sentence endings (English and Arabic)
        sentences = re.split(r'[.!?؟]\s+', text)
        return len([s for s in sentences if s.strip()])
    
    def _detect_structure(self, text: str) -> bool:
        """
        Detect if document has clear structure
        
        Args:
            text: Document text
            
        Returns:
            True if structure detected
        """
        # Look for structural markers
        markers = [
            r'^\d+\.',  # Numbered lists
            r'^[•\-*]\s',  # Bullet points
            r'^#{1,6}\s',  # Markdown headers
            r'^[A-Z][a-z]+:',  # Section headers
            r'^\d+\)\s',  # Numbered with parenthesis
        ]
        
        lines = text.split('\n')
        structured_lines = 0
        
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            for pattern in markers:
                if re.match(pattern, line):
                    structured_lines += 1
                    break
        
        # If >30% of first lines are structured
        return structured_lines / min(len(lines), 20) > 0.3 if lines else False
