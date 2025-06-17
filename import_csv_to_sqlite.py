import sqlite3
import pandas as pd


DATABASE_FILE = 'mlb_history.db'      
CSV_FILE = 'mlb_history_1902.csv'     
TABLE_NAME = 'mlb_history_1902'      

# Load CSV 
try:
    df = pd.read_csv(CSV_FILE)
    print(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns.")
    print(df.head())  
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# Connect to Database
try:
    conn = sqlite3.connect(DATABASE_FILE)
    print(f"Connected to database {DATABASE_FILE}")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# SQLite table
try:
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    print(f"Table '{TABLE_NAME}' written successfully.")
except Exception as e:
    print(f"Error writing to table: {e}")
    exit(1)

# Read back to verify
try:
    result = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} LIMIT 5", conn)
    print("Sample data from the database:")
    print(result)
except Exception as e:
    print(f"Error querying table: {e}")


conn.close()
print("Database connection closed.")
