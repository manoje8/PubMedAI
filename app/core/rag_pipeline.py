import os
from typing import Optional, List, Dict

from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_complete, openai_embed
from lightrag.utils import setup_logger

setup_logger('lightrag', level='INFO')

WORKING_DIR = "./rag_storage"


class RAGPipeline:

    def __init__(self, working_dir: str = WORKING_DIR):

        self.working_dir = working_dir

        self.rag: Optional[LightRAG] = None

        if not os.path.exists(working_dir):
            os.mkdir(working_dir)

    async def initialize_rag(self):
        """Must call before using pipeline"""

        self.rag = LightRAG(
            working_dir=self.working_dir,
            embedding_func=openai_embed,
            llm_model_func=gpt_4o_complete,
        )


        await self.rag.initialize_storages()

        return self

    async def close_rag(self):
        if self.rag is not None:
            await self.rag.finalize_storages()


    async def add_documents(self, chunks: List[Dict]):
        """Insert document chunks into LightRAG"""

        if not chunks or self.rag is None:
            return

        texts = [chunk['text'] for chunk in chunks]

        await self.rag.ainsert(texts)

    async def search_similar_cases(self, query: str, mode: str = 'local'):
        """Search for similar medical cases"""
        if self.rag is None:
            raise RuntimeError("Pipeline not initialized. Call await pipeline.initialize() first.")


        result = await self.rag.aquery(
            query,
            param=QueryParam(mode=mode),
        )
        return result

    async def generate_diagnosis_support(self, query: str) -> str:
        """
        Generate structured diagnosis support using LightRAG hybrid retrieval.
        LightRAG handles context retrieval internally.
        """

        if self.rag is None:
            raise RuntimeError("Pipeline not initialized. Call await pipeline.initialize() first.")

        prompt = """
As a medical research assistant, analyze the following patient query and provide diagnosis support based on the medical literature.

Patient Query/Clinical Presentation:
{query}

Please provide:
1. Possible differential diagnoses based on the presentation
2. Key clinical findings that would help distinguish between possibilities
3. Recommended diagnostic tests or procedures
4. Relevant clinical guidelines or recent research findings
5. Important contraindications or precautions

Format your response in a clear, structured manner suitable for healthcare professionals.
"""

        response = await self.rag.aquery(
            query,
            param=QueryParam(mode="hybrid")
        )

        return response


    async def batch_insert_and_query(self, chunks: List[Dict], query: str):
        """Insert documents and immediately query — useful for one-shot pipelines"""

        await self.add_documents(chunks=chunks)
        return await self.generate_diagnosis_support(query=query)


    async def get_citations(self, chunks: List[Dict]) -> List[Dict]:
        """Extract citations from the retrieved documents"""
        citations = []
        seen = set()

        for chunk in chunks:
            metadata = chunk['metadata']
            source = metadata.get('source', '')

            if source and source not in seen:
                seen.add(source)

                citation = {
                    'source': source,
                    'type': metadata.get('type', 'unknown'),
                    'relevance_score': source.get('distance', 0)
                }

                if 'pmid' in metadata:
                    citation['pmid'] = metadata['pmid']
                    citation['title'] = metadata.get('title', '')
                    citation['journal'] = metadata.get('journal', '')

                citations.append(citation)


            return citations


        return citations
