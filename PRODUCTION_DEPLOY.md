# Production Deployment Guide

## Prerequisites

1. **Docker and Docker Compose** installed on your server
2. **Domain name** (optional, but recommended for HTTPS)
3. **SSL certificates** (optional, for HTTPS)

## Quick Start

### 1. Build and Push Docker Image

```bash
# Build the image
docker build -t pavlosbanev/dna_experiment:latest .

# Push to Docker Hub (requires docker login)
docker login
docker push pavlosbanev/dna_experiment:latest
```

### 2. Set Up Environment Variables

```bash
# Copy the production environment template
cp .env.production .env

# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Edit .env and replace FLASK_SECRET_KEY with the generated value
nano .env
```

### 3. Deploy with Docker Compose

```bash
# Start the services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### 4. Access the Application

- **HTTP**: http://your-server-ip
- **HTTPS** (if configured): https://your-domain.com

## SSL/HTTPS Configuration (Optional)

### Using Let's Encrypt with Certbot

1. **Install Certbot** on your server:
   ```bash
   sudo apt-get update
   sudo apt-get install certbot
   ```

2. **Obtain SSL certificates**:
   ```bash
   sudo certbot certonly --standalone -d your-domain.com
   ```

3. **Create SSL directory and copy certificates**:
   ```bash
   mkdir -p ssl
   sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
   sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
   sudo chmod 644 ssl/*.pem
   ```

4. **Update nginx.conf**:
   - Uncomment the HTTPS server block (lines 65-75)
   - Update `server_name` to your domain
   - Uncomment the SSL volume mount in `docker-compose.prod.yml`

5. **Restart services**:
   ```bash
   docker-compose -f docker-compose.prod.yml restart nginx
   ```

## Scaling and Resource Management

### Adjust Resource Limits

Edit `docker-compose.prod.yml` to change CPU and memory limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '8'      # Maximum CPUs
      memory: 8G     # Maximum memory
    reservations:
      cpus: '4'      # Minimum CPUs
      memory: 4G     # Minimum memory
```

### Scale Gunicorn Workers

In `Dockerfile`, adjust the Gunicorn workers based on your CPU cores:

```dockerfile
# Formula: (2 x $num_cores) + 1
CMD ["gunicorn", "--workers", "8", ...]
```

## Monitoring and Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f dna-simulation
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Check Health Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Backup Results

```bash
# Create backup of results volume
docker run --rm -v dna_experiment_dna_results:/data -v $(pwd):/backup \
  alpine tar czf /backup/results-backup-$(date +%Y%m%d).tar.gz /data
```

### Update Deployment

```bash
# Pull latest image
docker pull pavlosbanev/dna_experiment:latest

# Recreate containers
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Clean up old images
docker image prune -f
```

## Troubleshooting

### Check if services are running

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Restart services

```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart dna-simulation
```

### Access container shell

```bash
docker exec -it dna-simulation-web /bin/bash
```

### Check nginx configuration

```bash
docker exec dna-simulation-nginx nginx -t
```

## Security Recommendations

1. **Always use HTTPS in production** with valid SSL certificates
2. **Set a strong FLASK_SECRET_KEY** in `.env`
3. **Keep Docker images updated** regularly
4. **Use firewall rules** to restrict access (UFW, iptables, etc.)
5. **Enable rate limiting** in nginx (already configured)
6. **Regular backups** of results and logs
7. **Monitor logs** for suspicious activity

## Production Checklist

- [ ] Built and pushed Docker image to registry
- [ ] Created `.env` file with secure secret key
- [ ] Configured domain name (if using)
- [ ] Obtained SSL certificates (if using HTTPS)
- [ ] Updated `nginx.conf` with domain and SSL settings
- [ ] Adjusted resource limits based on server capacity
- [ ] Started services with `docker-compose.prod.yml`
- [ ] Verified health checks are passing
- [ ] Tested application is accessible
- [ ] Set up backup strategy for results
- [ ] Configured monitoring/alerting (optional)
