UPDATE experiments
SET extras = json_merge_patch(extras, $2)
WHERE
  uuid = $1 AND archived = FALSE;
