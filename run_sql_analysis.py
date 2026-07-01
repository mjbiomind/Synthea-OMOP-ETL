import sqlite3
import pandas as pd

def query_omop_database():
    print("📦 Spin up in-memory SQL Database engine...")
    # Create an active SQL database connection in your computer's memory
    conn = sqlite3.connect(":memory:")
    
    # 1. Load your newly generated OMOP CSV tables into real SQL tables
    print("Loading OMOP CSV sheets into SQL tables...")
    person_df = pd.read_csv("omop_output/omop_person.csv")
    condition_df = pd.read_csv("omop_output/omop_condition_occurrence.csv")
    
    person_df.to_sql("omop_person", conn, index=False, if_exists="replace")
    condition_df.to_sql("omop_condition_occurrence", conn, index=False, if_exists="replace")
    
    # 2. Read your advanced 'cohort_query.sql' file line by line
    print("Reading cohort_query.sql script...")
    with open("cohort_query.sql", "r") as sql_file:
        sql_script = sql_file.read()
        
    # 3. Execute the SQL query directly on your tables using Pandas!
    print("Executing relational query across OMOP tables...")
    result_df = pd.read_sql_query(sql_script, conn)
    
    print("\n=== SQL QUERY ACTIVE SURVEILLANCE COHORT ===")
    print(result_df.to_string(index=False))
    
    # Clean up the database connection
    conn.close()

if __name__ == "__main__":
    query_omop_database()
