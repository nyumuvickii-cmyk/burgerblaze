# Deployment Guide - BurgerBlaze

This guide will help you deploy BurgerBlaze to Render.com. The site is fully configured and ready for deployment.

## Pre-Deployment Checklist

- [ ] Secret key configured (render.yaml or environment variable)
- [ ] DEBUG set to False in production
- [ ] Database URL configured
- [ ] Static files configured correctly
- [ ] Email settings configured (optional)

## Deployment Steps

### 1. Push to GitHub

```bash
cd /workspaces/burgerblaze

# Initialize git if not already done
git init
git add .
git commit -m "BurgerBlaze - Initial release"

# Add to your GitHub repository
git remote add origin https://github.com/YOUR-USERNAME/burgerblaze.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render.com

1. **Visit Render.com**
   - Go to https://render.com
   - Sign in with GitHub account

2. **Create New Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account
   - Select "burgerblaze" repository

3. **Configure Service**
   - The `render.yaml` file will be automatically detected
   - Review the configuration:
     - Name: `burgerblaze`
     - Environment: Python
     - Build command: `pip install -r requirements.txt`
     - Start command: `gunicorn burgerblaze.wsgi:application`

4. **Environment Variables**
   - Render will automatically set up PostgreSQL
   - Add these environment variables:
     ```
     DEBUG=False
     SECRET_KEY=<generate-a-random-key>
     ALLOWED_HOSTS=your-app-name.onrender.com,www.yourdomain.com
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will:
     - Install dependencies
     - Run migrations
     - Collect static files
     - Start the server

6. **Post-Deployment**
   - Wait for deployment to complete (3-5 minutes)
   - Visit your app at `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin`

### 3. Initial Setup on Render.com

After deployment, create the admin user:

1. In Render dashboard, open shell for your service
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Create an admin account with your credentials

## Alternative: Deploy on Heroku

### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Deploy

```bash
# Login
heroku login

# Create app
heroku create burgerblaze-YOUR-NAME
heroku git:remote -a burgerblaze-YOUR-NAME

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-generated-secret-key

# Deploy
git push heroku main

# Setup database
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py populate_menu

# View logs
heroku logs --tail
```

## Alternative: Deploy on DigitalOcean App Platform

### 1. Create App

1. Go to DigitalOcean App Platform
2. Click "Create" → "App"
3. Select "GitHub repository"
4. Choose "burgerblaze" repository

### 2. Configure Components

1. **Web Service**
   - Environment: Python
   - HTTP Routes: `/`
   - Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Run command: `gunicorn burgerblaze.wsgi:application`

2. **PostgreSQL Database**
   - Add a managed PostgreSQL database
   - DigitalOcean will set the `DATABASE_URL`

3. **Environment Variables**
   - DEBUG: False
   - SECRET_KEY: (generate random key)

4. Deploy and wait for completion

## Alternative: Deploy on PythonAnywhere

1. Go to https://www.pythonanywhere.com/
2. Sign up for free account
3. Upload project files
4. Configure web app settings
5. Set Python 3.11
6. Configure WSGI file
7. Reload web app

## Production Checklist

### Security

- [ ] Set `DEBUG = False`
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` correctly
- [ ] Use HTTPS (all deployment services provide this)
- [ ] Set `SECURE_SSL_REDIRECT = True`
- [ ] Use strong database passwords
- [ ] Consider firewall rules

### Performance

- [ ] Enable WhiteNoise for static files ✓ (already configured)
- [ ] Use PostgreSQL instead of SQLite ✓ (configured)
- [ ] Enable caching headers on static files
- [ ] Consider CDN for images
- [ ] Setup monitoring and logging

### Maintenance

- [ ] Setup automated backups
- [ ] Monitor error logs
- [ ] Track performance metrics
- [ ] Regular security updates
- [ ] Database optimization

### Backup and Recovery

```bash
# Create database backup
# For Render/DigitalOcean: use platform backup features

# For local testing:
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
```

## Environment Variables Reference

```
# Django Settings
DEBUG=False
SECRET_KEY=your-random-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-service.onrender.com

# Database (auto-set by platform)
DATABASE_URL=postgres://user:pass@host:port/dbname

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (optional)
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

## Monitoring and Logging

### Render.com
- Logs are available in the Render dashboard
- Real-time log streaming available

### Heroku
```bash
# View logs
heroku logs --tail

# View specific app logs
heroku logs --tail -a your-app-name

# Search logs
heroku logs | grep ERROR
```

### DigitalOcean
- Logs available in App Platform dashboard
- Integration with CloudWatch optional

## Troubleshooting Deployment

### Static Files Not Loading

```bash
# Collect again
python manage.py collectstatic --noinput --clear

# Check settings
DEBUG=False
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Database Connection Error

```bash
# Check DATABASE_URL is set
heroku config | grep DATABASE_URL

# Test connection
python manage.py dbshell
```

### 500 Server Error

1. Check logs for specific error
2. Verify all environment variables are set
3. Ensure database migrations ran
4. Check SECRET_KEY is set and valid

### Permission Denied on Migration

```bash
# Run migrations explicitly
python manage.py migrate --run-syncdb
```

## Custom Domain

### Render.com
1. Go to service settings
2. Add custom domain
3. Update DNS records
4. Enable HTTPS (automatic)

### Heroku
```bash
heroku domains:add www.yourdomain.com
```

Then add these DNS records:
- A record: points to Heroku IP
- CNAME record: points to your Heroku app

## Auto-Scaling and Performance

### Render.com
- Auto-scaling available on paid tiers
- Can manually increase resources

### Heroku
```bash
# Scale to multiple dynos
heroku ps:scale web=2
```

## Cost Optimization

- Start with free tier for testing
- Scale up as traffic increases
- Monitor resource usage
- Use spot instances for non-critical workloads

## Getting Help

- **Django Documentation**: https://docs.djangoproject.com
- **Render.com Docs**: https://render.com/docs
- **Heroku Docs**: https://devcenter.heroku.com
- **Project Issues**: Check GitHub issues

---

**Ready to launch BurgerBlaze?** Start with Step 1: Push to GitHub! 🚀
