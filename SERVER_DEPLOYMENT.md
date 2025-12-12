# Server Deployment Guide - Structure File Support

## Quick Deployment Commands

### Step 1: SSH to Your Server
```bash
ssh your-username@your-server-address
```

### Step 2: Navigate to Repository
```bash
cd /path/to/DNA_experiment
# Check current branch
git branch
```

### Step 3: Pull the New Branch
```bash
# Fetch the new branch
git fetch origin

# Switch to the new feature branch
git checkout feature/structure-file-webapp

# Or if you prefer to merge into existing branch:
# git checkout cif_inclusion_test
# git merge feature/structure-file-webapp

# Pull latest changes
git pull origin feature/structure-file-webapp
```

### Step 4: Install New Dependencies
```bash
# Install Flask and CORS support
pip install flask flask-cors

# Or if using pip3
pip3 install flask flask-cors

# Verify installation
pip list | grep -i flask
```

### Step 5: Test the Backend
```bash
# Navigate to the project root
cd /path/to/DNA_experiment

# Test run the Flask backend
python app_server.py
```

You should see:
```
Starting DNA Transport Simulation Backend...
Server starting on http://localhost:5000
 * Running on http://127.0.0.1:5000
```

Press `Ctrl+C` to stop the test.

### Step 6: Set Up as a Service (Production)

#### Option A: Using systemd (Recommended for Linux)

Create service file:
```bash
sudo nano /etc/systemd/system/dna-simulation.service
```

Add this content:
```ini
[Unit]
Description=DNA Transport Simulation Flask Backend
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/DNA_experiment
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /path/to/DNA_experiment/app_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable dna-simulation

# Start the service
sudo systemctl start dna-simulation

# Check status
sudo systemctl status dna-simulation

# View logs
sudo journalctl -u dna-simulation -f
```

#### Option B: Using nohup (Simple Alternative)

```bash
# Start in background
cd /path/to/DNA_experiment
nohup python app_server.py > flask_app.log 2>&1 &

# Get the process ID
echo $!

# Check if running
ps aux | grep app_server

# Stop when needed
kill $(ps aux | grep 'app_server.py' | awk '{print $2}')
```

#### Option C: Using PM2 (Node.js Process Manager)

```bash
# Install PM2 if not already installed
npm install -g pm2

# Start the Flask app
pm2 start app_server.py --name dna-simulation --interpreter python3

# Save the process list
pm2 save

# Set PM2 to start on boot
pm2 startup

# Check status
pm2 status

# View logs
pm2 logs dna-simulation
```

### Step 7: Configure Nginx (If Using Reverse Proxy)

Edit your Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/dna-simulation
```

Add this location block:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Existing configuration...

    # Flask backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Web interface (static file)
    location / {
        root /path/to/DNA_experiment;
        try_files $uri $uri/ /web_interface.html;
    }
}
```

Test and reload Nginx:
```bash
# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 8: Update CORS Settings (If Needed)

If your frontend is served from a different domain, update `app_server.py`:

```python
# Find this line:
CORS(app)  # Enable CORS for local development

# Replace with:
CORS(app, origins=["https://your-domain.com"])
```

### Step 9: Verify Deployment

```bash
# Check if Flask is running
curl http://localhost:5000/api/health

# Should return:
# {"status":"healthy","python_dir":"...","python_dir_exists":true}

# Test sequence simulation
curl -X POST http://localhost:5000/api/simulate/sequence \
  -H "Content-Type: application/json" \
  -d '{"sequence":"AAAAA","mode":"HOMO","model":"FISHBONE","symmetry":"symmetric","disorder":"0","dos":"5"}'
```

### Step 10: Access the Web Interface

Open in browser:
```
http://your-server-address/web_interface.html
# or
http://your-domain.com/web_interface.html
```

---

## Complete Deployment Script

Save this as `deploy.sh` for quick deployment:

```bash
#!/bin/bash

echo "=== DNA Simulation Deployment ==="

# Navigate to project
cd /path/to/DNA_experiment || exit

# Pull latest changes
echo "Pulling latest code..."
git fetch origin
git checkout feature/structure-file-webapp
git pull origin feature/structure-file-webapp

# Install dependencies
echo "Installing dependencies..."
pip3 install flask flask-cors

# Restart service
echo "Restarting service..."
sudo systemctl restart dna-simulation

# Check status
echo "Service status:"
sudo systemctl status dna-simulation --no-pager

# Test API
echo "Testing API..."
sleep 2
curl http://localhost:5000/api/health

echo "=== Deployment Complete ==="
echo "Web interface: http://your-domain.com/web_interface.html"
echo "Logs: sudo journalctl -u dna-simulation -f"
```

Make it executable:
```bash
chmod +x deploy.sh
```

Run deployment:
```bash
./deploy.sh
```

---

## Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python3 --version

# Check if port 5000 is already in use
sudo lsof -i :5000

# Kill process on port 5000
sudo kill $(sudo lsof -t -i:5000)

# Check logs
sudo journalctl -u dna-simulation -n 50
```

### Permission Errors
```bash
# Fix file permissions
chmod +x app_server.py
chmod 644 web_interface.html

# Fix ownership
sudo chown -R your-username:your-username /path/to/DNA_experiment
```

### CORS Errors in Browser
Update `app_server.py`:
```python
from flask_cors import CORS

# Change from:
CORS(app)

# To:
CORS(app, origins=["*"])  # Allow all origins (development)
# or
CORS(app, origins=["https://your-domain.com"])  # Specific domain (production)
```

### Files Not Found
```bash
# Verify all files are present
cd /path/to/DNA_experiment
ls -la app_server.py web_interface.html python/structure_reader.py

# Verify Python can find modules
python3 -c "import sys; print(sys.path)"
```

---

## Rollback (If Needed)

```bash
# Switch back to previous branch
git checkout cif_inclusion_test

# Restart service
sudo systemctl restart dna-simulation
```

---

## Security Checklist

- [ ] Change Flask debug mode to False for production
- [ ] Set proper CORS origins (not "*")
- [ ] Use HTTPS with SSL certificate
- [ ] Set up firewall rules (only allow necessary ports)
- [ ] Run Flask behind Nginx/Apache reverse proxy
- [ ] Set file upload size limits
- [ ] Implement rate limiting
- [ ] Regular security updates

---

## Quick Reference

**Start Backend:**
```bash
sudo systemctl start dna-simulation
```

**Stop Backend:**
```bash
sudo systemctl stop dna-simulation
```

**Restart Backend:**
```bash
sudo systemctl restart dna-simulation
```

**View Logs:**
```bash
sudo journalctl -u dna-simulation -f
```

**Update Code:**
```bash
cd /path/to/DNA_experiment
git pull origin feature/structure-file-webapp
sudo systemctl restart dna-simulation
```
