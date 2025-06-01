# Deployment Guide - Bloom and Flow Website

## Quick Start

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and configure
3. Run: `python run.py`

### Docker Deployment
1. `docker-compose up --build`
2. Access at http://localhost:5000

## Production Deployment Options

### Option 1: Traditional Server (VPS/Cloud)
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SESSION_SECRET="your-secure-secret-key"
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
export FLASK_ENV="production"

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Option 2: Docker
```bash
docker build -t bloom-flow .
docker run -p 5000:5000 -e SESSION_SECRET="your-key" bloom-flow
```

### Option 3: Platform as a Service
- **Heroku**: Add Procfile with `web: gunicorn main:app`
- **Railway**: Automatically detects Python app
- **Render**: Use start command `gunicorn main:app`

## Environment Configuration

Required environment variables:
- `SESSION_SECRET`: Flask session key (generate a secure random string)
- `DATABASE_URL`: PostgreSQL connection string (optional, uses SQLite if not set)

Optional:
- `FLASK_ENV`: Set to "production" for production
- `PORT`: Server port (default: 5000)

## Database Setup

### PostgreSQL (Recommended for Production)
```sql
CREATE DATABASE bloom_flow;
CREATE USER bloom_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE bloom_flow TO bloom_user;
```

### SQLite (Development)
No setup required - database file created automatically.

## Security Considerations

1. **Session Secret**: Use a strong, random secret key
2. **Database**: Use strong passwords and limit access
3. **HTTPS**: Always use SSL in production
4. **Environment Variables**: Never commit secrets to version control

## Performance Optimization

1. **Static Files**: Use a CDN or nginx for static assets
2. **Database**: Set up connection pooling
3. **Caching**: Consider Redis for session storage
4. **Workers**: Scale Gunicorn workers based on CPU cores

## Monitoring

- Check application logs regularly
- Monitor database performance
- Set up health checks for the `/` endpoint
- Monitor disk space if using SQLite