"""
Simple Flask backend for DNA Transport Simulation
Handles both sequence input and structure file uploads
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import tempfile
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Directory where main.py is located
PYTHON_DIR = Path(__file__).parent / 'python'

@app.route('/api/simulate/sequence', methods=['POST'])
def simulate_sequence():
    """Handle DNA sequence simulation"""
    try:
        data = request.json
        sequence = data.get('sequence')
        mode = data.get('mode', 'HOMO')
        model = data.get('model', 'FISHBONE')
        symmetry = data.get('symmetry', 'symmetric')
        disorder = data.get('disorder', '0')
        dos_points = data.get('dos', '5')
        
        # Validate sequence
        if not sequence:
            return jsonify({'error': 'Sequence is required'}), 400
        
        # Build command
        cmd = [
            'python', 'main.py',
            '--sequence', sequence,
            '--mode', mode,
            '--model', model,
            '--symmetry', symmetry,
            '--disorder', disorder,
            '--number_of_DOS_points', dos_points
        ]
        
        # Add optional parameters
        if data.get('seed'):
            cmd.extend(['--seed', str(data.get('seed'))])
        
        if data.get('export'):
            cmd.append('--export')
        
        if data.get('workers'):
            cmd.extend(['--workers', str(data.get('workers'))])
        
        # Analysis control flags
        if data.get('disable_dos'):
            cmd.append('--disable-dos')
        if data.get('disable_fft'):
            cmd.append('--disable-fft')
        if data.get('disable_analytical'):
            cmd.append('--disable-analytical')
        if data.get('disable_fourier'):
            cmd.append('--disable-fourier')
        
        # Run simulation
        result = subprocess.run(
            cmd,
            cwd=PYTHON_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Extract plots from output
        plots = {}
        output = result.stdout
        if '<<<PLOTS_JSON_START>>>' in output and '<<<PLOTS_JSON_END>>>' in output:
            try:
                import json
                start_marker = '<<<PLOTS_JSON_START>>>'
                end_marker = '<<<PLOTS_JSON_END>>>'
                start_idx = output.find(start_marker) + len(start_marker)
                end_idx = output.find(end_marker)
                plots_json = output[start_idx:end_idx].strip()
                plots = json.loads(plots_json)
                # Remove plots JSON from output display
                output = output[:output.find(start_marker)] + output[end_idx + len(end_marker):]
                output = output.strip()
            except Exception as e:
                print(f"Error extracting plots: {e}")
        
        return jsonify({
            'success': result.returncode == 0,
            'output': output,
            'error': result.stderr,
            'command': ' '.join(cmd),
            'plots': plots  # Include plots in response
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Simulation timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulate/structure', methods=['POST'])
def simulate_structure():
    """Handle structure file simulation"""
    try:
        # Get form data
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get other parameters
        mode = request.form.get('mode', 'HOMO')
        model = request.form.get('model', 'FISHBONE')
        chain_direction = request.form.get('chain-direction', 'z')
        symmetry = request.form.get('symmetry', 'symmetric')
        disorder = request.form.get('disorder', '0')
        dos_points = request.form.get('dos', '5')
        
        # Save uploaded file temporarily
        file_ext = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(mode='wb', suffix=file_ext, delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Build command
            cmd = [
                'python', 'main.py',
                '--structure', tmp_path,
                '--mode', mode,
                '--model', model,
                '--chain-direction', chain_direction,
                '--symmetry', symmetry,
                '--disorder', disorder,
                '--number_of_DOS_points', dos_points
            ]
            
            # Add optional parameters
            if request.form.get('seed'):
                cmd.extend(['--seed', request.form.get('seed')])
            
            if request.form.get('export'):
                cmd.append('--export')
            
            if request.form.get('workers'):
                cmd.extend(['--workers', request.form.get('workers')])
            
            # Analysis control flags
            if request.form.get('disable_dos'):
                cmd.append('--disable-dos')
            if request.form.get(' disable_fft'):
                cmd.append('--disable-fft')
            if request.form.get('disable_analytical'):
                cmd.append('--disable-analytical')
            if request.form.get('disable_fourier'):
                cmd.append('--disable-fourier')
            
            # Run simulation
            result = subprocess.run(
                cmd,
                cwd=PYTHON_DIR,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Extract plots from output
            plots = {}
            output = result.stdout
            if '<<<PLOTS_JSON_START>>>' in output and '<<<PLOTS_JSON_END>>>' in output:
                try:
                    import json
                    start_marker = '<<<PLOTS_JSON_START>>>'
                    end_marker = '<<<PLOTS_JSON_END>>>'
                    start_idx = output.find(start_marker) + len(start_marker)
                    end_idx = output.find(end_marker)
                    plots_json = output[start_idx:end_idx].strip()
                    plots = json.loads(plots_json)
                    # Remove plots JSON from output display
                    output = output[:output.find(start_marker)] + output[end_idx + len(end_marker):]
                    output = output.strip()
                except Exception as e:
                    print(f"Error extracting plots: {e}")
            
            return jsonify({
                'success': result.returncode == 0,
                'output': output,
                'error': result.stderr,
                'command': ' '.join(cmd),
                'filename': file.filename,
                'plots': plots  # Include plots in response
            })
            
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Simulation timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/examples', methods=['GET'])
def list_examples():
    """List available example files"""
    try:
        examples = []
        python_dir = PYTHON_DIR
        
        for file in python_dir.glob('example_*'):
            if file.suffix in ['.xyz', '.cif', '.pdb']:
                examples.append({
                    'name': file.name,
                    'path': str(file),
                    'type': file.suffix[1:].upper(),
                    'size': file.stat().st_size
                })
        
        return jsonify({'examples': examples})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'python_dir': str(PYTHON_DIR),
        'python_dir_exists': PYTHON_DIR.exists()
    })


if __name__ == '__main__':
    print(f"Starting DNA Transport Simulation Backend...")
    print(f"Python directory: {PYTHON_DIR}")
    print(f"Server starting on http://localhost:5000")
    print(f"\nAvailable endpoints:")
    print(f"  POST /api/simulate/sequence - Run sequence simulation")
    print(f"  POST /api/simulate/structure - Run structure file simulation")
    print(f"  GET  /api/examples - List example files")
    print(f"  GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
