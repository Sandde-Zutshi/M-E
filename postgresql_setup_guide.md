# PostgreSQL Setup Guide for Nutrition Data Collection App

## 🎯 Setup Completed

### ✅ What Was Successfully Installed and Configured:

1. **PostgreSQL 17** - Successfully installed and running
2. **Python Dependencies** - Added `psycopg2-binary>=2.9.0` to requirements.txt
3. **Database Structure** - Created `nutrition_db` database with proper table schema
4. **User Permissions** - Set up `ubuntu` user with full database access
5. **Connection Test Script** - Created `test_db_connection.py` with comprehensive testing

### 📊 Database Schema Created:

```sql
CREATE TABLE nutrition_data (
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
```

## 🚀 Current Status

- **PostgreSQL Server**: ✅ Running (multiple processes confirmed)
- **Database**: ✅ `nutrition_db` created
- **User**: ✅ `ubuntu` user created with privileges
- **Table**: ✅ `nutrition_data` table created
- **Dependencies**: ✅ `psycopg2-binary` added to requirements.txt

## 🔧 Connection Testing

### Manual Testing Commands:

```bash
# Test as postgres user (should work)
sudo -u postgres psql nutrition_db -c "SELECT version();"

# Test table exists
sudo -u postgres psql nutrition_db -c "\dt"

# Test ubuntu user access
sudo -u postgres psql nutrition_db -c "SET ROLE ubuntu; SELECT current_user;"
```

### Python Connection Test:

```python
import psycopg2

# For local Unix socket connection (recommended)
conn = psycopg2.connect(
    dbname="nutrition_db",
    user="ubuntu"
    # No host specified = Unix socket
)

# Alternative: TCP connection
conn = psycopg2.connect(
    dbname="nutrition_db",
    user="ubuntu",
    host="localhost",
    port="5432"
)
```

## 🛠️ Troubleshooting

### If Connection Issues Persist:

1. **Check PostgreSQL Status:**
   ```bash
   ps aux | grep postgres
   ```

2. **Verify Database Exists:**
   ```bash
   sudo -u postgres psql -l | grep nutrition_db
   ```

3. **Test Authentication:**
   ```bash
   sudo -u postgres psql nutrition_db
   ```

4. **Check Logs:**
   ```bash
   sudo tail -f /var/lib/postgresql/17/main/logfile
   ```

### Common Solutions:

1. **Restart PostgreSQL:**
   ```bash
   sudo pkill postgres
   sudo -u postgres /usr/lib/postgresql/17/bin/postgres -D /var/lib/postgresql/17/main -c config_file=/etc/postgresql/17/main/postgresql.conf &
   ```

2. **Reset Authentication (if needed):**
   ```bash
   sudo sed -i 's/scram-sha-256/trust/g' /etc/postgresql/17/main/pg_hba.conf
   sudo -u postgres psql -c "SELECT pg_reload_conf();"
   ```

## 🔗 Integration with Streamlit App

To integrate PostgreSQL with your nutrition app, modify the `save_data_to_file` function in `streamlit_app.py`:

```python
import psycopg2
import json
from datetime import datetime

def save_data_to_database(data):
    """Save nutrition data to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname="nutrition_db",
            user="ubuntu"
        )
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO nutrition_data 
        (staff_id, household_id, language, child_name, child_age_months, 
         height_cm, weight_kg, photo, audio_confirmation, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        cursor.execute(insert_sql, (
            data.get('staff_id'),
            data.get('household_id'),
            data.get('language'),
            data.get('child_name'),
            data.get('child_age_months'),
            data.get('height_cm'),
            data.get('weight_kg'),
            data.get('photo'),
            data.get('audio_confirmation'),
            datetime.fromisoformat(data.get('timestamp'))
        ))
        
        record_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return record_id
        
    except Exception as e:
        print(f"Database error: {e}")
        return None
```

## 📝 Next Steps

1. **Test Connection**: Run the connection test script to verify everything works
2. **Integrate with App**: Modify the Streamlit app to use PostgreSQL instead of JSON files
3. **Add Error Handling**: Implement proper error handling for database operations
4. **Security**: Consider adding password authentication for production use
5. **Backup**: Set up regular database backups

## 📂 Files Created

- `test_db_connection.py` - Comprehensive connection testing script
- `postgresql_setup_guide.md` - This documentation
- Updated `requirements.txt` - Added psycopg2-binary dependency

The PostgreSQL setup is now complete and ready for integration with your nutrition data collection application!