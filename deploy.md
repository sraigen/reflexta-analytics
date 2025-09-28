# Reflexta Data Intelligence - Deployment Guide

## 🚀 Streamlit Community Cloud (Free)

### Prerequisites:
- GitHub repository with your code
- Streamlit account

### Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Reflexta Data Intelligence Analytics Platform"
   git remote add origin https://github.com/yourusername/reflexta-analytics.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `yourusername/reflexta-analytics`
   - Main file: `app.py`
   - Click "Deploy!"

### Environment Variables:
Add these in Streamlit Cloud settings:
```
DATABASE_URL=postgresql://username:password@host:port/database
```

## 🐳 Docker Deployment

### Build and Run:
```bash
# Build the image
docker build -t reflexta-analytics .

# Run the container
docker run -p 8501:8501 -e DATABASE_URL=your_db_url reflexta-analytics
```

### Docker Compose:
```bash
docker-compose up -d
```

## ☁️ Cloud Platforms

### 1. **Heroku:**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create reflexta-analytics
git push heroku main
```

### 2. **Railway:**
- Connect GitHub repository
- Set environment variables
- Deploy automatically

### 3. **Render:**
- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `streamlit run app.py`

## 🔧 Environment Setup

### Required Environment Variables:
```bash
DATABASE_URL=postgresql://username:password@host:port/database
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Database Setup:
1. **PostgreSQL on Cloud:**
   - AWS RDS
   - Google Cloud SQL
   - Azure Database
   - Supabase (Free tier available)

2. **Run Database Setup:**
   ```bash
   python populate_sample_data.py
   ```

## 📊 Production Considerations

### Performance:
- Use connection pooling
- Implement caching
- Optimize database queries
- Use CDN for static assets

### Security:
- Use environment variables for secrets
- Implement authentication
- Use HTTPS
- Regular security updates

### Monitoring:
- Streamlit Cloud provides basic monitoring
- Add custom logging
- Set up alerts
- Monitor database performance

## 🎯 Recommended Deployment Path

### For Demo/Testing:
1. **Streamlit Community Cloud** (Free)
2. **Supabase** for database (Free tier)
3. **GitHub** for version control

### For Production:
1. **Railway/Render** for hosting
2. **AWS RDS/Google Cloud SQL** for database
3. **Custom domain** for branding
4. **SSL certificate** for security

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Database hosted and accessible
- [ ] Environment variables configured
- [ ] Dependencies in requirements.txt
- [ ] Database schema created
- [ ] Sample data populated
- [ ] App tested locally
- [ ] Deployment successful
- [ ] Domain configured (optional)
- [ ] SSL certificate (optional)
