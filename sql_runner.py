from utils import fetch_all

def execute_dynamic_sql(cursor, sql: str) -> list[dict]:
    cursor.execute(sql)
    while True:
        if cursor.description:
            return fetch_all(cursor)
        elif not cursor.nextset():
            return []
