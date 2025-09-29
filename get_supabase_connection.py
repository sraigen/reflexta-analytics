#!/usr/bin/env python3
"""
Get the correct Supabase connection string
"""

def get_supabase_connection_info():
    """Instructions to get the correct Supabase connection string"""
    
    print("🔧 How to Get the Correct Supabase Connection String")
    print("=" * 60)
    
    print("\n1. Go to your Supabase Dashboard:")
    print("   https://vbowznmcdzsgzntnzwfi.supabase.co")
    
    print("\n2. Click 'Settings' → 'Database'")
    
    print("\n3. Look for 'Connection string' section")
    
    print("\n4. You should see something like:")
    print("   postgresql://postgres:[YOUR-PASSWORD]@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres")
    
    print("\n5. Make sure to:")
    print("   ✅ Copy the FULL connection string")
    print("   ✅ Include the password")
    print("   ✅ Use the 'Direct connection' (not pooled)")
    
    print("\n6. Alternative: Check 'Connection pooling' section")
    print("   - Look for 'Direct connection' URL")
    print("   - This is usually what you need for Streamlit")
    
    print("\n7. If you see multiple URLs, try:")
    print("   - Direct connection (port 5432)")
    print("   - Not the pooled connection (port 6543)")
    
    print("\n8. Test the connection string locally first:")
    print("   python test_supabase_connection.py")
    
    print("\n" + "=" * 60)
    print("🎯 The issue is likely that Streamlit Cloud can't reach your database")
    print("   Make sure your Supabase database is publicly accessible")

if __name__ == "__main__":
    get_supabase_connection_info()
