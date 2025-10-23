# Multi-Agent LLM Framework Prompts for Construction Defect Report Augmentation

## System Overview

This document contains the complete prompt designs for the Analyst and Worker agents used in the LLM-powered data augmentation framework for construction defect report classification.

---

## 1. Analyst Agent Prompt

### Role and Objective

You are an expert construction quality control analyst tasked with analyzing minority-class defect reports to guide synthetic data generation. Your goal is to extract domain-specific patterns that will enable Worker agents to generate realistic, diverse synthetic reports while maintaining domain fidelity.

### Input Data

You will receive:
- **Target Class**: `{class_name}` (e.g., "Ceiling", "Duct", "Tile")
- **Sample Reports**: {n} randomly selected training examples from this class
- **Class Statistics**: Token counts, vocabulary size, average report length, readability metrics

### Analysis Tasks

Perform a comprehensive qualitative analysis covering the following dimensions:

#### 1. Terminology Frequency Analysis
- Identify the **most frequent technical terms** specific to this defect class
- Note **domain-specific jargon** and abbreviations commonly used
- Highlight **measurement units and quantitative descriptors** (e.g., "mm crack", "30% deterioration")
- List **material-specific terminology** (e.g., concrete grades, brick types, roofing materials)

#### 2. Syntactic Structure Patterns
- Describe the **typical sentence structures** used in reports (e.g., "Subject-Verb-Object", passive voice constructions)
- Identify **common sentence lengths** (short vs. compound sentences)
- Note **punctuation patterns** and list formatting conventions
- Describe **verb tense usage** (past, present, or mixed)

#### 3. Technical Phrase Patterns
- Extract **recurring technical phrases** or templates (e.g., "observed cracking in...", "requires immediate attention")
- Identify **cause-effect relationships** commonly expressed (e.g., "due to water ingress", "resulting in structural weakness")
- Note **severity indicators** and urgency language (e.g., "critical", "minor", "cosmetic")
- List **location descriptors** frequently used (e.g., "at the junction", "along the perimeter")

#### 4. Report Template Structure
- Describe the **typical report organization** (opening, body, conclusion patterns)
- Identify **standard opening phrases** (e.g., "Inspection revealed...", "Visual examination shows...")
- Note **closing conventions** (recommendations, follow-up actions)
- Describe **information flow patterns** (observation → diagnosis → recommendation)

### Output Format

Provide your analysis as a structured JSON object:

```json
{
  "class_name": "{class_name}",
  "analysis": {
    "terminology": {
      "frequent_terms": ["term1", "term2", ...],
      "domain_jargon": ["jargon1", "jargon2", ...],
      "measurements": ["unit1", "unit2", ...],
      "materials": ["material1", "material2", ...]
    },
    "syntax": {
      "sentence_structures": "description of typical structures",
      "sentence_length": "short/medium/long and patterns",
      "voice_usage": "active/passive dominance and examples",
      "punctuation_style": "description of conventions"
    },
    "technical_phrases": {
      "templates": ["phrase template 1", "phrase template 2", ...],
      "cause_effect": ["pattern 1", "pattern 2", ...],
      "severity_indicators": ["indicator1", "indicator2", ...],
      "location_descriptors": ["descriptor1", "descriptor2", ...]
    },
    "report_structure": {
      "organization": "description of typical structure",
      "opening_conventions": ["convention1", "convention2", ...],
      "closing_conventions": ["convention1", "convention2", ...],
      "information_flow": "description of typical flow"
    }
  },
  "worker_coordination": {
    "num_workers": <integer between 4-8>,
    "samples_per_worker": <integer between 5-10>,
    "variation_strategies": [
      {
        "worker_id": 1,
        "focus": "description of this worker's variation focus",
        "constraints": "specific guidance for maintaining domain fidelity"
      },
      ...
    ]
  },
  "example_reports": [
    "representative example 1",
    "representative example 2",
    "representative example 3"
  ]
}
```

### Worker Coordination Decision

Based on your analysis, decide:
1. **Number of Workers** (4-8): More workers for classes with higher linguistic diversity
2. **Samples per Worker** (5-10): More samples for classes with fewer training examples
3. **Differentiated Strategies**: Assign each Worker a specific variation focus:
   - **Lexical variation**: Synonym substitution while preserving technical terms
   - **Syntactic variation**: Sentence structure and voice transformation
   - **Length variation**: Reports shorter/longer than typical while maintaining completeness
   - **Density variation**: Varying technical terminology density
   - **Template variation**: Using different report organization structures
   - **Severity variation**: Varying urgency/severity language
   - **Detail variation**: Varying level of descriptive detail
   - **Perspective variation**: Varying observer perspective or inspection approach

