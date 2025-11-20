# DNA Transport Simulation - Docker Deployment Guide

## Quick Start

### Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at **http://localhost:5000**

## Manual Docker Build

```bash
# Build image
docker build -t dna-simulation:latest .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/logs:/app/logs \
  --name dna-simulation \
  dna-simulation:latest

# View logs
docker logs -f dna-simulation

# Stop container
docker stop dna-simulation
docker rm dna-simulation
```

## Production Deployment

### 1. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit with your settings
nano .env
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Deploy with Nginx Proxy

```bash
# Start with nginx reverse proxy
docker-compose --profile production up -d
```

### 3. SSL/HTTPS Setup

**Option A: Using Let's Encrypt (Recommended)**

```bash
# Install certbot
apt-get install certbot

# Generate certificates
certbot certonly --standalone -d your-domain.com

# Copy certificates
mkdir ssl
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem

# Update nginx.conf to enable HTTPS section
# Restart nginx
docker-compose restart nginx
```

**Option B: Self-Signed Certificate (Development)**

```bash
mkdir ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem
```

### 4. Resource Configuration

Edit `docker-compose.yml` to adjust resource limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '8'      # Adjust based on server
      memory: 16G    # Adjust based on server
```

### 5. Persistent Data

Results and logs are stored in volumes:
- `./results` - Simulation output files
- `./logs` - Application and access logs

## Monitoring

### View Application Logs

```bash
# All logs
docker-compose logs -f

# Application only
docker-compose logs -f dna-simulation

# Last 100 lines
docker-compose logs --tail=100 dna-simulation
```

### Check Health

```bash
# Container health status
docker ps

# Application endpoint
curl http://localhost:5000/

# Container stats
docker stats dna-simulation
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild image
docker-compose build

# Restart with new image
docker-compose up -d
```

### Backup Data

```bash
# Backup results
tar -czf results-backup-$(date +%Y%m%d).tar.gz results/

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

### Clean Up

```bash
# Remove stopped containers
docker-compose down

# Remove images
docker rmi dna-simulation:latest

# Clean up volumes (WARNING: deletes data)
docker-compose down -v
```

## Scaling

### Multiple Workers

The application uses Gunicorn with 4 workers by default. To adjust:

Edit `Dockerfile` CMD line:
```dockerfile
CMD ["gunicorn", "--workers", "8", ...]  # Increase workers
```

### Multiple Instances

Use docker-compose scale (requires load balancer):

```bash
docker-compose up -d --scale dna-simulation=3
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs dna-simulation

# Check if port is in use
netstat -tulpn | grep 5000

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Simulation Errors

```bash
# Enter container
docker exec -it dna-simulation bash

# Run test simulation
python main.py --sequence ATGCAT --mode HOMO --model FISHBONE

# Check dependencies
pip list
```

### Out of Memory

```bash
# Increase memory limit in docker-compose.yml
# Or check current usage
docker stats dna-simulation
```

### Performance Issues

1. Increase CPU/memory limits
2. Increase Gunicorn workers
3. Enable nginx caching
4. Monitor with `docker stats`

## Security Recommendations

1. **Change default secret key** in `.env`
2. **Enable HTTPS** in production
3. **Use firewall** to restrict access
4. **Keep images updated**: `docker-compose pull`
5. **Scan for vulnerabilities**: `docker scan dna-simulation:latest`
6. **Use specific image versions** instead of `latest`
7. **Run as non-root user** (TODO: add to Dockerfile)

## Cloud Deployment

### AWS EC2

```bash
# Install Docker
sudo yum install docker -y
sudo service docker start

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <your-repo>
cd DNA_experiment

# Deploy
docker-compose up -d
```

### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/dna-simulation

# Deploy
gcloud run deploy dna-simulation \
  --image gcr.io/PROJECT-ID/dna-simulation \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Create container
az container create \
  --resource-group myResourceGroup \
  --name dna-simulation \
  --image dna-simulation:latest \
  --dns-name-label dna-sim \
  --ports 5000
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Session encryption key | Random |
| `FLASK_ENV` | Environment mode | production |
| `RESULTS_DIR` | Results directory path | /app/results |
| `MAX_CONCURRENT_JOBS` | Job queue limit | Unlimited |

## Next Steps

1. Set up monitoring (Prometheus/Grafana)
2. Configure automatic backups
3. Implement user authentication
4. Add job persistence (Redis/PostgreSQL)
5. Set up CI/CD pipeline
