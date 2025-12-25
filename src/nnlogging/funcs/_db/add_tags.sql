UPDATE experiments
SET
  tags = list_sort(list_distinct(list_concat(tags, $2)))
WHERE
  uuid = $1 AND archived = FALSE;
