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
