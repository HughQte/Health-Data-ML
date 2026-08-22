USE run;

-- Admissions by type
SELECT
    admission_type,
    COUNT(*) AS admissions
FROM mimiciii_admissions
GROUP BY admission_type
ORDER BY admissions DESC;
