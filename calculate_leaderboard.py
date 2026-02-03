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
          ROUND(totalScore, 2) AS "Total",
          ROUND(clarityScore, 2) AS "Clarity",
          ROUND(logicScore, 2) AS "Logic",
          ROUND(internalAlignment, 2) AS "Align",
          ROUND(narrativeFlow, 2) AS "Flow",
          ROUND(r2n_retention, 2) AS "R2N Ret",
          ROUND(r2n_authenticity, 2) AS "R2N Auth",
          ROUND(r2s_retention, 2) AS "R2S Ret",
          ROUND(r2s_authenticity, 2) AS "R2S Auth",
          ROUND(n2s_retention, 2) AS "N2S Ret",
          ROUND(n2s_authenticity, 2) AS "N2S Auth"
        FROM (
          SELECT
            id, totalScore, clarityScore, logicScore, internalAlignment, narrativeFlow,
            r2n_retention, r2n_authenticity, r2s_retention, r2s_authenticity, n2s_retention, n2s_authenticity,
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY totalScore DESC) as rn
          FROM (
            SELECT
              t.participants.agent AS id,
              t.averages.totalScore,
              t.averages.clarityScore,
              t.averages.logicScore,
              t.averages.internalAlignment,
              t.averages.narrativeFlow,
              t.averages.r2n_retention,
              t.averages.r2n_authenticity,
              t.averages.r2s_retention,
              t.averages.r2s_authenticity,
              t.averages.n2s_retention,
              t.averages.n2s_authenticity
            FROM results t
          )
        )
        WHERE rn = 1
        ORDER BY "Total" DESC;
        """
        
        print("Testing CLI-style query sequence (via Python DuckDB)...\n")
        df = conn.execute(query).df()
        print(df.to_string(index=False))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
