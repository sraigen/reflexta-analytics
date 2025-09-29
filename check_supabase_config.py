#!/usr/bin/env python3
"""
Check Supabase database configuration
"""

def check_supabase_config():
    """Instructions to check Supabase configuration"""
    
    print("🔍 Supabase Database Configuration Checklist")
    print("=" * 60)
    
    print("\n1. Go to your Supabase Dashboard:")
    print("   https://vbowznmcdzsgzntnzwfi.supabase.co")
    
    print("\n2. Check Database Status:")
    print("   - Go to 'Settings' → 'Database'")
    print("   - Make sure database is 'Running' (not paused)")
    print("   - Check if there are any error messages")
    
    print("\n3. Check Public Access:")
    print("   - Go to 'Settings' → 'Database'")
    print("   - Look for 'Public access' or 'Database access'")
    print("   - Make sure it's enabled")
    
    print("\n4. Check Connection String:")
    print("   - Go to 'Settings' → 'Database'")
    print("   - Look for 'Connection string' section")
    print("   - Copy the 'Direct connection' URL (not pooled)")
    print("   - Should look like: postgresql://postgres:[PASSWORD]@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres")
    
    print("\n5. Check Firewall Settings:")
    print("   - Go to 'Settings' → 'Database'")
    print("   - Look for 'Firewall' or 'Network access'")
    print("   - Make sure there are no IP restrictions")
    print("   - Allow connections from anywhere (0.0.0.0/0)")
    
    print("\n6. Check SSL Configuration:")
    print("   - Make sure SSL is properly configured")
    print("   - Try different SSL modes: require, prefer, allow")
    
    print("\n7. Alternative: Try Connection Pooling:")
    print("   - Look for 'Connection pooling' section")
    print("   - Try the pooled connection URL (port 6543)")
    print("   - Format: postgresql://postgres:[PASSWORD]@db.vbowznmcdzsgzntnzwfi.supabase.co:6543/postgres")
    
    print("\n8. Check Database Logs:")
    print("   - Go to 'Logs' section")
    print("   - Look for any connection errors")
    print("   - Check if there are any blocked connections")
    
    print("\n" + "=" * 60)
    print("🎯 Common Issues:")
    print("   - Database is paused (most common)")
    print("   - Public access is disabled")
    print("   - Firewall blocking connections")
    print("   - Wrong connection string")
    print("   - SSL configuration issues")
    
    print("\n🚀 Next Steps:")
    print("   1. Check all the above settings")
    print("   2. Get the correct connection string")
    print("   3. Update Streamlit Cloud secrets")
    print("   4. Test the connection again")

if __name__ == "__main__":
    check_supabase_config()
