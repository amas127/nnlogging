CREATE TABLE IF NOT EXISTS experiments (
  uuid UUID NOT NULL,
  grp VARCHAR,
  exp VARCHAR NOT NULL,
  run VARCHAR,
  parents UUID [] DEFAULT [],
  status VARCHAR CHECK (
    status IN ('RUNNING', 'FAILED', 'SUCCESSFUL')
  ) DEFAULT 'RUNNING',
  archived BOOL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT now(),
  ended_at TIMESTAMP,
  duration INTERVAL GENERATED ALWAYS AS (ended_at - created_at),
  tags VARCHAR [] DEFAULT [],
  hparams JSON,
  summaries JSON,
  extras JSON,
  UNIQUE (grp, exp, run),
  PRIMARY KEY (uuid)
);


CREATE TABLE IF NOT EXISTS rawtracks (
  uuid UUID NOT NULL,
  step UBIGINT NOT NULL,
  met JSON,
  atf JSON,
  ctx JSON,
  ts TIMESTAMP DEFAULT now(),
  FOREIGN KEY (uuid) REFERENCES experiments (uuid)
);


CREATE INDEX IF NOT EXISTS idx_rawtracks_uuid ON rawtracks (uuid);
