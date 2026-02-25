import hashlib

import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
from config import Config

from shared.logger import logger

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n","\n",".", " ", ""]
        )

    def process_pdf(self, file_path:str) -> List[Dict]:
        """Extract text from PDF and split it into chunks"""

        chunks = []

        try:
            doc = fitz.open(file_path)
            full_text = ""

            for page_num in range(len(doc)):
                page = doc[page_num]
                full_text += page.get_text()

            doc.close()

            text_chunks = self.text_splitter.split_text(full_text)

            for i, chunk in enumerate(text_chunks):
                chunk_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()

                chunks.append({
                    "id": chunk_id,
                    "text": chunk,
                    "source": file_path,
                    "chunk_index": i,
                    "type": 'journal'
                })

        except Exception as e:
            logger.error(f"PDF processing error {file_path}: {str(e)}", exc_info=True)

        return chunks


    def process_pubmed_article(self, article: Dict) -> List[Dict]:
        """Process pubmed article into chunks"""
        chunks = []

        full_text = f"Title: {article.get("title", "")}\n"
        full_text += f"Authors: {''.join(article.get('authors', []))}"
        full_text += f"Journal: {article.get('journal', '')}"
        full_text += f"Publication Date: {article.get('publication_date', '')}"
        full_text += f"MeSH terms: {''.join(article.get('mesh_terms', []))}"
        full_text += f"Abstract: {article.get('abstract', '')}"


        text_chunks = self.text_splitter.split_text(full_text)


        for i, chunk in enumerate(text_chunks):
            chunk_id = hashlib.md5(f"{article['pmid']}_{i}".encode()).hexdigest()
            chunks.append({
                'id': chunk_id,
                'text': chunk,
                'source': f"PubMed ID: {article['pmid']}",
                'chunk_index': i,
                'type': 'pubmed',
                'metadata': {
                    'pmid': article['pmid'],
                    'title': article['title'],
                    'authors': article['authors'],
                    'journal': article['journal'],
                    'mesh_terms': article['mesh_terms']
                }
            })



        return chunks