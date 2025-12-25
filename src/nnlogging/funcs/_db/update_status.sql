UPDATE experiments
SET
  status = $2
WHERE
  uuid = $1
  AND archived = FALSE;
