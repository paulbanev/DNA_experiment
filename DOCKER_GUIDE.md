# DNA Transport Simulation - Docker Deployment Guide

## 🐳 Quick Start with Docker

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

### One-Command Deployment

```bash
# Clone the repository
git clone https://github.com/paulbanev/DNA_experiment.git
cd DNA_experiment
git checkout feature/structure-file-webapp

# Start everything
docker-compose up -d

# Access the app
# Open browser: http://localhost
```

**That's it!** 🎉

---

## 📋 Detailed Instructions

### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/paulbanev/DNA_experiment.git
cd DNA_experiment
git checkout feature/structure-file-webapp

# Copy environment file (optional)
cp .env.example .env
# Edit .env if needed
```

### 2. Build and Start

```bash
# Build images
docker-compose build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Verify Deployment

```bash
# Check running containers
docker-compose ps

# Should show:
# dna-simulation-backend   running   0.0.0.0:5000->5000/tcp
# dna-simulation-nginx     running   0.0.0.0:80->80/tcp

# Test backend health
curl http://localhost:5000/api/health

# Test web interface
curl http://localhost/
```

### 4. Access the Application

Open in browser:
```
http://localhost
# or
http://your-server-ip
```

---

## 🎛️ Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f nginx
```

### Rebuilding

```bash
# Rebuild after code changes
docker-compose build

# Rebuild and restart
docker-compose up -d --build

# Force rebuild (no cache)
docker-compose build --no-cache
```

### Maintenance

```bash
# Check container status
docker-compose ps

# Execute command in backend container
docker-compose exec backend python --version

# Run simulation directly
docker-compose exec backend python python/main.py --sequence AAAAA --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0 --number_of_DOS_points 5

# Access backend shell
docker-compose exec backend /bin/bash
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a
```

---

## 📁 Docker Architecture

```
┌─────────────────────────────────────┐
│         Docker Compose              │
└─────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  Nginx          │  │  Flask Backend  │
│  (Port 80/443)  │  │  (Port 5000)    │
│                 │  │                 │
│  - Reverse Proxy│  │  - API Server   │
│  - Static Files │  │  - Simulations  │
│  - Rate Limiting│  │  - File Upload  │
└─────────────────┘  └─────────────────┘
         │                    │
         └────────┬───────────┘
                  │
         ┌────────▼────────┐
         │  Docker Network │
         │  (dna-network)  │
         └─────────────────┘
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file:
```bash
FLASK_ENV=production
PYTHONUNBUFFERED=1
MAX_UPLOAD_SIZE=10485760
```

### Port Configuration

Edit `docker-compose.yml` to change ports:
```yaml
services:
  nginx:
    ports:
      - "8080:80"  # Change from 80 to 8080
```

### Volume Mounts

Volumes are automatically created for:
- `./python` - Application code (live reload in development)
- `./python/results` - Simulation results (persisted)

---

## 🚀 Production Deployment

### On a Cloud Server (AWS, DigitalOcean, etc.)

```bash
# 1. SSH to server
ssh user@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and log back in

# 3. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone and start
git clone https://github.com/paulbanev/DNA_experiment.git
cd DNA_experiment
git checkout feature/structure-file-webapp
docker-compose up -d

# 5. Configure firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### SSL/HTTPS Setup (Optional)

1. Get SSL certificates (Let's Encrypt):
```bash
# Install certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem
```

2. Uncomment HTTPS section in `nginx.conf`

3. Update `docker-compose.yml`:
```yaml
nginx:
  volumes:
    - ./ssl:/etc/nginx/ssl:ro
```

4. Restart:
```bash
docker-compose down
docker-compose up -d
```

---

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check if ports are in use
sudo lsof -i :5000
sudo lsof -i :80

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Permission Errors

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker-compose up -d
```

### Backend Crashes

```bash
# Check backend logs
docker-compose logs -f backend

# Restart backend only
docker-compose restart backend

# Access backend shell to debug
docker-compose exec backend /bin/bash
python app_server.py  # Run manually
```

### Network Issues

```bash
# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

---

## 📊 Monitoring

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

### Logs

```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Since timestamp
docker-compose logs --since 2h
```

---

## 🔒 Security Best Practices

- [ ] Use `.env` file for sensitive configuration
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Set up firewall rules
- [ ] Regularly update Docker images
- [ ] Use docker secrets for production credentials
- [ ] Implement authentication for public deployments
- [ ] Regular backups of results volume

---

## 🆙 Updating

```bash
# Pull latest code
git pull origin feature/structure-file-webapp

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Verify
docker-compose ps
curl http://localhost/api/health
```

---

## 📦 Export/Import

### Export Images

```bash
# Save images
docker save dna_experiment_backend:latest | gzip > dna-backend.tar.gz
docker save nginx:alpine | gzip > dna-nginx.tar.gz
```

### Import Images

```bash
# Load images
docker load < dna-backend.tar.gz
docker load < dna-nginx.tar.gz

# Start
docker-compose up -d
```

---

## 🎯 Performance Tuning

### For Development (Live Reload)

Edit `docker-compose.yml`:
```yaml
backend:
  volumes:
    - .:/app  # Mount entire directory
  environment:
    - FLASK_ENV=development
    - FLASK_DEBUG=1
```

### For Production (Optimized)

Edit `docker-compose.yml`:
```yaml
backend:
  restart: always
  environment:
    - FLASK_ENV=production
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
```

---

## 📞 Support

### Quick Health Check

```bash
# One-liner health check
docker-compose ps && \
curl -s http://localhost:5000/api/health | python3 -m json.tool && \
echo "Web interface: http://localhost/"
```

### Get Full Status

```bash
#!/bin/bash
echo "=== Docker Compose Status ==="
docker-compose ps

echo -e "\n=== Backend Health ==="
curl -s http://localhost:5000/api/health | python3 -m json.tool

echo -e "\n=== Nginx Status ==="
docker-compose exec nginx nginx -t 2>&1 | grep -E "(successful|test)"

echo -e "\n=== Resources ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 🎉 Success!

If everything is working, you should see:
- ✅ Both containers running (`docker-compose ps`)
- ✅ Backend health check passing (`/api/health`)
- ✅ Web interface accessible (`http://localhost`)
- ✅ File upload working
- ✅ Simulations executing

**Enjoy your Dockerized DNA Transport Simulation!** 🧬
