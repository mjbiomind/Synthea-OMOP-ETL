import pandas as pd
import pytest
import io

# Mock source data for testing
mock_conditions_csv = """START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION
2024-01-10,2024-01-15,p_001,enc_101,254153009,Post-traumatic stress disorder
2025-06-14,,p_002,enc_202,F43.10,Post-traumatic stress disorder unspecified"""

mock_vocab_csv = """source_code,source_vocabulary,source_concept_id,target_concept_id,target_concept_name,target_domain
254153009,SNOMED,436073,436073,Posttraumatic stress disorder,Condition
F43.10,ICD10CM,45766186,436073,Posttraumatic stress disorder,Condition"""

def test_omop_semantic_mapping():
    """Test that different source vocabularies successfully map to the standard OMOP concept ID."""
    # Read our text blocks as dataframes
    raw_conditions = pd.read_csv(io.StringIO(mock_conditions_csv))
    vocab_map = pd.read_csv(io.StringIO(mock_vocab_csv))
    
    # Force string types to prevent mismatches
    raw_conditions["CODE"] = raw_conditions["CODE"].astype(str)
    vocab_map["source_code"] = vocab_map["source_code"].astype(str)
    
    # Execute the exact merge logic from your pipeline
    mapped_df = raw_conditions.merge(vocab_map, left_on="CODE", right_on="source_code", how="left")
    
    # ASSERTIONS: Verify that both rows correctly resolved to the target PTSD code 436073
    assert len(mapped_df) == 2
    assert mapped_df.loc[0, "target_concept_id"] == 436073
    assert mapped_df.loc[1, "target_concept_id"] == 436073
    print("\n✅ Unit Test Passed: Semantic mapping successfully verified!")
