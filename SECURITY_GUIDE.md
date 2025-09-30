# 🔒 Security Configuration Guide

## ⚠️ CRITICAL: Remove Hardcoded Credentials

This guide helps you secure your application by removing exposed credentials and implementing proper security practices.

## 🚨 Immediate Actions Required

### 1. **Remove Exposed Credentials from Git History**

The following credentials were found in your codebase:
- API Key: `sk-0f8f14e071d34831aabf892ea372de2f`
- Database Password: `Sit@1125`
- Database URLs with credentials

**⚠️ These credentials are now compromised and should be regenerated immediately!**

### 2. **Regenerate All Credentials**
- [ ] Generate new DeepSeek API key
- [ ] Change database passwords
- [ ] Update all connection strings

## 🔧 Secure Configuration Setup

### Step 1: Environment Variables

Create a `.env` file (copy from `env.example`):
```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/database_name
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password

# AI Assistant API Key
DEEPSEEK_API_KEY=your_new_deepseek_api_key_here
```

### Step 2: Streamlit Secrets

Create `.streamlit/secrets.toml` (copy from `.streamlit/secrets.toml.example`):
```toml
[connections.sql]
url = "postgresql+psycopg://username:password@localhost:5432/database_name"

deepseek_api_key = "your_new_deepseek_api_key_here"
```

### Step 3: Git Security

The following files are now protected by `.gitignore`:
- `.env` files
- `.streamlit/secrets.toml`
- Any files containing `*api_key*`, `*secret*`, `*token*`, `*password*`

## 🚀 Deployment Security

### For Streamlit Cloud:
1. Go to your app settings
2. Add secrets in the "Secrets" section:
   ```
   [connections.sql]
   url = "your_database_url"
   
   deepseek_api_key = "your_api_key"
   ```

### For Local Development:
1. Copy `env.example` to `.env`
2. Fill in your actual credentials
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
4. Fill in your actual credentials

## 🔍 Security Checklist

- [ ] All hardcoded credentials removed from code
- [ ] Environment variables configured
- [ ] `.env` file created and filled
- [ ] `.streamlit/secrets.toml` configured
- [ ] Old credentials regenerated
- [ ] Git history cleaned (if needed)
- [ ] Team members informed about new credentials

## 🛡️ Best Practices

1. **Never commit credentials** to git
2. **Use environment variables** for all sensitive data
3. **Rotate credentials regularly**
4. **Use different credentials** for dev/staging/production
5. **Monitor access logs** for suspicious activity
6. **Use strong, unique passwords**

## 🆘 Emergency Response

If credentials are compromised:
1. **Immediately regenerate** all exposed credentials
2. **Review access logs** for unauthorized usage
3. **Notify team members** of credential changes
4. **Update all environments** with new credentials
5. **Consider using a password manager** for team credential sharing

## 📞 Support

If you need help with credential management or security setup, refer to:
- Streamlit Cloud documentation
- Your database provider's security guide
- API provider's authentication documentation
