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
          participants.agent AS id,
          ROUND(AVG(r.averages.totalScore), 2) AS Total,
          ROUND(AVG(r.averages.clarityScore), 2) AS Clarity,
          ROUND(AVG(r.averages.logicScore), 2) AS Logic,
          ROUND(AVG(r.averages.internalAlignment), 2) AS Align,
          ROUND(AVG(r.averages.narrativeFlow), 2) AS Flow,
          ROUND(AVG(r.averages.r2n_retention), 2) AS R2N_Ret,
          ROUND(AVG(r.averages.r2n_authenticity), 2) AS R2N_Auth,
          ROUND(AVG(r.averages.r2s_retention), 2) AS R2S_Ret,
          ROUND(AVG(r.averages.r2s_authenticity), 2) AS R2S_Auth,
          ROUND(AVG(r.averages.n2s_retention), 2) AS N2S_Ret,
          ROUND(AVG(r.averages.n2s_authenticity), 2) AS N2S_Auth
        FROM (SELECT participants, UNNEST(results) AS r FROM results)
        GROUP BY id
        ORDER BY Total DESC, id;
        """
        
        print("Testing CLI-style query sequence (via Python DuckDB)...\n")
        df = conn.execute(query).df()
        print(df.to_string(index=False))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
