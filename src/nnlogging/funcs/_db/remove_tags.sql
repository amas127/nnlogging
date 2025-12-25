UPDATE experiments
SET tags = list_filter(tags, x -> NOT list_contains($2, x))
WHERE uuid = $1 AND archived = FALSE;
