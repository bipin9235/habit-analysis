"""
Check what's actually stored in your database
Run this to see the raw data
"""

import sqlite3
import json
from config import LOCAL_DB_PATH, D1_DATABASE_ID, CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
import requests

def check_local_db():
    """Check local SQLite database"""
    print("\n" + "="*60)
    print("📊 LOCAL DATABASE CHECK")
    print("="*60)
    
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM habit_entries")
        count = cursor.fetchone()[0]
        print(f"\nTotal entries in local DB: {count}")
        
        if count > 0:
            cursor.execute("SELECT username, entry_date, habits_data FROM habit_entries ORDER BY entry_date DESC LIMIT 5")
            entries = cursor.fetchall()
            
            print("\nLast 5 entries:")
            for username, date, data in entries:
                print(f"\n  User: {username}")
                print(f"  Date: {date}")
                print(f"  Raw JSON: {data}")
                try:
                    parsed = json.loads(data)
                    print(f"  Parsed data:")
                    for habit, value in parsed.items():
                        print(f"    - {habit}: {value} (type: {type(value).__name__})")
                except Exception as e:
                    print(f"  ❌ ERROR parsing JSON: {e}")
        
        conn.close()
        print("\n✅ Local DB check complete")
        
    except FileNotFoundError:
        print(f"\n❌ Database file not found: {LOCAL_DB_PATH}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def check_d1_db():
    """Check Cloudflare D1 database"""
    print("\n" + "="*60)
    print("☁️  CLOUDFLARE D1 CHECK")
    print("="*60)
    
    if not all([CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, D1_DATABASE_ID]):
        print("\n⚠️  D1 credentials not configured, skipping D1 check")
        return
    
    try:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/d1/database/{D1_DATABASE_ID}/query"
        
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Get count
        data = {"sql": "SELECT COUNT(*) as count FROM habit_entries"}
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        if result.get('success'):
            count = result['result'][0]['results'][0]['count']
            print(f"\nTotal entries in D1: {count}")
            
            if count > 0:
                # Get last 5 entries
                data = {"sql": "SELECT username, entry_date, habits_data FROM habit_entries ORDER BY entry_date DESC LIMIT 5"}
                response = requests.post(url, json=data, headers=headers)
                result = response.json()
                
                if result.get('success'):
                    entries = result['result'][0]['results']
                    
                    print("\nLast 5 entries:")
                    for entry in entries:
                        print(f"\n  User: {entry['username']}")
                        print(f"  Date: {entry['entry_date']}")
                        print(f"  Raw JSON: {entry['habits_data']}")
                        try:
                            parsed = json.loads(entry['habits_data'])
                            print(f"  Parsed data:")
                            for habit, value in parsed.items():
                                print(f"    - {habit}: {value} (type: {type(value).__name__})")
                        except Exception as e:
                            print(f"  ❌ ERROR parsing JSON: {e}")
        else:
            print(f"\n❌ D1 Error: {result.get('errors', 'Unknown error')}")
        
        print("\n✅ D1 check complete")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    check_local_db()
    check_d1_db()
    print("\n" + "="*60)
