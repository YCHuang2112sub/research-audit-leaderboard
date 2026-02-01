import duckdb
import sys
import pandas as pd

def main():
    try:
        conn = duckdb.connect()
        
        # Updated query to exclude the Auditor (green_agent)
        query = """
        SELECT
          id,
          ROUND(total, 2) AS "Total Score",
          ROUND(clarity, 2) AS Clarity,
          ROUND(logic, 2) AS Logic,
          ROUND(align, 2) AS Align,
          ROUND(flow, 2) AS Flow,
          ROUND(r2n_ret, 2) AS "R2N Ret",
          ROUND(r2s_ret, 2) AS "R2S Ret",
          ROUND(n2s_ret, 2) AS "N2S Ret"
        FROM (
          SELECT
            id, total, clarity, logic, align, flow, r2n_ret, r2s_ret, n2s_ret,
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY total DESC) as rn
          FROM (
            -- Only count the agents being audited (participants.agent)
            -- Exclude the Auditor (green_agent)
            SELECT
              t.participants.agent AS id,
              (SELECT AVG(r.totalScore) FROM UNNEST(t.results) AS _(r)) AS total,
              (SELECT AVG(r.clarityScore) FROM UNNEST(t.results) AS _(r)) AS clarity,
              (SELECT AVG(r.logicScore) FROM UNNEST(t.results) AS _(r)) AS logic,
              (SELECT AVG(r.internalAlignment) FROM UNNEST(t.results) AS _(r)) AS align,
              (SELECT AVG(r.narrativeFlow) FROM UNNEST(t.results) AS _(r)) AS flow,
              (SELECT AVG(r.r2n_retention) FROM UNNEST(t.results) AS _(r)) AS r2n_ret,
              (SELECT AVG(r.r2s_retention) FROM UNNEST(t.results) AS _(r)) AS r2s_ret,
              (SELECT AVG(r.n2s_retention) FROM UNNEST(t.results) AS _(r)) AS n2s_ret
            FROM read_json_auto('results/*.json') t
          )
        )
        WHERE rn = 1
        ORDER BY "Total Score" DESC;
        """
        
        print("Refining Leaderboard (Excluding Auditor Agent)...\n")
        df = conn.execute(query).df()
        
        if df.empty:
            print("No results found in results/*.json")
        else:
            print(df.to_string(index=False))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
