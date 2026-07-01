# Synthea-to-OMOP CDM ETL Data Pipeline

An Extract, Transform, Load (ETL) data engineering pipeline built with Python and `pandas` to migrate unstructured, messy synthetic clinical tracking records (Synthea specification) into standardized tables compliant with the **OHDSI OMOP Common Data Model (CDM) v6.0**.

## 🧬 The Clinical Database Challenge
Healthcare systems generate data using vastly disparate vocabularies. For instance, a clinician at one facility might log a diagnosis using a billing code (**ICD-10-CM: F43.10**), while a system tracker at another facility might log the same condition using an observation code (**SNOMED-CT: 254153009**). 

Conducting multi-center clinical research across these systems is nearly impossible without data harmonization. The **OMOP Common Data Model** solves this by establishing structural rules and a standardized vocabulary backend that maps disparate native terminologies down to unified global identifiers (`concept_id`).

## 🚀 The Data Engineering Solution
This pipeline ingests raw, source-specific demographic and clinical condition registries to execute data restructuring and semantic normalization across two core OMOP domain frameworks:

1. **`PERSON` Table Migration:**
   * Converts string-based GUID participant identifiers (`Id`) into robust, sequentially indexed numeric primary keys (`person_id`).
   * Parsed ISO timestamps (`BIRTHDATE`) to calculate integer-isolated metrics (`year_of_birth`, `month_of_birth`, `day_of_birth`).
   * Harmonized raw strings (e.g., `"M"`, `"F"`, `"white"`) down to official OHDSI Concept IDs (e.g., `8507`, `8532`, `8527`).

2. **`CONDITION_OCCURRENCE` Table Migration:**
   * Relational structural integration mapping participant string keys back to newly minted sequential surrogate integers.
   * Executed a complex relational data merge joining messy tracking codes with an OMOP crosswalk vocabulary layout.
   * Dynamically maps both ICD-10 billing strings and native SNOMED codes down to the unified **Standard SNOMED Definition for PTSD (`target_concept_id: 436073`)**.

## 📁 Repository Pipeline Layout
```text
├── source_data/
│   ├── raw_patients.csv          # Native unstructured demographic fields
│   ├── raw_conditions.csv        # Messy clinical logs with varying vocabularies
│   └── omop_vocabulary_map.csv   # OHDSI terminology crosswalk matrix
├── omop_output/
│   ├── omop_person.csv           # Structured OMOP CDM Person Table
│   └── omop_condition_occurrence.csv # Standardized Condition Occurrence Table
├── etl_pipeline.py               # Main Python Pandas mapping script
└── README.md                     # Project documentation
```

## 🛠️ Installation & Execution

### Prerequisites
* Python 3.8+
* Environment: [GitHub Codespaces](https://github.com) or a local workspace.

### 1. Ingest Data & Execute Mapping Logic
```bash
pip install pandas
python etl_pipeline.py
```

## 📊 Semantic Transformation Output Matrix
The success of this data pipeline is visible in the output folder. Notice how disparate source codes resolve to the exact same standardized definition column:

### Raw Inputs vs OMOP Standardized Targets:
* Source Entry 1: `CODE: 254153009` (SNOMED) \(\rightarrow\) `condition_concept_id: 436073`
* Source Entry 2: `CODE: F43.10` (ICD10CM) \(\rightarrow\) `condition_concept_id: 436073`

```text
condition_occurrence_id | person_id | condition_concept_id | condition_source_concept_id | condition_source_value
-----------------------------------------------------------------------------------------------------------------
1                       | 1         | 436073               | 436073                      | 254153009
2                       | 2         | 436073               | 45766186                    | F43.10
```
