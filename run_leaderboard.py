import json
import subprocess
import os
import sys

def main():
    config_path = 'leaderboard_config.json'
    # Use the verified absolute path to the DuckDB binary
    duckdb_exe = r'C:\Users\User\AppData\Local\Microsoft\WinGet\Links\duckdb.exe'
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)
        
    if not os.path.exists(duckdb_exe):
        # Fallback to 'duckdb' if absolute path is not found (unlikely)
        duckdb_exe = 'duckdb'
        
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Extract the query from the first name/query object
        query = config[0]['query']
        
        print(f"Executing two-command sequence from {config_path}...\n")
        
        # Build the command with three -c flags
        # 1. Set output mode to line (vertical) for better readability
        # 2. Create the temp table
        # 3. Run the query
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
