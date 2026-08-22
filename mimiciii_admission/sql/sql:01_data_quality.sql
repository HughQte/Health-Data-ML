-- =====================================================
-- MIMIC-III Hospital Admissions Analysis
-- 01 - Data Quality Assessment
-- =====================================================

USE run;

-- 1. Preview the data
SELECT *
FROM mimiciii_admissions
ORDER BY subject_id
LIMIT 10;


-- 2. How many hospital admissions?
SELECT COUNT(*) AS total_admissions
FROM mimiciii_admissions;


-- 3. How many unique patients?
SELECT COUNT(DISTINCT subject_id) AS unique_patients
FROM mimiciii_admissions;


-- 4. Check whether admission IDs are duplicated
SELECT
    hadm_id,
    COUNT(*) AS count
FROM mimiciii_admissions
GROUP BY hadm_id
HAVING COUNT(*) > 1;


-- 5. Admission type distribution
SELECT
    admission_type,
    COUNT(*) AS admissions
FROM mimiciii_admissions
GROUP BY admission_type
ORDER BY admissions DESC;


-- 6. Check for invalid admission/discharge dates
SELECT
    subject_id,
    hadm_id,
    admittime,
    dischtime
FROM mimiciii_admissions
WHERE dischtime < admittime;


-- 7. Check important missing values
SELECT
    COUNT(*) AS total_rows,

    SUM(CASE WHEN subject_id IS NULL THEN 1 ELSE 0 END)
        AS missing_subject_id,

    SUM(CASE WHEN hadm_id IS NULL THEN 1 ELSE 0 END)
        AS missing_hadm_id,

    SUM(CASE WHEN admittime IS NULL THEN 1 ELSE 0 END)
        AS missing_admittime,

    SUM(CASE WHEN dischtime IS NULL THEN 1 ELSE 0 END)
        AS missing_dischtime,

    SUM(CASE WHEN admission_type IS NULL THEN 1 ELSE 0 END)
        AS missing_admission_type,

    SUM(CASE WHEN diagnosis IS NULL THEN 1 ELSE 0 END)
        AS missing_diagnosis

FROM mimiciii_admissions;
