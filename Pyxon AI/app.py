"""
Streamlit Web Demo for AI-Powered Document Parser
Interactive interface for document parsing and RAG capabilities
"""

import streamlit as st
import os
from pathlib import Path
import time
from datetime import datetime

# Import our modules
from src.parser import DocumentParser
from src.chunking import ChunkingEngine
from src.storage import VectorStore, SQLStore
from src.rag import RAGSystem
from src.arabic import ArabicHandler

# Page configuration
st.set_page_config(
    page_title="AI Document Parser - RAG System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background: rgba(255,255,255,0.05);
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .chunk-card {
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
    }
    h1, h2, h3 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()
if 'sql_store' not in st.session_state:
    st.session_state.sql_store = SQLStore()
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = RAGSystem(
        st.session_state.vector_store,
        st.session_state.sql_store
    )
if 'processed_documents' not in st.session_state:
    st.session_state.processed_documents = []

def main():
    """Main application"""
    
    # Header
    st.title("🚀 AI-Powered Document Parser with RAG")
    st.markdown("### Advanced Document Processing for Retrieval-Augmented Generation")
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=150)
        st.markdown("## 📋 Navigation")
        
        page = st.radio(
            "Select Page",
            ["📄 Upload & Parse", "🔍 Search & Retrieve", "📊 Analytics", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📞 Contact")
        st.markdown("**Anas Mohammad**")
        st.markdown("📧 anas.mohammad6673332@gmail.com")
        st.markdown("📱 00962786673332")
        
        st.markdown("---")
        st.markdown("### 🎯 Features")
        st.markdown("""
        - ✅ Multi-format parsing
        - ✅ Smart chunking
        - ✅ Arabic support
        - ✅ Vector search
        - ✅ RAG ready
        """)
    
    # Route to appropriate page
    if page == "📄 Upload & Parse":
        upload_parse_page()
    elif page == "🔍 Search & Retrieve":
        search_page()
    elif page == "📊 Analytics":
        analytics_page()
    else:
        settings_page()

def upload_parse_page():
    """Upload and parse documents page"""
    
    st.header("📄 Upload & Parse Documents")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Upload Your Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        # Configuration
        st.markdown("### ⚙️ Configuration")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            language = st.selectbox("Language", ["Auto-detect", "English", "Arabic"])
        with col_b:
            strategy = st.selectbox("Chunking Strategy", ["Auto", "Fixed", "Dynamic"])
        with col_c:
            chunk_size = st.slider("Chunk Size", 256, 1024, 512)
        
        preserve_diacritics = st.checkbox("Preserve Arabic Diacritics", value=True)
        
        if uploaded_file:
            # Save uploaded file
            save_path = f"./data/uploads/{uploaded_file.name}"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Parse button
            if st.button("🚀 Parse Document", type="primary", use_container_width=True):
                with st.spinner("⏳ Processing document..."):
                    parse_document(save_path, language, strategy, chunk_size, preserve_diacritics)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        stats = st.session_state.sql_store.get_statistics()
        
        st.metric("Total Documents", stats.get('total_documents', 0))
        st.metric("Total Chunks", stats.get('total_chunks', 0))
        st.metric("In Vector DB", st.session_state.vector_store.count_chunks())
        
        # Recent documents
        st.markdown("### 📁 Recent Documents")
        recent = st.session_state.sql_store.list_documents()[:5]
        
        if recent:
            for doc in recent:
                with st.expander(f"📄 {doc['filename']}"):
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.write(f"**Type:** {doc['file_type']}")
                        st.write(f"**Language:** {doc['language']}")
                        st.write(f"**Chunks:** {doc['num_chunks']}")
                    
                    with col_action:
                        if st.button("🗑️", key=f"del_recent_{doc['document_id']}", help="Delete this document"):
                            with st.spinner("Deleting..."):
                                st.session_state.sql_store.delete_document(doc['document_id'])
                                st.session_state.vector_store.delete_document(doc['document_id'])
                                st.success(f"✅ Deleted: {doc['filename']}")
                                st.rerun()
        else:
            st.info("No documents yet. Upload your first document!")

def parse_document(file_path, language, strategy, chunk_size, preserve_diacritics):
    """Parse and process document"""
    
    try:
        # Map language
        lang_map = {"Auto-detect": "en", "English": "en", "Arabic": "ar"}
        lang = lang_map[language]
        
        # Map strategy
        strat_map = {"Auto": "auto", "Fixed": "fixed", "Dynamic": "dynamic"}
        strat = strat_map[strategy]
        
        # Create parser
        parser = DocumentParser(
            language=lang,
            preserve_diacritics=preserve_diacritics,
            strategy=strat
        )
        
        # Parse with progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📖 Reading document...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        # Parse
        result = parser.parse_with_chunking(file_path, chunk_size=chunk_size)
        
        if not result.success:
            st.error(f"❌ Error: {result.error}")
            return
        
        status_text.text("✂️ Chunking text...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        # Store in databases
        status_text.text("💾 Storing in databases...")
        progress_bar.progress(75)
        
        # Add to SQL
        st.session_state.sql_store.add_document(result.metadata)
        st.session_state.sql_store.add_chunks(result.chunks)
        
        # Add to Vector DB
        st.session_state.vector_store.add_chunks(result.chunks)
        
        progress_bar.progress(100)
        status_text.text("✅ Processing complete!")
        time.sleep(0.5)
        
        # Display results
        st.success("🎉 Document processed successfully!")
        
        # Show metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Chunks Created", len(result.chunks))
        col2.metric("Total Words", result.metadata.total_words)
        col3.metric("Language", result.metadata.language.upper())
        col4.metric("Strategy", result.metadata.chunking_strategy.title())
        
        # Show sample chunks
        st.markdown("### 📝 Sample Chunks")
        for i, chunk in enumerate(result.chunks[:3]):
            with st.expander(f"Chunk {i+1}"):
                st.write(chunk.content[:500] + "..." if len(chunk.content) > 500 else chunk.content)
        
        # Store in session
        st.session_state.processed_documents.append({
            'id': result.document_id,
            'name': result.metadata.filename,
            'timestamp': datetime.now()
        })
        
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")

def search_page():
    """Search and retrieval page"""
    
    st.header("🔍 Search & Retrieve")
    
    # Search interface
    st.markdown("### Search Your Documents")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query",
            placeholder="What are you looking for?",
            label_visibility="collapsed"
        )
    
    with col2:
        num_results = st.number_input("Results", 1, 20, 5)
    
    # Language filter
    col_a, col_b = st.columns(2)
    with col_a:
        search_lang = st.selectbox("Filter by Language", ["All", "English", "Arabic"])
    with col_b:
        # Get available documents
        docs = st.session_state.sql_store.list_documents()
        doc_options = ["All Documents"] + [f"{d['filename']} ({d['document_id'][:8]})" for d in docs]
        selected_doc = st.selectbox("Filter by Document", doc_options)
    
    # Search button
    if st.button("🔎 Search", type="primary", use_container_width=True):
        if query:
            with st.spinner("🔍 Searching..."):
                # Prepare filters
                doc_id = None
                if selected_doc != "All Documents":
                    doc_idx = doc_options.index(selected_doc) - 1
                    doc_id = docs[doc_idx]['document_id']
                
                lang_filter = None
                if search_lang != "All":
                    lang_filter = "ar" if search_lang == "Arabic" else "en"
                
                # Perform search
                results = st.session_state.rag_system.retriever.retrieve(
                    query=query,
                    k=num_results,
                    document_id=doc_id,
                    language=lang_filter
                )
                
                # Display results
                st.markdown(f"### Found {len(results)} Results")
                
                for i, result in enumerate(results):
                    with st.container():
                        st.markdown(f"""
                        <div class="chunk-card">
                            <h4>Result {i+1} - Score: {result['score']:.3f}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.write(result['content'])
                        
                        # Metadata
                        with st.expander("📋 Metadata"):
                            st.json(result['chunk_metadata'])
                            if result['document_metadata']:
                                st.json(result['document_metadata'])
                        
                        st.markdown("---")
        else:
            st.warning("⚠️ Please enter a search query")

def analytics_page():
    """Analytics and statistics page"""
    
    st.header("📊 Analytics Dashboard")
    
    # Get statistics
    stats = st.session_state.sql_store.get_statistics()
    
    # Overview metrics
    st.markdown("### 📈 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Documents", stats.get('total_documents', 0))
    col2.metric("Total Chunks", stats.get('total_chunks', 0))
    col3.metric("Vector Store", st.session_state.vector_store.count_chunks())
    col4.metric("Avg Chunks/Doc", 
                stats['total_chunks'] // max(stats['total_documents'], 1) if stats.get('total_documents') else 0)
    
    # By language
    st.markdown("### 🌍 By Language")
    lang_data = stats.get('by_language', {})
    if lang_data:
        cols = st.columns(len(lang_data))
        for i, (lang, count) in enumerate(lang_data.items()):
            cols[i].metric(lang.upper(), count)
    
    # By file type
    st.markdown("### 📁 By File Type")
    type_data = stats.get('by_file_type', {})
    if type_data:
        cols = st.columns(len(type_data))
        for i, (ftype, count) in enumerate(type_data.items()):
            cols[i].metric(ftype.upper(), count)
    
    # Document list
    st.markdown("### 📚 All Documents")
    docs = st.session_state.sql_store.list_documents()
    
    if docs:
        for doc in docs:
            with st.expander(f"📄 {doc['filename']} - {doc['document_id'][:12]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**File Type:** {doc['file_type']}")
                    st.write(f"**Language:** {doc['language']}")
                    st.write(f"**Chunks:** {doc['num_chunks']}")
                    st.write(f"**Words:** {doc['total_words']}")
                
                with col2:
                    st.write(f"**Size:** {doc['file_size']} bytes")
                    st.write(f"**Strategy:** {doc['chunking_strategy']}")
                    st.write(f"**Processed:** {doc['processed_at']}")
                
                if st.button(f"🗑️ Delete", key=f"del_{doc['document_id']}"):
                    st.session_state.sql_store.delete_document(doc['document_id'])
                    st.session_state.vector_store.delete_document(doc['document_id'])
                    st.success("✅ Document deleted")
                    st.rerun()
    else:
        st.info("No documents yet. Upload some documents to get started!")

def settings_page():
    """Settings and database management page"""
    
    st.header("⚙️ Settings & Database Management")
    
    # Document Management Section
    st.markdown("### 📁 Document Management")
    
    docs = st.session_state.sql_store.list_documents()
    
    if docs:
        st.info(f"📊 Total Documents: {len(docs)}")
        
        # Bulk delete option
        with st.expander("🗑️ Bulk Delete All Documents"):
            st.warning("⚠️ This will delete all documents from both databases!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Delete All Documents", type="secondary", use_container_width=True):
                    st.session_state['confirm_delete_all'] = True
            
            if st.session_state.get('confirm_delete_all', False):
                st.error("**Are you sure?** This cannot be undone!")
                
                with col2:
                    if st.button("✅ Yes, Delete All", type="primary", use_container_width=True):
                        with st.spinner("Deleting all documents..."):
                            for doc in docs:
                                st.session_state.sql_store.delete_document(doc['document_id'])
                                st.session_state.vector_store.delete_document(doc['document_id'])
                            st.session_state['confirm_delete_all'] = False
                            st.success("✅ All documents deleted!")
                            st.balloons()
                            st.rerun()
                
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state['confirm_delete_all'] = False
                    st.rerun()
    else:
        st.info("📭 No documents in database. Upload documents to get started!")
    
    st.markdown("---")
    
    # Database Management Section
    st.markdown("### 🗄️ Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔵 Vector Database")
        chunk_count = st.session_state.vector_store.count_chunks()
        st.metric("Chunks Stored", chunk_count)
        
        if st.button("🔄 Reset Vector DB", type="secondary", use_container_width=True):
            st.session_state['confirm_vector_reset'] = True
        
        if st.session_state.get('confirm_vector_reset', False):
            st.warning("⚠️ This will delete all vector embeddings!")
            
            col_v1, col_v2 = st.columns(2)
            
            with col_v1:
                if st.button("✅ Confirm Reset", type="primary", key="confirm_vector"):
                    with st.spinner("Resetting vector database..."):
                        st.session_state.vector_store.reset()
                        st.session_state['confirm_vector_reset'] = False
                        st.success("✅ Vector database reset!")
                        st.rerun()
            
            with col_v2:
                if st.button("❌ Cancel", key="cancel_vector"):
                    st.session_state['confirm_vector_reset'] = False
                    st.rerun()
    
    with col2:
        st.markdown("#### 🟢 SQL Database")
        stats = st.session_state.sql_store.get_statistics()
        st.metric("Documents", stats.get('total_documents', 0))
        st.metric("Chunks", stats.get('total_chunks', 0))
        
        if st.button("🔄 Reset SQL DB", type="secondary", use_container_width=True):
            st.session_state['confirm_sql_reset'] = True
        
        if st.session_state.get('confirm_sql_reset', False):
            st.warning("⚠️ This will delete all documents and metadata!")
            
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                if st.button("✅ Confirm Reset", type="primary", key="confirm_sql"):
                    with st.spinner("Resetting SQL database..."):
                        st.session_state.sql_store.reset()
                        st.session_state['confirm_sql_reset'] = False
                        st.success("✅ SQL database reset!")
                        st.rerun()
            
            with col_s2:
                if st.button("❌ Cancel", key="cancel_sql"):
                    st.session_state['confirm_sql_reset'] = False
                    st.rerun()
    
    st.markdown("---")
    
    # Complete Reset Option
    st.markdown("### 🔴 Complete System Reset")
    st.error("⚠️ **DANGER ZONE**: This will reset BOTH databases and delete ALL data!")
    
    if st.button("💥 Reset Everything", type="secondary"):
        st.session_state['confirm_complete_reset'] = True
    
    if st.session_state.get('confirm_complete_reset', False):
        st.error("🚨 **FINAL WARNING**: This action cannot be undone!")
        st.write("Type **DELETE ALL** to confirm:")
        
        confirm_text = st.text_input("Confirmation", key="complete_reset_text")
        
        col_final1, col_final2 = st.columns(2)
        
        with col_final1:
            if st.button("✅ Confirm Complete Reset", type="primary", disabled=(confirm_text != "DELETE ALL")):
                with st.spinner("Resetting all databases..."):
                    st.session_state.vector_store.reset()
                    st.session_state.sql_store.reset()
                    st.session_state['confirm_complete_reset'] = False
                    st.success("✅ All databases reset successfully!")
                    st.balloons()
                    st.rerun()
        
        with col_final2:
            if st.button("❌ Cancel Complete Reset"):
                st.session_state['confirm_complete_reset'] = False
                st.rerun()
    
    st.markdown("---")
    
    # System Information
    st.markdown("### 💡 System Information")
    st.write(f"**Version:** 1.0.0")
    st.write(f"**Author:** Anas Mohammad")
    st.write(f"**Email:** anas.mohammad6673332@gmail.com")
    st.write(f"**Phone:** 00962786673332")


if __name__ == "__main__":
    main()
