UPDATE experiments
SET
  ended_at = now()
WHERE
  uuid = $1
  AND archived = FALSE;
