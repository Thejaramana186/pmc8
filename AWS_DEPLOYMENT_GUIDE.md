# AWS Deployment Guide for PI Management System

## 🚀 Quick Deployment Steps

### 1. **Build and Run with Docker**

```bash
# Build the Docker image
docker build -t pi-management .

# Run with SQLite (simple setup)
docker run -d \
  --name pi-management \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-super-secret-key-change-this \
  -v $(pwd)/data:/app/data \
  pi-management

# Or run with docker-compose
docker-compose up -d
```

### 2. **Environment Variables for Production**

Create a `.env` file or set these environment variables:

```bash
# Required
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key

# Database (choose one)
DATABASE_URL=sqlite:///data/pi_management.db
# OR for PostgreSQL:
# DATABASE_URL=postgresql://username:password@host:port/database

# Email Configuration (optional but recommended)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 3. **AWS EC2 Deployment**

```bash
# 1. Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# 3. Clone your project
git clone your-repo-url
cd pi-management

# 4. Set environment variables
cp .env.example .env
nano .env  # Edit with your settings

# 5. Build and run
docker-compose up -d

# 6. Check logs
docker-compose logs -f
```

### 4. **AWS ECS Deployment**

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

docker build -t pi-management .
docker tag pi-management:latest your-account.dkr.ecr.us-east-1.amazonaws.com/pi-management:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/pi-management:latest

# 2. Create ECS task definition with environment variables
# 3. Create ECS service
# 4. Configure load balancer
```

## 🔧 Configuration Options

### **Database Options**

1. **SQLite (Simple)**
   ```bash
   DATABASE_URL=sqlite:///data/pi_management.db
   ```

2. **PostgreSQL (Recommended for production)**
   ```bash
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

3. **AWS RDS**
   ```bash
   DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/pi_management
   ```

### **Email Providers**

1. **Gmail**
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

2. **Yahoo**
   ```bash
   MAIL_SERVER=smtp.mail.yahoo.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@yahoo.com
   MAIL_PASSWORD=your-app-password
   ```

3. **Outlook**
   ```bash
   MAIL_SERVER=smtp-mail.outlook.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@outlook.com
   MAIL_PASSWORD=your-password
   ```

## 🛠️ Troubleshooting

### **Database Issues**
```bash
# Check if database is initialized
docker exec -it pi-management python3 -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database initialized!')
"
```

### **Permission Issues**
```bash
# Fix file permissions
sudo chown -R 1000:1000 ./data
chmod 755 ./data
```

### **Check Logs**
```bash
# Docker logs
docker logs pi-management

# Application logs
docker exec -it pi-management tail -f /var/log/app.log
```

## 🔒 Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS with SSL certificate
- [ ] Configure firewall rules
- [ ] Use strong database passwords
- [ ] Enable email app passwords
- [ ] Regular security updates

## 📊 Monitoring

### **Health Check**
```bash
curl http://your-server:5000/login
```

### **Database Check**
```bash
docker exec -it pi-management python3 -c "
from app import create_app, db
from app.models.user import User
app = create_app()
with app.app_context():
    count = User.query.count()
    print(f'Users in database: {count}')
"
```

## 🚀 Production Optimizations

1. **Use Gunicorn** (included in startup script)
2. **Enable database connection pooling**
3. **Set up reverse proxy with Nginx**
4. **Configure log rotation**
5. **Set up automated backups**
6. **Monitor resource usage**

## 📞 Support

If you encounter issues:
1. Check the logs first
2. Verify environment variables
3. Test database connectivity
4. Check email configuration
5. Review AWS security groups and networking

The application is now production-ready for AWS deployment!