from enum import Enum


class PromptStrategy(Enum):
    CHAIN_OF_THOUGHT='chain_of_thought'
    FEW_SHOT='few_shot'
    ZERO_SHOT='zero_shot'
    STRUCTURED_OUTPUT='structured_output'
    ROLE_BASED='role_based'
    CONSTRAINT_BASED='constraint_based'
