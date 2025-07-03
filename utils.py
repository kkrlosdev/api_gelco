from datetime import *
from decimal import Decimal

def fetch_all(cursor) -> list[dict]:
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    def serialize(value):
        if isinstance(value, (datetime, date)):
            return value.strftime('%Y-%m-%d')
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, str):
            return value.strip()
        return value

    return [
        {col: serialize(val) for col, val in zip(columns, row)}
        for row in rows
    ]

def fetch_one(cursor) -> dict:
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row) if row else None)
