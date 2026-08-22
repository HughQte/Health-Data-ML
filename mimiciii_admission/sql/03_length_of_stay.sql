SELECT
    subject_id,
    hadm_id,
    admission_type,
    admittime,
    dischtime,

    ROUND(
        TIMESTAMPDIFF(HOUR, admittime, dischtime) / 24.0,
        2
    ) AS los_days

FROM mimiciii_admissions
ORDER BY los_days DESC;

SELECT
    admission_type,
    COUNT(*) AS admissions,

    ROUND(
        AVG(
            TIMESTAMPDIFF(HOUR, admittime, dischtime) / 24.0
        ),
        2
    ) AS avg_los_days

FROM mimiciii_admissions
GROUP BY admission_type
ORDER BY avg_los_days DESC;
