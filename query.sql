-- Definitive query for the new protocol schema
-- Aggregates metrics by the audited agent ID (participants.agent)
SELECT
  t.participants.agent AS id,
  ROUND(AVG(t.averages.totalScore), 2) AS "Total",
  ROUND(AVG(t.averages.clarityScore), 2) AS "Clarity",
  ROUND(AVG(t.averages.logicScore), 2) AS "Logic",
  ROUND(AVG(t.averages.internalAlignment), 2) AS "Align",
  ROUND(AVG(t.averages.narrativeFlow), 2) AS "Flow",
  ROUND(AVG(t.averages.r2n_retention), 2) AS "R2N Ret",
  ROUND(AVG(t.averages.r2n_authenticity), 2) AS "R2N Auth",
  ROUND(AVG(t.averages.r2s_retention), 2) AS "R2S Ret",
  ROUND(AVG(t.averages.r2s_authenticity), 2) AS "R2S Auth",
  ROUND(AVG(t.averages.n2s_retention), 2) AS "N2S Ret",
  ROUND(AVG(t.averages.n2s_authenticity), 2) AS "N2S Auth"
FROM read_json_auto('results/*.json') t
WHERE t.averages IS NOT NULL
GROUP BY id
ORDER BY "Total" DESC, id;
