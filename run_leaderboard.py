import json
import subprocess
import os
import sys

def main():
    config_path = 'LEADERBOARD_QUERY.json'
    # Use the verified absolute path to the DuckDB binary
    duckdb_exe = r'C:\Users\User\AppData\Local\Microsoft\WinGet\Links\duckdb.exe'
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)
        
    if not os.path.exists(duckdb_exe):
        # Fallback to 'duckdb' if absolute path is not found (unlikely)
        duckdb_exe = 'duckdb'
        
    # Definitive query for the new protocol schema
    definitive_query = """
    SELECT
      r.participants.agent AS id,
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
    FROM (SELECT UNNEST(results) AS r FROM results)
    GROUP BY id
    ORDER BY Total DESC, id;
    """
    
    try:
        query = definitive_query
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if config and len(config) > 0 and 'query' in config[0]:
                    query = config[0]['query']
                    print(f"Using query from {config_path}")
        
        print("Executing definitive aggregated leaderboard query...\n")
        
        # Build the command with three -c flags
        cmd = [
            duckdb_exe, 
            "-c", ".mode line",
            "-c", "CREATE TEMP TABLE results AS SELECT * FROM read_json_auto('results/*.json');",
            "-c", query
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error executing query:")
            print(result.stderr)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
