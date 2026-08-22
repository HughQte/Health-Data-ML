-- =============================================
-- MIMIC-III Admissions Data Quality Assessment
-- =============================================

-- Number of admissions
SELECT COUNT(*) AS total_admissions
FROM run.mimiciii_admissions;


-- Number of unique patients
SELECT COUNT(DISTINCT subject_id) AS unique_patients
FROM run.mimiciii_admissions;


-- Check for duplicated admission IDs
SELECT
    hadm_id,
    COUNT(*) AS n
FROM run.mimiciii_admissions
GROUP BY hadm_id
HAVING COUNT(*) > 1;


-- Check admission type distribution
SELECT
    admission_type,
    COUNT(*) AS admissions
FROM run.mimiciii_admissions
GROUP BY admission_type
ORDER BY admissions DESC;