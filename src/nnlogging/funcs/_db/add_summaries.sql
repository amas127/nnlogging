UPDATE experiments
SET summaries = json_merge_patch(summaries, $2)
WHERE
  uuid = $1 AND archived = FALSE;
