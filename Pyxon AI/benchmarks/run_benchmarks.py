"""
Comprehensive Benchmark Suite
Tests accuracy, chunking quality, performance, and Arabic support
"""

import time
import sys
import os
from typing import Dict, Any, List
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import DocumentParser
from src.chunking import ChunkingEngine
from src.storage import VectorStore, SQLStore
from src.arabic import ArabicHandler


def run_single_document_benchmark(file_path: str) -> Dict[str, Any]:
    """
    Run comprehensive benchmark on a single document
    
    Args:
        file_path: Path to document
        
    Returns:
        Dictionary with benchmark results
    """
    results = {}
    
    # Performance metrics
    start_time = time.time()
    
    # Parse document
    parser = DocumentParser(strategy='auto')
    parse_result = parser.parse_with_chunking(file_path)
    
    parse_time = time.time() - start_time
    
    if not parse_result.success:
        results['error'] = parse_result.error
        return results
    
    # Basic metrics
    results['parse_time'] = f"{parse_time:.2f}s"
    results['file_size'] = parse_result.metadata.file_size
    results['num_chunks'] = len(parse_result.chunks)
    results['total_words'] = parse_result.metadata.total_words
    results['total_chars'] = parse_result.metadata.total_chars
    results['language'] = parse_result.metadata.language
    results['chunking_strategy'] = parse_result.metadata.chunking_strategy
    
    # Chunking quality metrics
    chunk_lengths = [len(chunk.content) for chunk in parse_result.chunks]
    results['avg_chunk_size'] = sum(chunk_lengths) / len(chunk_lengths) if chunk_lengths else 0
    results['min_chunk_size'] = min(chunk_lengths) if chunk_lengths else 0
    results['max_chunk_size'] = max(chunk_lengths) if chunk_lengths else 0
    
    # Storage performance
    vector_store = VectorStore(persist_directory="./data/test_chroma")
    sql_store = SQLStore(db_path="./data/test.db")
    
    # Vector store benchmark
    start_time = time.time()
    vector_result = vector_store.add_chunks(parse_result.chunks)
    vector_time = time.time() - start_time
    
    results['vector_store_time'] = f"{vector_time:.2f}s"
    results['chunks_added_vector'] = vector_result['added']
    
    # SQL store benchmark
    start_time = time.time()
    sql_store.add_document(parse_result.metadata)
    sql_result = sql_store.add_chunks(parse_result.chunks)
    sql_time = time.time() - start_time
    
    results['sql_store_time'] = f"{sql_time:.2f}s"
    results['chunks_added_sql'] = sql_result['added']
    
    # Retrieval benchmark
    if parse_result.chunks:
        test_query = parse_result.chunks[0].content[:100]
        
        start_time = time.time()
        search_results = vector_store.search(test_query, k=5)
        search_time = time.time() - start_time
        
        results['search_time'] = f"{search_time:.4f}s"
        results['search_results_count'] = len(search_results)
    
    # Arabic-specific tests if applicable
    if parse_result.metadata.language == 'ar':
        arabic_handler = ArabicHandler()
        
        results['has_diacritics'] = arabic_handler.has_diacritics(parse_result.text)
        results['diacritic_count'] = arabic_handler.count_diacritics(parse_result.text)
    
    # Throughput metrics
    results['chars_per_second'] = int(parse_result.metadata.total_chars / parse_time)
    results['words_per_second'] = int(parse_result.metadata.total_words / parse_time)
    
    return results


def run_all_benchmarks(test_files: List[str]) -> Dict[str, Any]:
    """
    Run benchmarks on multiple files
    
    Args:
        test_files: List of file paths
        
    Returns:
        Aggregated results
    """
    all_results = []
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nBenchmarking: {file_path}")
            results = run_single_document_benchmark(file_path)
            results['file_path'] = file_path
            all_results.append(results)
        else:
            print(f"File not found: {file_path}")
    
    return {
        'individual_results': all_results,
        'summary': generate_summary(all_results)
    }


def generate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary statistics
    
    Args:
        results: List of benchmark results
        
    Returns:
        Summary statistics
    """
    if not results:
        return {}
    
    # Extract metrics
    parse_times = [float(r['parse_time'].rstrip('s')) for r in results if 'parse_time' in r]
    num_chunks = [r['num_chunks'] for r in results if 'num_chunks' in r]
    avg_chunk_sizes = [r['avg_chunk_size'] for r in results if 'avg_chunk_size' in r]
    
    summary = {
        'total_documents': len(results),
        'avg_parse_time': f"{sum(parse_times) / len(parse_times):.2f}s" if parse_times else "N/A",
        'total_chunks': sum(num_chunks),
        'avg_chunks_per_doc': sum(num_chunks) / len(num_chunks) if num_chunks else 0,
        'avg_chunk_size': sum(avg_chunk_sizes) / len(avg_chunk_sizes) if avg_chunk_sizes else 0
    }
    
    return summary


def print_results(results: Dict[str, Any]):
    """Print benchmark results"""
    print("\n" + "="*80)
    print("BENCHMARK RESULTS")
    print("="*80)
    
    if 'individual_results' in results:
        for i, result in enumerate(results['individual_results']):
            print(f"\n--- Document {i+1}: {result.get('file_path', 'Unknown')} ---")
            for key, value in result.items():
                if key != 'file_path':
                    print(f"  {key}: {value}")
        
        print("\n" + "-"*80)
        print("SUMMARY")
        print("-"*80)
        for key, value in results['summary'].items():
            print(f"  {key}: {value}")
    else:
        for key, value in results.items():
            print(f"  {key}: {value}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    # Example benchmark
    test_files = [
        "./data/sample/sample.pdf",
        "./data/sample/sample.docx",
        "./data/sample/sample.txt"
    ]
    
    print("Starting comprehensive benchmark suite...")
    results = run_all_benchmarks(test_files)
    print_results(results)
    
    # Save results
    with open("./data/benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Results saved to ./data/benchmark_results.json")
