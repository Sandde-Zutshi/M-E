import psycopg2

try:
    # Updated for Linux environment - you may need to adjust the username
    conn = psycopg2.connect(
        dbname="nutrition_db",
        user="ubuntu",        # your Linux username
        password="",          # usually empty for local Postgres
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("✅ Connected successfully to PostgreSQL!")
    print("PostgreSQL version:", version)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed:", e)