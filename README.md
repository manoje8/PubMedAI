# Medical Research Assistant with LightRag

An AI-powered medical research assistant that helps healthcare professionals with diagnosis support using RAG (Retrieval-Augmented Generation), context engineering, clinical playbooks, and advanced prompt engineering.

## Features

- **Multi-modal Interface**: Patient mode and Doctor mode with different UI/UX
- **Context Engineering**: Structured patient data with clinical relevance scoring
- **Clinical Playbooks**: Evidence-based clinical pathways
- **RAG Pipeline**: Semantic search over medical literature
- **PubMed Integration**: Real-time search of medical literature
- **Advanced Prompt Engineering**: Chain-of-thought, few-shot, and structured outputs
- **Document Processing**: Upload and analyze medical PDFs

## Architecture

- **Backend**: FastAPI with async support
- **Frontend**: Streamlit for interactive UI
- **RAG**: LightRag

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/manoje8/PubMedAI
cd PubMedAI