"""
Command Line Interface for Document Parser
"""

import click
import os
from pathlib import Path
from src.parser import DocumentParser
from src.storage import VectorStore, SQLStore
from src.rag import RAGSystem
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()


@click.group()
def cli():
    """AI-Powered Document Parser CLI"""
    console.print("[bold blue]🚀 AI Document Parser[/bold blue]", style="bold")


@cli.command()
@click.option('--file', '-f', required=True, help='Path to document file')
@click.option('--strategy', '-s', default='auto', help='Chunking strategy (auto/fixed/dynamic)')
@click.option('--language', '-l', default='en', help='Document language (en/ar)')
@click.option('--chunk-size', '-c', default=512, help='Chunk size for fixed strategy')
@click.option('--preserve-diacritics', '-d', is_flag=True, default=True, help='Preserve Arabic diacritics')
def parse(file, strategy, language, chunk_size, preserve_diacritics):
    """Parse a document and store in databases"""
    
    console.print(f"\n[cyan]Parsing document: {file}[/cyan]")
    
    if not os.path.exists(file):
        console.print(f"[red]Error: File not found: {file}[/red]")
        return
    
    # Initialize parser
    parser = DocumentParser(
        language=language,
        preserve_diacritics=preserve_diacritics,
        strategy=strategy
    )
    
    # Parse document
    with Progress() as progress:
        task = progress.add_task("[green]Processing...", total=100)
        
        progress.update(task, advance=25)
        result = parser.parse_with_chunking(file, chunk_size=chunk_size)
        
        progress.update(task, advance=25)
        
        if not result.success:
            console.print(f"[red]Error: {result.error}[/red]")
            return
        
        # Initialize databases
        vector_store = VectorStore()
        sql_store = SQLStore()
        
        progress.update(task, advance=25)
        
        # Store results
        sql_store.add_document(result.metadata)
        sql_store.add_chunks(result.chunks)
        vector_store.add_chunks(result.chunks)
        
        progress.update(task, advance=25)
    
    # Display results
    console.print("\n[green]✅ Document processed successfully![/green]\n")
    
    table = Table(title="Document Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Document ID", result.document_id)
    table.add_row("Filename", result.metadata.filename)
    table.add_row("File Type", result.metadata.file_type)
    table.add_row("Language", result.metadata.language)
    table.add_row("Chunks Created", str(len(result.chunks)))
    table.add_row("Total Words", str(result.metadata.total_words))
    table.add_row("Total Characters", str(result.metadata.total_chars))
    table.add_row("Chunking Strategy", result.metadata.chunking_strategy)
    
    console.print(table)


@cli.command()
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--num-results', '-n', default=5, help='Number of results')
@click.option('--language', '-l', default=None, help='Filter by language')
def search(query, num_results, language):
    """Search for documents"""
    
    console.print(f"\n[cyan]Searching for: {query}[/cyan]\n")
    
    # Initialize stores
    vector_store = VectorStore()
    sql_store = SQLStore()
    rag_system = RAGSystem(vector_store, sql_store)
    
    # Perform search
    results = rag_system.retriever.retrieve(
        query=query,
        k=num_results,
        language=language
    )
    
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return
    
    # Display results
    console.print(f"[green]Found {len(results)} results:[/green]\n")
    
    for i, result in enumerate(results):
        console.print(f"[bold cyan]Result {i+1} (Score: {result['score']:.3f})[/bold cyan]")
        console.print(f"{result['content'][:300]}...\n")
        console.print(f"[dim]Document: {result['chunk_metadata']['document_id']}[/dim]")
        console.print("─" * 80 + "\n")


@cli.command()
def list_documents():
    """List all processed documents"""
    
    sql_store = SQLStore()
    docs = sql_store.list_documents()
    
    if not docs:
        console.print("[yellow]No documents found[/yellow]")
        return
    
    table = Table(title="Processed Documents")
    table.add_column("ID", style="cyan")
    table.add_column("Filename", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Language", style="magenta")
    table.add_column("Chunks", style="blue")
    
    for doc in docs:
        table.add_row(
            doc['document_id'][:12] + "...",
            doc['filename'],
            doc['file_type'],
            doc['language'],
            str(doc['num_chunks'])
        )
    
    console.print(table)


@cli.command()
def stats():
    """Display database statistics"""
    
    sql_store = SQLStore()
    vector_store = VectorStore()
    
    stats = sql_store.get_statistics()
    
    table = Table(title="Database Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Documents", str(stats.get('total_documents', 0)))
    table.add_row("Total Chunks", str(stats.get('total_chunks', 0)))
    table.add_row("Vector Store Chunks", str(vector_store.count_chunks()))
    
    # By language
    for lang, count in stats.get('by_language', {}).items():
        table.add_row(f"Documents ({lang})", str(count))
    
    # By file type
    for ftype, count in stats.get('by_file_type', {}).items():
        table.add_row(f"Documents ({ftype})", str(count))
    
    console.print(table)


@cli.command()
@click.option('--document-id', '-d', required=True, help='Document ID to delete')
def delete(document_id):
    """Delete a document"""
    
    if click.confirm(f'Delete document {document_id}?'):
        sql_store = SQLStore()
        vector_store = VectorStore()
        
        sql_store.delete_document(document_id)
        vector_store.delete_document(document_id)
        
        console.print(f"[green]✅ Document {document_id} deleted[/green]")


@cli.command()
@click.option('--file', '-f', required=True, help='Path to document file')
def benchmark(file):
    """Run benchmarks on a document"""
    
    from benchmarks.run_benchmarks import run_single_document_benchmark
    
    if not os.path.exists(file):
        console.print(f"[red]Error: File not found: {file}[/red]")
        return
    
    console.print(f"\n[cyan]Running benchmarks on: {file}[/cyan]\n")
    
    results = run_single_document_benchmark(file)
    
    # Display results
    table = Table(title="Benchmark Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    for metric, value in results.items():
        table.add_row(metric, str(value))
    
    console.print(table)


if __name__ == '__main__':
    cli()