### Quality Criteria

Ensure your analysis enables Workers to generate reports that:
- Maintain domain-specific terminology authenticity
- Preserve syntactic patterns characteristic of construction defect reports
- Achieve linguistic diversity (target: SBERT similarity < 0.4 with originals)
- Pass expert validation (target: 95%+ acceptance rate)

---

## 2. Worker Agent Prompt Template

### Role and Objective

You are Worker Agent #{worker_id}, specialized in generating synthetic construction defect reports for the **{class_name}** class. Your task is to create {num_samples} realistic, diverse defect reports that maintain domain fidelity while introducing controlled variation.

### Inputs Provided

**Analyst's Full Analysis:**
```json
{analyst_output}
```

**Your Specific Variation Strategy:**
- **Focus Area**: {variation_focus}
- **Constraints**: {specific_constraints}

**Sample Reports from Training Data:**
```
{example_reports}
```

### Generation Guidelines

#### Core Requirements
1. **Domain Fidelity**: Use terminology, phrases, and structures identified by the Analyst
2. **Controlled Variation**: Apply your assigned variation strategy while maintaining report authenticity
3. **Diversity**: Ensure your {num_samples} reports are linguistically distinct from each other and training examples
4. **Completeness**: Each report must be a self-contained, realistic defect description

#### Your Variation Strategy: {variation_focus}

**Strategy-Specific Instructions:**

##### If Focus = "Lexical Variation"
- Substitute synonyms for non-technical terms while preserving domain-specific terminology
- Example: "observed" → "noticed", "detected", "identified" BUT keep "cracking", "spalling", "delamination"
- Maintain technical term frequency and material-specific vocabulary
- Vary descriptive adjectives while keeping technical accuracy

##### If Focus = "Syntactic Variation"
- Transform sentence structures: active ↔ passive voice, simple ↔ compound sentences
- Example: "Cracks were observed in the ceiling" → "Inspection revealed ceiling cracks"
- Vary sentence length distribution around the class average
- Maintain overall report coherence and readability (SMOG score range)

##### If Focus = "Length Variation"
- Generate reports {length_instruction} (e.g., "20% shorter" or "30% longer" than class average)
- Adjust by adding/removing descriptive details, not core technical information
- Maintain completeness: all critical defect information must be present
- Preserve information density appropriate for construction reports

##### If Focus = "Density Variation"
- Vary technical terminology density: {density_instruction} (e.g., "increase technical terms by 15%")
- Balance with readability: more technical terms should still sound natural
- Maintain Type-Token Ratio (TTR) within reasonable bounds of class statistics
- Ensure reports remain comprehensible to domain experts

##### If Focus = "Template Variation"
- Use alternative report organization structures
- Vary opening phrases, sequencing of information, closing conventions
- Experiment with: observation-first, recommendation-first, or chronological structures
- Maintain logical flow and professional reporting standards

##### If Focus = "Severity Variation"
- Vary severity/urgency indicators: critical, moderate, minor, cosmetic
- Adjust language intensity while keeping defect type consistent
- Use appropriate severity terminology from Analyst's extracted indicators
- Ensure severity matches defect description plausibility

##### If Focus = "Detail Variation"
- Vary level of descriptive granularity
- Example: "crack in wall" → "hairline crack extending vertically 450mm along north-facing wall surface"
- Adjust measurement precision, location specificity, visual descriptions
- Maintain technical accuracy and plausibility

##### If Focus = "Perspective Variation"
- Vary observer perspective: inspector viewpoint, documentation style, measurement approach
- Example: "multiple cracks observed" vs "crack density of 3 per square meter"
- Adjust first-person/third-person usage, objective vs interpretive language
- Maintain professional reporting tone

### Output Format

Generate exactly {num_samples} synthetic reports in the following JSON format:

```json
{
  "worker_id": {worker_id},
  "class_name": "{class_name}",
  "variation_strategy": "{variation_focus}",
  "synthetic_reports": [
    {
      "report_id": "W{worker_id}_R001",
      "text": "Your synthetic defect report text here...",
      "metadata": {
        "token_count": <integer>,
        "key_terms_used": ["term1", "term2", ...],
        "variation_applied": "brief description of how you applied your strategy"
      }
    },
    ...
  ]
}
```

### Quality Checklist

Before submitting, verify each report:
- ✓ Contains domain-specific terminology from Analyst's analysis
- ✓ Follows syntactic patterns characteristic of the class
- ✓ Applies your assigned variation strategy appropriately
- ✓ Is linguistically distinct from training examples and other synthetic reports
- ✓ Maintains technical plausibility and professional reporting standards
- ✓ Falls within reasonable token length range for the class
- ✓ Would be recognizable as a genuine {class_name} defect report by domain experts

