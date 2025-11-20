# Logging and Observability Fixes

## Problem

Zero observability in Portainer - logs were being written to files inside the container instead of stdout/stderr where Docker can capture them.

## Changes Made

### 1. Dockerfile - Gunicorn Logging

**File**: [`Dockerfile`](file:///c:/Users/Pavlos%20Banev/Develop/DNA_experiment%20-%20Copy/Dockerfile)

Changed Gunicorn command from logging to files:
```dockerfile
# Before - logs to files (invisible to Portainer)
CMD ["gunicorn", ..., "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "web_app:app"]

# After - logs to stdout/stderr (visible in Portainer)
CMD ["gunicorn", ..., "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "web_app:app"]
```

**Key changes**:
- `--access-logfile -` → Log HTTP access to stdout
- `--error-logfile -` → Log errors to stderr
- `--log-level info` → Set log level for visibility

### 2. Docker Compose - Log Driver Configuration

**File**: [`docker-compose.prod.yml`](file:///c:/Users/Pavlos%20Banev/Develop/DNA_experiment%20-%20Copy/docker-compose.prod.yml)

Added logging configuration to manage log size:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"     # Max 10MB per log file
    max-file: "3"       # Keep 3 files (30MB total)
```

Removed unnecessary `dna_logs` volume since logs now go to Docker's logging system.

## How It Works Now

1. **Gunicorn** outputs all logs to stdout/stderr
2. **Docker** captures these streams using the json-file driver
3. **Portainer** reads from Docker's log system and displays in UI

## Benefits

✅ **Full visibility** in Portainer logs viewer  
✅ **Real-time monitoring** of requests and errors  
✅ **Log rotation** prevents disk fillup  
✅ **No volume mounts needed** for logs  
✅ **Standard Docker practices** for container logging

## Viewing Logs in Portainer

After rebuilding and redeploying:

1. Go to Portainer → Containers
2. Click on `dna-simulation-web`
3. Click "Logs" tab
4. You'll now see:
   - Gunicorn startup messages
   - HTTP requests (access log)
   - Application errors
   - Python exceptions

## Next Steps

To apply these changes:

```bash
# 1. Added openpyxl to requirements.txt
# 2. Rebuild image with new logging config
docker build -t pavlosbanev/dna_experiment:latest .

# 3. Push to registry
docker push pavlosbanev/dna_experiment:latest

# 4. Deploy updated stack
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

## What You'll See

Example log output in Portainer:
```
2025-11-20 21:05:32 [INFO] Starting gunicorn 21.2.0
2025-11-20 21:05:32 [INFO] Listening at: http://0.0.0.0:5000
2025-11-20 21:05:32 [INFO] Using worker: sync
2025-11-20 21:05:32 [INFO] Booting worker with pid: 8
192.168.1.100 - - [20/Nov/2025:21:06:15 +0000] "GET / HTTP/1.1" 200  
192.168.1.100 - - [20/Nov/2025:21:07:43 +0000] "POST /api/simulate HTTP/1.1" 200
```

## Files Modified

- ✅ [`Dockerfile`](file:///c:/Users/Pavlos%20Banev/Develop/DNA_experiment%20-%20Copy/Dockerfile)
- ✅ [`docker-compose.prod.yml`](file:///c:/Users/Pavlos%20Banev/Develop/DNA_experiment%20-%20Copy/docker-compose.prod.yml)  
- ✅ [`python/requirements.txt`](file:///c:/Users/Pavlos%20Banev/Develop/DNA_experiment%20-%20Copy/python/requirements.txt)
