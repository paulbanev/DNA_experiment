# Running the DNA Transport Simulation Web App

## Quick Start

### 1. Start the Backend Server

Open a terminal and run:

```bash
cd c:\Users\Pavlos` Banev\Develop\DNA_experiment
python app_server.py
```

You should see:
```
Starting DNA Transport Simulation Backend...
Server starting on http://localhost:5000

Available endpoints:
  POST /api/simulate/sequence - Run sequence simulation
  POST /api/simulate/structure - Run structure file simulation
  GET  /api/examples - List example files
  GET  /api/health - Health check
 * Running on http://127.0.0.1:5000
```

### 2. Open the Web Interface

Open in your browser:
```
file:///c:/Users/Pavlos%20Banev/Develop/DNA_experiment/web_interface.html
```

Or simply double-click `web_interface.html`

## Using the Web Interface

### Tab 1: DNA Sequence (Original Method)

1. Enter a DNA sequence (e.g., `AAAAA`, `ATGCATGC`)
2. Select parameters:
   - Electronic Mode (HOMO/LUMO)
   - Transport Model (FISHBONE, WIRE, LADDER, etc.)
   - Hopping Symmetry
   - Disorder Type
   - Number of DOS Points
3. Click **Run Simulation**
4. Wait for results (will appear at the bottom)

✅ **Test this to verify the old logic still works!**

### Tab 2: Structure File (New Method)

1. Click to upload or drag & drop a structure file:
   - `python/example_chain.xyz` - 10-atom carbon chain
   - `python/example_benzene.cif` - Benzene molecule  
   - `python/example_dna.pdb` - DNA base pair
2. Select parameters:
   - Electronic Mode (HOMO/LUMO)
   - Transport Model
   - **Chain Direction** (x, y, or z) - NEW parameter!
   - Hopping Symmetry
   - Disorder Type
   - Number of DOS Points
3. Click **Run Simulation**
4. Wait for results

✅ **Test this to verify the new file upload functionality!**

## Architecture

```
┌─────────────────┐
│  web_interface  │  (Frontend - HTML/CSS/JavaScript)
│     .html       │  Opens in browser
└────────┬────────┘
         │ HTTP API Calls
         ↓
┌─────────────────┐
│   app_server.py │  (Backend - Flask)
│                 │  Runs on localhost:5000
└────────┬────────┘
         │ Executes commands
         ↓
┌─────────────────┐
│   python/       │  (Python Simulation)
│   main.py       │  - sequence.py (old)
│                 │  - structure_reader.py (new)
└─────────────────┘
```

## API Endpoints

The backend provides these endpoints:

### POST `/api/simulate/sequence`
Run simulation with DNA sequence input.

**Request Body (JSON):**
```json
{
  "sequence": "AAAAA",
  "mode": "HOMO",
  "model": "FISHBONE",
  "symmetry": "symmetric",
  "disorder": "0",
  "dos": "5"
}
```

### POST `/api/simulate/structure`
Run simulation with structure file upload.

**Request Body (FormData):**
- `file`: The structure file (CIF/XYZ/PDB)
- `mode`: HOMO or LUMO
- `model`: FISHBONE, WIRE, LADDER, etc.
- `chain_direction`: x, y, or z
- `symmetry`: symmetric or asymmetric
- `disorder`: 0-5
- `dos`: Number of DOS points

### GET `/api/examples`
List available example files.

### GET `/api/health`
Health check endpoint.

## Testing Checklist

- [ ] **Backend is running** (you should see Flask output in terminal)
- [ ] **Web interface opens** in browser
- [ ] **Test Sequence Tab**:
  - [ ] Enter `AAAAA`, HOMO, FISHBONE, symmetric, disorder 0
  - [ ] Click "Run Simulation"
  - [ ] See results appear
- [ ] **Test Structure Tab**:
  - [ ] Upload `python/example_chain.xyz`
  - [ ] Select HOMO, FISHBONE, z-axis, symmetric, disorder 0
  - [ ] Click "Run Simulation"
  - [ ] See results appear
- [ ] **Test File Upload**:
  - [ ] Try `example_benzene.cif` with different chain direction
  - [ ] Try `example_dna.pdb`
- [ ] **Verify Results**:
  - [ ] Check output shows "Simulation completed successfully"
  - [ ] Check command is displayed
  - [ ] Check eigenvalues, probabilities, etc. are shown

## Troubleshooting

### "Failed to connect to backend server"
**Solution:** Make sure `python app_server.py` is running in a terminal.

### "Module 'flask_cors' not found"
**Solution:** Run `pip install flask-cors`

### Backend shows errors
**Solution:** Check that:
- You're in the correct directory
- Python dependencies are installed (numpy, biopython, matplotlib, pandas)
- The `python/` subdirectory exists with all the simulation files

### Results don't appear
**Solution:**
1. Check browser console for errors (F12)
2. Check backend terminal for error messages
3. Ensure the simulation completed (check terminal output)

## Features Comparison

| Feature | Sequence Tab | Structure Tab |
|---------|--------------|---------------|
| **Input Type** | DNA sequence string | CIF/XYZ/PDB file |
| **Parameters** | Pre-defined for DNA | Extracted from atomic coordinates |
| **Chain Direction** | ❌ Not needed | ✅ **NEW!** (x/y/z) |
| **File Upload** | ❌ No | ✅ **NEW!** |
| **Example Files** | Built-in sequences | 3 example files provided |

## Files Created

### Web App Files:
- `web_interface.html` - Beautiful frontend interface
- `app_server.py` - Flask backend server

### Example Structure Files:
- `python/example_chain.xyz` - Carbon chain
- `python/example_benzene.cif` - Benzene
- `python/example_dna.pdb` - DNA base pair

### Core Modules:
- `python/structure_reader.py` - NEW! Reads CIF/XYZ/PDB
- `python/main.py` - Updated to support both inputs
- `python/sequence.py` - Original (unchanged)

## Next Steps

After testing the web interface:

1. ✅ Verify old sequence logic still works
2. ✅ Test new structure file upload
3. ✅ Try all three file formats (CIF, XYZ, PDB)
4. ✅ Compare results between methods
5. 📊 Visualize results (plots are saved in `python/results/`)

Enjoy your enhanced DNA Transport Simulation! 🧬
