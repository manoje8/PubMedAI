from typing import Dict, List

from app.model.context_model import ClinicalContextType, UrgencyLevel, EngineeredContext
from shared.logger import logger

class ContextEngineer:

    def __init__(self):
        self.context_templates = self.__load_templates()
        self.specialty_keywords = self.__load_specialty_keyworks()

    def __load_templates(self):
        return {
            "emergency": {
                "primary_focus": ['airway', 'breathing', 'circulation', 'disability'],
                'time_sensitive': True,
                'format': 'rapid_sequence'
            },
            "diagnostic": {
                'primary_focus': ['differential', 'red_flags', 'typical_presentation'],
                'time_sensitive': False,
                'format': 'systematic_review'
            }
        }

    def __load_specialty_keyworks(self):
        return {
            "cardiology": {
                "keywords": ["chest pain", "palpitations", "dyspnea", "edema", "syncope", "orthopnea"],
                "weight": 1.5
            },
            "neurology": {
                "keywords": ["headache", "seizure", "weakness", "numbness", "dizziness"],
                "weight": 1.4
            },
            "infectious_disease": {
                "keywords": ["fever", "chills", "rash", "cough", "sore throat", "nausea", "vomiting", "loss of appetite"],
                "weight": 1.3
            },
            "pulmonology": {
                "keywords": ["cough", "wheezing", "shortness of breath", "hemoptysis", "cough with expectoration"],
                "weight": 1.3
            },
            "gastroenterology": {
                "keywords": ["abdominal pain", "nausea", "vomiting", "diarrhea"],
                "weight": 1.3
            }
        }

    def engineer_context(self, raw_input: Dict):
        logger.debug("Engineer critical context from raw input")

        context_type = self.__identify_context_type(raw_input)

        urgency = self.__assess_urgency(raw_input)

        structured_symptoms = self.__structure_symptoms(raw_input.get('symptoms', []))



    def __identify_context_type(self, raw_input: Dict) -> ClinicalContextType:
        symptoms = []

        for s in raw_input.get('symptoms', []):
            symptoms.append(s.get('description', '').lower())

        symptom_text = " ".join(symptoms)

        # Emergency
        emergency_keywords = [
            'unconscious', 'not breathing', 'severe bleeding',
            'stroke', 'heart attack', 'seizure'
        ]

        if any(keyword in symptom_text for keyword in emergency_keywords):
            return ClinicalContextType.EMERGENCY

        # Pediatrics
        age = raw_input.get('demographics', {}).get('age', 0)

        if 0 < age < 18:
            return ClinicalContextType.PEDIATRICS

        # Geriatric
        if age >= 65:
            return ClinicalContextType.GERIATRICS


        return ClinicalContextType.PRIMARY_CARE

    def __assess_urgency(self, raw_input: Dict) -> UrgencyLevel:
        vitals = raw_input.get('vital_signs', {})

        if (
            vitals.get('heart_rate', 0) > 140 or
            vitals.get('heart_rate', 0) < 40 or
            vitals.get('systolic_bp', 120) < 90 or
            vitals.get('oxygen_saturation', 100) < 90
        ):
            urgent_keywords = [
                'chest pain', 'difficulty breathing', 'severe pain',
                'confusion', 'unresponsiveness'
            ]

            symptom_text = " ".join([
                s.get('description', '').lower
                for s in raw_input.get('symptoms', [])
            ])


            if any(keyword in symptom_text for keyword in urgent_keywords):
                return UrgencyLevel.CRITICAL

        return UrgencyLevel.ROUTINE


    def __structure_symptoms(self, symptoms: List) -> List[Dict]:
        structured = []

        for symptom in symptoms:
            structured_symptom = {
                'description': symptom.get('description', ''),
                'onset': symptom.get('onset', 'unknown'),
                'duration': symptom.get('duration', 'unknown'),
                'severity': symptom.get('severity', 5),
                'character': symptom.get('character', ''),
                'modifying_factors': symptom.get('modifying_factors', ''),
                'associated_symptoms': symptom.get('associated', []),
                'clinical_significance': self.__self_symptoms_significance(symptom)
            }

            structured.append(structured_symptom)

        return structured

    async def __self_symptoms_significance(self, symptom: Dict) -> str:
        severity = symptom.get('severity', 5)

        if severity >= 8:
            return "high"
        elif severity >= 4:
            return "moderate"
        else:
            return "low"