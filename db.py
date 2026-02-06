import pandas as pd
import ibm_db
import ibm_db_dbi

# --- nastavenia DB ---
DB_HOST = "tvoj_host"       # IP alebo hostname DB
DB_PORT = "50000"            # port DB2
DB_NAME = "ESO"              # názov databázy / schémy
DB_USER = "esoro"
DB_PASSWORD = "esor4moss"

def load_data(sql):
    """
    Funkcia pre načítanie dát z DB2 do pandas DataFrame
    Schéma ESO sa nastaví hneď po pripojení.
    """
    # connection string pre IBM DB2
    conn_str = (
        f"DATABASE={DB_NAME};"
        f"HOSTNAME={DB_HOST};"
        f"PORT={DB_PORT};"
        f"PROTOCOL=TCPIP;"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
    )
    
    # pripojenie
    conn = ibm_db.connect(conn_str, "", "")
    
    # nastavenie predvolenej schémy
    ibm_db.exec_immediate(conn, "SET CURRENT SCHEMA ESO")
    
    # pandas DataFrame z SQL query
    pdf = pd.read_sql(sql, ibm_db_dbi.Connection(conn))
    
    # zatvorenie spojenia
    ibm_db.close(conn)
    
    return pdf
