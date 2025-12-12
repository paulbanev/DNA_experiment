#!/bin/bash
# DNA Transport Simulation - Fresh Server Setup
# Run this script on a new Ubuntu/Debian server

echo "==================================="
echo "DNA Simulation - Fresh Server Setup"
echo "==================================="

# 1. UPDATE SYSTEM
echo ""
echo "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. INSTALL PYTHON AND PIP
echo ""
echo "Step 2: Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv git

# Verify installations
python3 --version
pip3 --version
git --version

# 3. CLONE REPOSITORY
echo ""
echo "Step 3: Cloning repository..."
cd /var/www  # Or wherever you want the app
# If /var/www doesn't exist:
sudo mkdir -p /var/www
sudo chown -R $USER:$USER /var/www

git clone https://github.com/paulbanev/DNA_experiment.git
cd DNA_experiment

# 4. CHECKOUT THE FEATURE BRANCH
echo ""
echo "Step 4: Switching to feature branch..."
git checkout feature/structure-file-webapp
git pull origin feature/structure-file-webapp

# 5. INSTALL PYTHON DEPENDENCIES
echo ""
echo "Step 5: Installing Python dependencies..."
pip3 install numpy biopython matplotlib pandas flask flask-cors

# Verify installations
pip3 list | grep -E "numpy|biopython|matplotlib|pandas|flask"

# 6. TEST THE PYTHON SIMULATION (Optional)
echo ""
echo "Step 6: Testing Python simulation..."
cd python
python3 main.py --sequence AAAAA --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0 --number_of_DOS_points 5
cd ..

# 7. CREATE SYSTEMD SERVICE
echo ""
echo "Step 7: Creating systemd service..."
sudo tee /etc/systemd/system/dna-simulation.service > /dev/null <<EOF
[Unit]
Description=DNA Transport Simulation Flask Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/DNA_experiment
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /var/www/DNA_experiment/app_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. START THE SERVICE
echo ""
echo "Step 8: Starting the backend service..."
sudo systemctl daemon-reload
sudo systemctl enable dna-simulation
sudo systemctl start dna-simulation

# Wait a moment for service to start
sleep 2

# Check status
sudo systemctl status dna-simulation --no-pager

# 9. TEST THE API
echo ""
echo "Step 9: Testing API endpoint..."
curl http://localhost:5000/api/health

# 10. INSTALL AND CONFIGURE NGINX (Optional but recommended)
echo ""
echo "Step 10: Installing Nginx..."
sudo apt install -y nginx

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/dna-simulation > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Serve static web interface
    location / {
        root /var/www/DNA_experiment;
        try_files \$uri \$uri/ /web_interface.html;
        index web_interface.html;
    }

    # Proxy API requests to Flask
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    # Serve example files
    location /python/example_ {
        alias /var/www/DNA_experiment/python/;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/dna-simulation /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx

# 11. CONFIGURE FIREWALL
echo ""
echo "Step 11: Configuring firewall..."
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS (for future SSL)
echo "y" | sudo ufw enable

# 12. FINAL STATUS CHECK
echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Services Status:"
sudo systemctl status dna-simulation --no-pager | head -5
sudo systemctl status nginx --no-pager | head -5
echo ""
echo "Access your app at:"
echo "  http://$(curl -s ifconfig.me)/web_interface.html"
echo "  or"
echo "  http://your-server-ip/web_interface.html"
echo ""
echo "API Health Check:"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""
echo "Useful Commands:"
echo "  sudo systemctl status dna-simulation  # Check backend status"
echo "  sudo systemctl restart dna-simulation # Restart backend"
echo "  sudo journalctl -u dna-simulation -f  # View backend logs"
echo "  sudo systemctl status nginx           # Check Nginx status"
echo ""
echo "Next Steps:"
echo "  1. Optional: Set up SSL with Let's Encrypt (certbot)"
echo "  2. Optional: Configure domain name"
echo "  3. Test the web interface in your browser"
echo "==================================="
