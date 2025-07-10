import psycopg2
import os

def test_postgresql_connection():
    """Test PostgreSQL connection with multiple configuration options."""
    
    # Configuration options to try
    configs = [
        {
            "dbname": "nutrition_db",
            "user": "sandeep",
            "password": "",
            "host": "localhost", 
            "port": "5432"
        },
        {
            "dbname": "nutrition_db",
            "user": os.getenv("USER", "postgres"),  # Use system username or postgres
            "password": "",
            "host": "localhost",
            "port": "5432"
        },
        {
            "dbname": "postgres",  # Try connecting to default postgres db first
            "user": os.getenv("USER", "postgres"),
            "password": "",
            "host": "localhost",
            "port": "5432"
        }
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n🔄 Attempt {i}: Testing connection with user '{config['user']}' to database '{config['dbname']}'...")
        
        try:
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            
            # Test the connection
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            
            # Check if nutrition_db exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'nutrition_db';")
            db_exists = cursor.fetchone()
            
            print("✅ Connected successfully to PostgreSQL!")
            print(f"PostgreSQL version: {version[0]}")
            print(f"Database 'nutrition_db' exists: {'Yes' if db_exists else 'No'}")
            
            cursor.close()
            conn.close()
            
            return True, config
            
        except psycopg2.Error as e:
            print(f"❌ Connection failed: {e}")
            continue
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue
    
    print("\n❌ All connection attempts failed!")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure PostgreSQL is installed and running")
    print("2. Check if the database 'nutrition_db' exists")
    print("3. Verify the username and permissions")
    print("4. On Linux, you might need to install PostgreSQL:")
    print("   sudo apt-get update && sudo apt-get install postgresql postgresql-contrib")
    
    return False, None

def create_nutrition_database():
    """Create the nutrition_db database and basic table structure."""
    try:
        # Connect to postgres default database to create nutrition_db
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("USER", "postgres"),
            password="",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True  # Required for CREATE DATABASE
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'nutrition_db';")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE nutrition_db;")
            print("✅ Created database 'nutrition_db'")
        else:
            print("ℹ️  Database 'nutrition_db' already exists")
        
        cursor.close()
        conn.close()
        
        # Now connect to the nutrition_db and create table
        conn = psycopg2.connect(
            dbname="nutrition_db",
            user=os.getenv("USER", "postgres"),
            password="",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        # Create nutrition_data table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS nutrition_data (
            id SERIAL PRIMARY KEY,
            staff_id VARCHAR(100) NOT NULL,
            household_id VARCHAR(100) NOT NULL,
            language VARCHAR(50) NOT NULL,
            child_name VARCHAR(255) NOT NULL,
            child_age_months INTEGER NOT NULL,
            height_cm DECIMAL(5,2) NOT NULL,
            weight_kg DECIMAL(5,2) NOT NULL,
            photo VARCHAR(255),
            audio_confirmation VARCHAR(255),
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Created/verified nutrition_data table")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database/table: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing PostgreSQL Connection...")
    print("=" * 50)
    
    success, working_config = test_postgresql_connection()
    
    if success:
        print(f"\n🎉 Connection successful with config: {working_config}")
        
        # Ask user if they want to create the database structure
        create_db = input("\n❓ Would you like to create the nutrition_db database and table structure? (y/n): ")
        if create_db.lower() in ['y', 'yes']:
            print("\n🔨 Creating database structure...")
            if create_nutrition_database():
                print("\n✅ Database setup complete! You can now use PostgreSQL with your nutrition app.")
            else:
                print("\n❌ Database setup failed. Please check the errors above.")
    else:
        print("\n❌ Unable to establish PostgreSQL connection. Please check your PostgreSQL installation and configuration.")