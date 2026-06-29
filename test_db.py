from sqlalchemy import text

from app.database.session import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))

    print(result.fetchone()[0])

print(" Database Connected Successfully")