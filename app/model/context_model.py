from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List


class ClinicalContextType(Enum):
    EMERGENCY = "emergency"
    PRIMARY_CARE = "primary_care"
    SPECIALITY = "speciality"
    PEDIATRICS = "pediatrics"
    GERIATRICS = "geriatrics"


class UrgencyLevel(Enum):
    CRITICAL = "critical"
    URGENT = "urgent"
    ROUTINE = "routine"
    FOLLOW_UP = "follow_up"


@dataclass
class EngineeredContext:
    demographics: Dict[str, Any]
    symptoms: List[Dict[str, Any]]
    medical_history: Dict[str, List[str]]
    medications: List[Dict[str, Any]]
    vital_signs: Dict[str, Any]
    lab_results: Dict[str, Any]
    risk_factors: List[str]
    context_type: ClinicalContextType
    urgency: UrgencyLevel
    search_query: str
    summary: str
    warnings: List[str] = field(default_factory=list)
    relevant_specialities: List[Dict] = field(default_factory=list)
