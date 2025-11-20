# DNA Transport Simulation - Web Interface

A Flask-based web application for running DNA quantum transport simulations through your browser.

## Features

- 🎯 **Easy Parameter Configuration** - All simulation parameters in one clean form
- ⚡ **Multiple Concurrent Simulations** - Run several simulations at once
- 📊 **Real-Time Progress** - Track simulation status live
- 📈 **Results Visualization** - View plots directly in browser
- 💾 **Download Results** - Get Excel files and images
- 🔄 **Job History** - See recent simulations

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-web.txt
```

### 2. Start the Server

```bash
python web_app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## Usage

### Running a Simulation

1. Enter your DNA sequence (e.g., `ATGCAT`)
2. Select electronic mode (HOMO/LUMO)
3. Choose transport model
4. Configure advanced options if needed
5. Click "Run Simulation"
6. View results on the results page

### Parameters

**Required:**
- **Sequence**: DNA sequence using A, T, G, C bases
- **Mode**: HOMO (highest occupied) or LUMO (lowest unoccupied)
- **Model**: Transport model (Fishbone, Wire, Ladder, etc.)

**Optional:**
- **Symmetry**: Hopping symmetry type
- **Disorder**: Disorder type (0-10)
- **Workers**: Number of CPU cores (0 = auto-detect)
- **DOS Bins**: Energy histogram resolution
- **Random Seed**: For reproducible results

**Calculation Flags:**
- Disable specific calculations for faster runtime
- Recommended for quick tests: disable analytical + dipole FFT

## API Endpoints

The web app provides a REST API:

- `POST /api/simulate` - Start a new simulation
- `GET /api/status/<job_id>` - Check simulation status
- `GET /api/jobs` - List all jobs
- `GET /api/download/<job_id>/<filename>` - Download results

### Example API Usage

```python
import requests

# Start simulation
response = requests.post('http://localhost:5000/api/simulate', json={
    'sequence': 'ATGCAT',
    'mode': 'HOMO',
    'model': 'FISHBONE',
    'symmetry': 'symmetric',
    'disorder': 0,
    'workers': 4,
    'export': True
})

job_id = response.json()['job_id']

# Check status
status = requests.get(f'http://localhost:5000/api/status/{job_id}')
print(status.json())
```

## Server Deployment

### Using Gunicorn (Production)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Using Docker

```bash
# Build image
docker build -t dna-simulation .

# Run container
docker run -p 5000:5000 dna-simulation
```

### Environment Variables

- `FLASK_SECRET_KEY`: Secret key for sessions
- `RESULTS_DIR`: Custom results directory path
- `MAX_WORKERS`: Limit concurrent simulations

## File Structure

```
python/
├── web_app.py              # Flask backend
├── templates/
│   ├── index.html          # Main form
│   └── results.html        # Results display
├── static/
│   ├── style.css           # Styling
│   └── app.js              # Frontend JavaScript
└── requirements-web.txt    # Web dependencies
```

## Troubleshooting

**Port already in use:**
```bash
# Use a different port
python web_app.py --port 8000
```

**Simulations not starting:**
- Check that `main.py` is in the correct location
- Verify Python path in `web_app.py`
- Check console output for error messages

**Results not showing:**
- Ensure results directory exists and is writable
- Check browser console for JavaScript errors
- Verify API endpoints are accessible

## Notes

- Job data is stored in memory - restarting the server clears history
- For production, consider using Redis or a database for job storage
- Results files are shared across all users - use authentication for multi-user deployments

## License

Same license as the main DNA simulation project.
