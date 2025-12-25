UPDATE experiments
SET
  archived = TRUE
WHERE
  uuid = $1;
