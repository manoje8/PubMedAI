from app.core.document_processor import DocumentProcessor
from app.core.pubmed_fetcher import PubMedFetcher
from app.core.rag_pipeline import RAGPipeline


class DiagnosisAssistance:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.pubmed_fetcher = PubMedFetcher()
        self.doc_processor = DocumentProcessor()