"""
DNA Transport Simulation - Web Interface
=========================================

Flask-based web application for running DNA transport simulations
through a browser interface.

Features:
- Easy parameter configuration
- Multiple concurrent simulations
- Real-time progress tracking
- Results visualization and download
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, session, redirect, url_for
from functools import wraps
import os
import json
import uuid
import time
import threading
from datetime import datetime
from pathlib import Path
import subprocess
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dna-simulation-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Authentication configuration
ACCESS_PASSWORD = "sweppesportokal1!"

# Simulation job storage (in-memory for now, could use Redis/DB for production)
jobs = {}
jobs_lock = threading.Lock()

# Get paths
BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR.parent / 'results'
PYTHON_EXECUTABLE = sys.executable

def login_required(f):
    """Decorator to protect routes with authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def run_simulation_background(job_id, params):
    """Run simulation in background thread"""
    with jobs_lock:
        jobs[job_id]['status'] = 'running'
        jobs[job_id]['started_at'] = datetime.now().isoformat()
    
    try:
        # Build command
        cmd = [
            PYTHON_EXECUTABLE,
            str(BASE_DIR / 'main.py'),
            '--sequence', params['sequence'],
            '--mode', params['mode'],
            '--model', params['model'],
            '--symmetry', params['symmetry'],
            '--disorder', str(params['disorder']),
            '--workers', str(params['workers']),
            '--dos-bins', str(params['dos_bins'])
        ]
        
        # Add optional seed
        if params.get('seed'):
            cmd.extend(['--seed', str(params['seed'])])
        
        # Add flags
        if params.get('export'):
            cmd.append('--export')
        if params.get('disable_dos'):
            cmd.append('--disable-dos')
        if params.get('disable_analytical'):
            cmd.append('--disable-analytical')
        if params.get('disable_fft'):
            cmd.append('--disable-fft')
        if params.get('disable_dipole_fft'):
            cmd.append('--disable-dipole-fft')
        if params.get('disable_fourier'):
            cmd.append('--disable-fourier')
        
        # Run simulation
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR.parent)
        )
        
        with jobs_lock:
            if result.returncode == 0:
                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['output'] = result.stdout
                jobs[job_id]['completed_at'] = datetime.now().isoformat()
                
                # Store result file paths
                jobs[job_id]['files'] = {
                    'excel': str(RESULTS_DIR / 'results.xlsx') if params.get('export') else None,
                    'eigenvalue_plot': str(RESULTS_DIR / 'eigenvalue_spectrum.png'),
                    'dos_plot': str(RESULTS_DIR / 'density_of_states.png') if not params.get('disable_dos') else None
                }
            else:
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['error'] = result.stderr
                jobs[job_id]['completed_at'] = datetime.now().isoformat()
    
    except Exception as e:
        with jobs_lock:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = str(e)
            jobs[job_id]['completed_at'] = datetime.now().isoformat()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if session.get('authenticated'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ACCESS_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Incorrect password. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Main page with simulation form"""
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
@login_required
def simulate():
    """Start a new simulation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['sequence', 'mode', 'model']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create job
        job_id = str(uuid.uuid4())
        
        # Store job info
        with jobs_lock:
            jobs[job_id] = {
                'id': job_id,
                'status': 'queued',
                'params': data,
                'created_at': datetime.now().isoformat(),
                'started_at': None,
                'completed_at': None,
                'output': None,
                'error': None,
                'files': {}
            }
        
        # Start simulation in background
        thread = threading.Thread(
            target=run_simulation_background,
            args=(job_id, data)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'queued',
            'message': 'Simulation started'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<job_id>')
@login_required
def status(job_id):
    """Get simulation status"""
    with jobs_lock:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs[job_id].copy()
    
    return jsonify(job)

@app.route('/api/jobs')
@login_required
def list_jobs():
    """List all jobs"""
    with jobs_lock:
        job_list = [
            {
                'id': job['id'],
                'status': job['status'],
                'sequence': job['params'].get('sequence'),
                'created_at': job['created_at'],
                'completed_at': job['completed_at']
            }
            for job in jobs.values()
        ]
    
    # Sort by creation time (newest first)
    job_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify(job_list)

@app.route('/api/download/<job_id>/<filename>')
@login_required
def download(job_id, filename):
    """Download result file"""
    with jobs_lock:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs[job_id]
        
        if job['status'] != 'completed':
            return jsonify({'error': 'Job not completed'}), 400
        
        # Get file path
        file_path = None
        if filename == 'results.xlsx' and job['files'].get('excel'):
            file_path = job['files']['excel']
        elif filename == 'eigenvalue_spectrum.png' and job['files'].get('eigenvalue_plot'):
            file_path = job['files']['eigenvalue_plot']
        elif filename == 'density_of_states.png' and job['files'].get('dos_plot'):
            file_path = job['files']['dos_plot']
    
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/results/<job_id>')
@login_required
def results(job_id):
    """Results page"""
    return render_template('results.html', job_id=job_id)

if __name__ == '__main__':
    # Ensure results directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("🧬 DNA Transport Simulation - Web Interface")
    print("="*60)
    print(f"\n📂 Results directory: {RESULTS_DIR}")
    print(f"\n🌐 Starting server at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
