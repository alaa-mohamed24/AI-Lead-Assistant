# responsible for data storage

import sqlite3
from src.ai_lead_assistant.models import Lead

DATABASE_NAME= "leads.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LEADS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            property_type TEXT,
            location TEXT,
            budget REAL,
            bedrooms INTEGER,
            finishing TEXT,
            timeline TEXT,
            intent TEXT,
            score INTEGER,
            classification TEXT,
            status TEXT DEFAULT 'PENDING',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
""")
    connection.commit()
    connection.close()


def save_lead(lead: Lead, score: int, classification: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leads (
        name,
        phone,
        property_type,
        location,
        budget,
        bedrooms,
        finishing,
        timeline,
        intent,
        score,
        classification
        ) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)    
""", (
    lead.name,
    lead.phone,
    lead.property_type.value,
    lead.location,
    lead.budget,
    lead.bedrooms,
    lead.finishing.value,
    lead.timeline,
    lead.intent,
    score,
    classification
)
)

    connection.commit()

    lead_id = cursor.lastrowid

    connection.close()    

    return lead_id


def get_leads():

    try:
        create_table() 
    except Exception:
        pass

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM LEADS
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.OperationalError:
        return []
    finally:
        connection.close()


def get_lead_by_id(lead_id: int):

    connection= get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM leads
        WHERE id = ?
""", (lead_id,))

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return dict(row)

def get_last_lead():
    connection = get_connection()

    connection.row_factory= sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM leads 
        ORDER BY id DESC
        LIMIT 1
""")

    row = cursor.fetchone()

    if row is None :
        return None

    return dict(row)


# def save_or_update_lead(lead: Lead, score:int, classification:str, status:str= "PENDING"):
#     create_table()
#     connection= get_connection()
#     cursor = connection.cursor()

#     prop_val= lead.property_type.value if hasattr(lead.property_type, 'value') else lead.property_type
#     fin_val = lead.finishing.value if hasattr(lead.finishing, 'value') else lead.finishing

#     cursor.execute("SELECT id FROM lead WHERE phone = ? AND phone IS  NOT NULL AND phone != '' ", (lead.phone,))
#     existing = cursor.fetchone()

#     if existing :
#         lead_id = existing[0]
        