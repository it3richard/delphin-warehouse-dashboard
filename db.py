import pandas as pd
import pyodbc

DB_DSN = "MOSSDB"
DB_USER = "esoro"
DB_PASSWORD = "esor4moss"

def load_data(sql):
    conn = pyodbc.connect(f"DSN={DB_DSN};UID={DB_USER};PWD={DB_PASSWORD}")
    cursor = conn.cursor()
    cursor.execute("SET SCHEMA ESO")  # nastavenie predvolenej schémy
    conn.commit()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df
