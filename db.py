import pandas as pd
import ibm_db
import ibm_db_dbi

# --- nastavenia DB ---
DB_HOST = "MOSSDB"       # IP alebo hostname DB
DB_PORT = "50000"
DB_NAME = "ESO"
DB_USER = "esoro"
DB_PASSWORD = "esor4moss"

def load_data(sql):
    conn_str = (
        f"DATABASE={DB_NAME};"
        f"HOSTNAME={DB_HOST};"
        f"PORT={DB_PORT};"
        f"PROTOCOL=TCPIP;"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
    )
    conn = ibm_db.connect(conn_str, "", "")
    
    # nastavenie predvolenej schémy
    ibm_db.exec_immediate(conn, "SET CURRENT SCHEMA ESO")
    
    df = pd.read_sql(sql, ibm_db_dbi.Connection(conn))
    ibm_db.close(conn)
    return df
