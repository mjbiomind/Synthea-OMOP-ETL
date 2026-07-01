-- Advanced OMOP Cohort Selection Query
-- Objective: Identify patients diagnosed with PTSD who are still actively being monitored.

SELECT 
    p.person_id,
    p.person_source_value AS patient_guid,
    p.year_of_birth,
    p.gender_source_value AS gender,
    co.condition_source_value AS raw_icd_snomed_code,
    co.condition_start_date,
    -- Label patients as 'Active' if there is no recorded diagnosis end date
    CASE 
        WHEN co.condition_end_date IS NULL OR co.condition_end_date = '' THEN 'Active Surveillance'
        ELSE 'Resolved / Discharged'
    END AS clinical_status
FROM 
    omop_person p
INNER JOIN 
    omop_condition_occurrence co ON p.person_id = co.person_id
WHERE 
    -- 436073 is the global standard OMOP concept ID for PTSD
    co.condition_concept_id = 436073
ORDER BY 
    co.condition_start_date DESC;
