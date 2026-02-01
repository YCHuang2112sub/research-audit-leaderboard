import duckdb
import pandas as pd

# Set display options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def main():
    try:
        # Connect to an in-memory database
        conn = duckdb.connect()
        
        print("--- Testing User's Query (Fixed) ---")
        # The user's query fails if the table is named 'results' and the column is also 'results'.
        # We also need to account for how DuckDB reads the JSON.
        query = """
        SELECT 
            t.agent AS "Agent", 
            t.totalScore AS "Total score" 
        FROM (
            SELECT 
                participants.agent AS agent, 
                res.totalScore, 
                ROW_NUMBER() OVER (PARTITION BY participants.agent ORDER BY res.totalScore DESC) AS rn 
            FROM read_json_auto('results/*.json') 
            CROSS JOIN UNNEST(results) AS r(res)
        ) AS t 
        WHERE t.rn = 1 
        ORDER BY "Total score" DESC;
        """
        
        df = conn.execute(query).df()
        
        print("\n--- Result ---")
        print(df)
        
        # Also print the raw schema to see why it might have failed before
        print("\n--- Raw Schema Discovery ---")
        schema_df = conn.execute("SELECT * FROM read_json_auto('results/*.json') LIMIT 1").df()
        print("Columns:", schema_df.columns.tolist())
        print("Participants Column Sample:", schema_df['participants'].iloc[0])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

