#!/usr/bin/env python3
"""
Get the correct connection string from Supabase dashboard
"""

def get_correct_connection_instructions():
    """Instructions to get the correct connection string"""
    
    print("🔧 How to Get the Correct Transaction Pooler Connection String")
    print("=" * 70)
    
    print("\n1. Go to your Supabase Dashboard:")
    print("   https://vbowznmcdzsgzntnzwfi.supabase.co")
    
    print("\n2. Click 'Settings' → 'Database'")
    
    print("\n3. Look for 'Connection string' section")
    
    print("\n4. Find the 'Transaction pooler' section")
    print("   - It should show 'IPv4 compatible' with a green checkmark")
    print("   - Look for the connection string that starts with:")
    print("     postgresql://postgres.vbowznmcdzsgzntnzwfi:[PASSWORD]@...")
    
    print("\n5. Copy the FULL connection string from the Transaction pooler section")
    print("   - It should include your password")
    print("   - It should have a different hostname (not db.vbowznmcdzsgzntnzwfi.supabase.co)")
    print("   - It should use port 6543 (not 5432)")
    
    print("\n6. The format should look like:")
    print("   postgresql://postgres.vbowznmcdzsgzntnzwfi:[YOUR-PASSWORD]@[POOLER-HOST]:6543/postgres")
    
    print("\n7. Update your Streamlit Cloud secrets with this EXACT string")
    
    print("\n" + "=" * 70)
    print("🎯 Key Differences from Direct Connection:")
    print("   - Hostname: postgres.vbowznmcdzsgzntnzwfi (not db.vbowznmcdzsgzntnzwfi)")
    print("   - Port: 6543 (not 5432)")
    print("   - Domain: pooler.supabase.com (not supabase.co)")
    print("   - IPv4 compatible (not IPv6 only)")
    
    print("\n🚀 This should fix the 'Cannot assign requested address' error!")

if __name__ == "__main__":
    get_correct_connection_instructions()
