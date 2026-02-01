import duckdb
import sys

def main():
    try:
        conn = duckdb.connect()
        
        # 1. First command (-c)
        conn.execute("CREATE TEMP TABLE results AS SELECT * FROM read_json_auto('results/*.json');")
        
        # 2. Second command (-c) - The leaderboard query
        query = """
        SELECT
          id,
          ROUND(total, 2) AS "Total Score",
          ROUND(clarity, 2) AS Clarity,
          ROUND(logic, 2) AS Logic,
          ROUND(align, 2) AS Align,
          ROUND(flow, 2) AS Flow
        FROM (
          SELECT
            id, total, clarity, logic, align, flow,
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY total DESC) as rn
          FROM (
            SELECT
              t.participants.agent AS id,
              (SELECT AVG(r.totalScore) FROM UNNEST(t.results) AS _(r)) AS total,
              (SELECT AVG(r.clarityScore) FROM UNNEST(t.results) AS _(r)) AS clarity,
              (SELECT AVG(r.logicScore) FROM UNNEST(t.results) AS _(r)) AS logic,
              (SELECT AVG(r.internalAlignment) FROM UNNEST(t.results) AS _(r)) AS align,
              (SELECT AVG(r.narrativeFlow) FROM UNNEST(t.results) AS _(r)) AS flow
            FROM results t
          )
        )
        WHERE rn = 1
        ORDER BY "Total Score" DESC;
        """
        
        print("Testing CLI-style query sequence (via Python DuckDB)...\n")
        df = conn.execute(query).df()
        print(df.to_string(index=False))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
