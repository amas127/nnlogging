UPDATE experiments
SET hparams = json_merge_patch(hparams, $2)
WHERE
  uuid = $1 AND archived = FALSE;
