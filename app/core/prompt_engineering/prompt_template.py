class PromptTemplate:
    CHAIN_OF_THOUGHT = """
    Let's approach this clinical case step by step:

    1. First, let's identify the key presenting symptoms and their characteristics:
       {symptoms_analysis}

    2. Based on these symptoms, let's consider the possible pathophysiological mechanisms:
       {pathophysiology}

    3. Now, let's generate a differential diagnosis list:
       {differential}

    4. For each possibility, let's evaluate the supporting and conflicting evidence:
       {evidence_evaluation}

    5. Finally, let's determine the most likely diagnosis and recommended next steps:
       {final_recommendation}
    """

    FEW_SHOT_EXAMPLES = """
    Here are similar clinical cases for reference:

    Example 1:
    Presentation: {example1_presentation}
    Working Diagnosis: {example1_diagnosis}
    Key Decision Factors: {example1_factors}
    Outcome: {example1_outcome}

    Example 2:
    Presentation: {example2_presentation}
    Working Diagnosis: {example2_diagnosis}
    Key Decision Factors: {example2_factors}
    Outcome: {example2_outcome}

    Now analyze the current case following this pattern.
    """

    STRUCTURED_OUTPUT = """
    Provide your analysis in the following structured format:

    DIFFERENTIAL DIAGNOSIS:
    1. [Diagnosis] - Probability: [High/Medium/Low]
       Supporting Evidence:
       - [Evidence 1]
       - [Evidence 2]
       Conflicting Evidence:
       - [Evidence 1]

    RECOMMENDED TESTS:
    - [Test 1] - Rationale: [Why this test]
    - [Test 2] - Rationale: [Why this test]

    TREATMENT CONSIDERATIONS:
    - Immediate: [Actions]
    - If confirmed: [Treatment]
    - If ruled out: [Alternatives]

    FOLLOW-UP PLAN:
    - [Timeframe]: [Action]
    - Red Flags: [Warning signs]
    """

    ROLE_BASED = """
    You are an expert {specialty} consultant reviewing this case.
    Consider the following specialty-specific aspects:

    Key {specialty} considerations:
    - {consideration1}
    - {consideration2}

    Red flags in {specialty}:
    - {redflag1}
    - {redflag2}

    Provide your {specialty} perspective on this case.
    """