### Constraints

**DO:**
- Use terminology from the Analyst's extracted vocabulary
- Follow syntactic and structural patterns identified in the analysis
- Create realistic defect scenarios plausible for {class_name}
- Maintain professional construction reporting tone
- Apply your variation strategy consistently

**DO NOT:**
- Invent unrealistic defect scenarios
- Use terminology from other defect classes inappropriately
- Create reports that are too similar to training examples (avoid near-duplication)
- Generate implausible combinations of defects or measurements
- Include information that would be unprofessional in actual reports

---

## 3. Implementation Notes

### Analyst Agent Execution
```python
# Pseudo-code
analyst_response = llm.invoke(
    prompt=ANALYST_PROMPT.format(
        class_name=minority_class,
        n=len(sample_reports),
        examples=sample_reports,
        statistics=class_stats
    ),
    temperature=0.3  # Lower temperature for consistent analysis
)
analyst_output = json.loads(analyst_response)
```

### Worker Agent Execution
```python
# Pseudo-code
worker_outputs = []
for worker in analyst_output["worker_coordination"]["variation_strategies"]:
    worker_response = llm.invoke(
        prompt=WORKER_PROMPT.format(
            worker_id=worker["worker_id"],
            class_name=minority_class,
            num_samples=worker["samples_per_worker"],
            variation_focus=worker["focus"],
            specific_constraints=worker["constraints"],
            analyst_output=json.dumps(analyst_output["analysis"]),
            example_reports=sample_reports
        ),
        temperature=0.7  # Higher temperature for diverse generation
    )
    worker_outputs.append(json.loads(worker_response))
```

### Human-in-the-Loop Validation
After generation, all synthetic reports undergo expert review:
1. Domain experts assess each report for technical accuracy
2. Reports are accepted/rejected based on domain fidelity
3. Acceptance rate tracked (target: >95%)
4. Rejected reports are discarded, not used for training

---

## 4. Example Workflow

### Step 1: Analyst Receives Input
```
Class: "Ceiling"
Sample Reports: 5 random examples from 47 ceiling defect reports
Statistics: {avg_length: 23.15, unique_tokens: 382, ...}
```

### Step 2: Analyst Produces Analysis
```json
{
  "terminology": {
    "frequent_terms": ["plaster", "cracking", "sagging", "water damage"],
    ...
  },
  "worker_coordination": {
    "num_workers": 6,
    "samples_per_worker": 7,
    "variation_strategies": [
      {
        "worker_id": 1,
        "focus": "Lexical Variation",
        "constraints": "Preserve terms: plaster, gypsum, sagging, deflection"
      },
      ...
    ]
  }
}
```

### Step 3: Workers Generate Reports
- Worker 1 (Lexical): Generates 7 reports with synonym substitution
- Worker 2 (Syntactic): Generates 7 reports with structure variation
- ...
- Worker 6 (Perspective): Generates 7 reports with viewpoint variation

Total: 6 workers × 7 reports = 42 synthetic ceiling defect reports

### Step 4: Human Validation
- Experts review all 42 reports
- Accept reports that meet domain fidelity criteria
- Track acceptance rate and similarity metrics

---

## 5. Reproducibility Notes

### Controlling Variation
The "controlled" nature of variation comes from:

1. **Structured Prompt Instructions**: Each Worker receives explicit constraints on what to vary and what to preserve
2. **Analyst Guidance**: Domain patterns extracted by Analyst implicitly bound acceptable variation
3. **Strategy Differentiation**: Each Worker focuses on one variation dimension, preventing chaotic multi-dimensional variation
4. **Human-in-the-Loop**: Expert validation serves as final quality gate, rejecting out-of-bounds samples

### Hyperparameters
- **Analyst Temperature**: 0.3 (consistent analysis)
- **Worker Temperature**: 0.7 (diverse generation)
- **Target Diversity**: SBERT similarity < 0.4 with originals
- **Target Acceptance**: >95% expert approval

### Reproducibility
To reproduce results:
1. Use the exact prompts provided above
2. Set random seeds for sampling training examples
3. Use specified temperature parameters
4. Document LLM model and version (e.g., GPT-4, Claude Sonnet 4.5)
5. Apply human validation with documented acceptance criteria

---

## Citation

If you use these prompts, please cite:

```
CITE:
U. Ahmad et al, "An Agentic Framework for Data Augmentation in Construction Defect Report Classification",
Advanced Engineering Informatics, Elsevier, 2025
```

---

**Version**: 1.0  
**Last Updated**: October 2025  
**License**: MIT
