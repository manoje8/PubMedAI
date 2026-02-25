from app.core.prompt_engineering.prompt_memory import PromptMemory
from app.core.prompt_engineering.prompt_template import PromptTemplate
from app.model.prompt_model import PromptStrategy


class PromptEngineer:

    def __init__(self):
        self.strategies = self.__initialize_strategies()
        self.templates = PromptTemplate()
        self.memory = PromptMemory()

    def __initialize_strategies(self):
        return {
            PromptStrategy.CHAIN_OF_THOUGHT: {
                'weight': 1.2,
                'temperature': 0.3,
                'max_tokens': 1000
            },
            PromptStrategy.FEW_SHOT: {
                'weight': 1.1,
                'temperature': 0.4,
                'max_tokens': 800
            },
            PromptStrategy.STRUCTURED_OUTPUT: {
                'weight': 1.0,
                'temperature': 0.2,
                'max_tokens': 600
            }
        }