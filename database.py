import sqlite3
import json
import requests
from datetime import datetime
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, D1_DATABASE_ID, USE_LOCAL_DB, LOCAL_DB_PATH

def init_db():
    """Initialize the database with required tables"""
    if USE_LOCAL_DB:
        _init_local_db()
    else:
        _init_d1_db()

def _init_local_db():
    """Initialize local SQLite database"""
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            habits_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, entry_date)
        )
    ''')
    
    conn.commit()
    conn.close()

def _init_d1_db():
    """Initialize Cloudflare D1 database"""
    try:
        # This would be the D1 initialization
        # For now, we'll handle it when making queries
        pass
    except Exception as e:
        print(f"Error initializing D1: {e}")

def get_user_entry(username, entry_date):
    """Get a user's entry for a specific date"""
    if USE_LOCAL_DB:
        return _get_user_entry_local(username, entry_date)
    else:
        return _get_user_entry_d1(username, entry_date)

def _get_user_entry_local(username, entry_date):
    """Get entry from local database"""
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT entry_date, habits_data FROM habit_entries WHERE username = ? AND entry_date = ?',
            (username, entry_date)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "date": result[0],
                "habits": json.loads(result[1])
            }
        return None
    except Exception as e:
        print(f"Error fetching entry: {e}")
        return None

def _get_user_entry_d1(username, entry_date):
    """Get entry from Cloudflare D1"""
    try:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/d1/database/{D1_DATABASE_ID}/query"
        
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "sql": "SELECT entry_date, habits_data FROM habit_entries WHERE username = ? AND entry_date = ?",
            "params": [username, entry_date]
        }
        
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        if result.get('success') and result.get('result'):
            rows = result['result'][0].get('results', [])
            if rows:
                return {
                    "date": rows[0]["entry_date"],
                    "habits": json.loads(rows[0]["habits_data"])
                }
        else:
            print(f"D1 Read Error: {result.get('errors', 'Unknown error')}")
        
        return None
    except Exception as e:
        print(f"Error fetching entry from D1: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_entry(username, entry_date, habits_data):
    """Save or update a user's entry for a date"""
    if USE_LOCAL_DB:
        return _save_entry_local(username, entry_date, habits_data)
    else:
        return _save_entry_d1(username, entry_date, habits_data)

def _save_entry_local(username, entry_date, habits_data):
    """Save entry to local database"""
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        cursor = conn.cursor()
        
        habits_json = json.dumps(habits_data)
        
        cursor.execute('''
            INSERT INTO habit_entries (username, entry_date, habits_data)
            VALUES (?, ?, ?)
            ON CONFLICT(username, entry_date)
            DO UPDATE SET habits_data = ?, updated_at = CURRENT_TIMESTAMP
        ''', (username, entry_date, habits_json, habits_json))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving entry: {e}")
        return False

def _save_entry_d1(username, entry_date, habits_data):
    """Save entry to Cloudflare D1"""
    try:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/d1/database/{D1_DATABASE_ID}/query"
        
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        habits_json = json.dumps(habits_data)
        
        # First, try to check if entry exists
        check_data = {
            "sql": "SELECT id FROM habit_entries WHERE username = ? AND entry_date = ?",
            "params": [username, entry_date]
        }
        
        check_response = requests.post(url, json=check_data, headers=headers)
        check_result = check_response.json()
        
        entry_exists = False
        if check_result.get('success') and check_result.get('result'):
            results = check_result['result'][0].get('results', [])
            entry_exists = len(results) > 0
        
        # Use appropriate SQL based on whether entry exists
        if entry_exists:
            # Update existing entry
            sql = """
                UPDATE habit_entries 
                SET habits_data = ?, updated_at = CURRENT_TIMESTAMP
                WHERE username = ? AND entry_date = ?
            """
            params = [habits_json, username, entry_date]
        else:
            # Insert new entry
            sql = """
                INSERT INTO habit_entries (username, entry_date, habits_data)
                VALUES (?, ?, ?)
            """
            params = [username, entry_date, habits_json]
        
        write_data = {
            "sql": sql,
            "params": params
        }
        
        response = requests.post(url, json=write_data, headers=headers)
        result = response.json()
        
        if not result.get('success'):
            error_msg = result.get('errors', ['Unknown error'])[0] if result.get('errors') else 'Unknown error'
            print(f"D1 Write Error: {error_msg}")
            print(f"Response: {result}")
        
        return result.get('success', False)
    except Exception as e:
        print(f"Error saving entry to D1: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_all_entries(username):
    """Get all entries for a user"""
    if USE_LOCAL_DB:
        return _get_all_entries_local(username)
    else:
        return _get_all_entries_d1(username)

def _get_all_entries_local(username):
    """Get all entries from local database"""
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT entry_date, habits_data FROM habit_entries WHERE username = ? ORDER BY entry_date DESC',
            (username,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    except Exception as e:
        print(f"Error fetching all entries: {e}")
        return []

def _get_all_entries_d1(username):
    """Get all entries from Cloudflare D1"""
    try:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/d1/database/{D1_DATABASE_ID}/query"
        
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "sql": "SELECT entry_date, habits_data FROM habit_entries WHERE username = ? ORDER BY entry_date DESC",
            "params": [username]
        }
        
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        if result.get('success') and result.get('result'):
            results = []
            for row in result['result'][0].get('results', []):
                results.append((row["entry_date"], row["habits_data"]))
            return results
        else:
            print(f"D1 Get All Entries Error: {result.get('errors', 'Unknown error')}")
        
        return []
    except Exception as e:
        print(f"Error fetching all entries from D1: {e}")
        import traceback
        traceback.print_exc()
        return []
