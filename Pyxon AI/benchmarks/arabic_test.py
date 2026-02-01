"""
Arabic Language Support Tests
Tests Arabic text handling, diacritics, and encoding
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arabic import ArabicHandler
from src.parser import DocumentParser


class ArabicBenchmarks:
    """Arabic-specific benchmark tests"""
    
    def __init__(self):
        self.arabic_handler = ArabicHandler(preserve_diacritics=True)
        self.results = {}
    
    def test_diacritics_preservation(self):
        """Test diacritics preservation"""
        # Arabic text with diacritics
        test_text = """
        بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
        الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
        """
        
        # Count diacritics
        diacritic_count = self.arabic_handler.count_diacritics(test_text)
        has_diacritics = self.arabic_handler.has_diacritics(test_text)
        
        # Normalize with preservation
        normalized = self.arabic_handler.normalize(test_text)
        preserved_count = self.arabic_handler.count_diacritics(normalized)
        
        self.results['diacritics_test'] = {
            'original_diacritics': diacritic_count,
            'has_diacritics': has_diacritics,
            'preserved_diacritics': preserved_count,
            'preservation_rate': (preserved_count / diacritic_count * 100) if diacritic_count > 0 else 0
        }
    
    def test_diacritics_removal(self):
        """Test diacritics removal"""
        test_text = "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"
        
        removed = self.arabic_handler.remove_diacritics(test_text)
        
        self.results['diacritics_removal'] = {
            'original': test_text,
            'removed': removed,
            'original_length': len(test_text),
            'removed_length': len(removed),
            'diacritics_removed': len(test_text) - len(removed)
        }
    
    def test_arabic_detection(self):
        """Test Arabic text detection"""
        texts = [
            "هذا نص عربي",
            "This is English",
            "نص مختلط Mixed text",
            "مَا هِيَ الأَهْدَافُ؟"
        ]
        
        results = []
        for text in texts:
            is_arabic = self.arabic_handler.is_arabic(text)
            results.append({
                'text': text,
                'is_arabic': is_arabic
            })
        
        self.results['arabic_detection'] = results
    
    def test_arabic_normalization(self):
        """Test Arabic text normalization"""
        test_cases = [
            ("إأآا", "ا"),  # Alef variations
            ("ى", "ي"),  # Yeh variations
            ("ة", "ه"),  # Teh Marbuta
        ]
        
        results = []
        for original, expected in test_cases:
            normalized = self.arabic_handler.normalize_arabic_letters(original)
            results.append({
                'original': original,
                'expected': expected,
                'normalized': normalized,
                'correct': expected in normalized
            })
        
        self.results['normalization_test'] = results
    
    def test_arabic_tokenization(self):
        """Test Arabic tokenization"""
        test_text = "هذا اختبار للتقسيم النصي باللغة العربية"
        
        tokens = self.arabic_handler.tokenize_arabic(test_text)
        
        self.results['tokenization'] = {
            'original_text': test_text,
            'tokens': tokens,
            'token_count': len(tokens)
        }
    
    def test_document_parsing_arabic(self):
        """Test full document parsing with Arabic"""
        # Create test Arabic text
        arabic_text = """
        بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
        
        هذا مستند تجريبي باللغة العربية يحتوي على علامات التشكيل.
        الهدف من هذا الاختبار هو التأكد من أن النظام يدعم اللغة العربية بشكل كامل.
        
        الفقرة الثانية تحتوي على نص طويل نسبياً لاختبار عملية التقسيم.
        يجب أن يكون النظام قادراً على التعامل مع النصوص العربية بكفاءة.
        """
        
        # Save to temp file
        temp_file = "./data/test_arabic.txt"
        os.makedirs(os.path.dirname(temp_file), exist_ok=True)
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(arabic_text)
        
        # Parse
        parser = DocumentParser(language='ar', preserve_diacritics=True)
        result = parser.parse_with_chunking(temp_file)
        
        self.results['document_parsing'] = {
            'success': result.success,
            'language_detected': result.metadata.language if result.success else None,
            'num_chunks': len(result.chunks) if result.success else 0,
            'has_diacritics': self.arabic_handler.has_diacritics(result.text) if result.success else False
        }
        
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def run_all_tests(self):
        """Run all Arabic tests"""
        print("Running Arabic Language Tests...")
        print("=" * 80)
        
        self.test_diacritics_preservation()
        print("✓ Diacritics preservation test complete")
        
        self.test_diacritics_removal()
        print("✓ Diacritics removal test complete")
        
        self.test_arabic_detection()
        print("✓ Arabic detection test complete")
        
        self.test_arabic_normalization()
        print("✓ Arabic normalization test complete")
        
        self.test_arabic_tokenization()
        print("✓ Arabic tokenization test complete")
        
        self.test_document_parsing_arabic()
        print("✓ Document parsing test complete")
        
        print("=" * 80)
        print("\nTest Results:\n")
        
        return self.results
    
    def print_results(self):
        """Print formatted results"""
        import json
        print(json.dumps(self.results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    benchmarks = ArabicBenchmarks()
    results = benchmarks.run_all_tests()
    benchmarks.print_results()
    
    # Save results
    import json
    with open("./data/arabic_benchmark_results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Results saved to ./data/arabic_benchmark_results.json")
