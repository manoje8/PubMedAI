from typing import Dict, List, Optional


class PromptMemory:
    def __init__(self):
        self.successful_prompt = []
        self.case_examples = []

    def _load_case_examples(self) -> List[Dict]:
        return [
            {
                'presentation': '45-year-old male with acute onset chest pain, radiating to left arm, associated with diaphoresis and nausea. ECG shows ST elevations in V2-V4.',
                'diagnosis': 'STEMI',
                'key_factors': 'Typical cardiac symptoms with ECG changes',
                'outcome': 'Emergent catheterization, stent placed'
            },
            {
                'presentation': '32-year-old female with recurrent headaches, throbbing, unilateral, photophobia, nausea. No focal deficits.',
                'diagnosis': 'Migraine with aura',
                'key_factors': 'Classic migraine features, normal neuro exam',
                'outcome': 'Responded to triptans'
            }
        ]

    def get_similar_cases(self, query: str, specialty: Optional[str], k: int = 2) -> List[Dict]:
        # TODO: embeddings for similarity search
        return self.case_examples[:k]