import psycopg2

try:
    # Using the ubuntu user for this Linux environment
    conn = psycopg2.connect(
        dbname="nutrition_db",
        user="ubuntu",        # current Linux username
        host="localhost",
        port="5432"
        # No password needed - using trust authentication
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