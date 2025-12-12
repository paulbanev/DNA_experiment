# Commit the new structure file support feature
# Run this script to stage and commit all the right files

Write-Host "`n=== DNA Transport Simulation - Structure File Support Commit ===" -ForegroundColor Cyan
Write-Host "`nStep 1: Staging files..." -ForegroundColor Yellow

# Updated .gitignore
Write-Host "  - .gitignore (Python entries)" -ForegroundColor Green
git add .gitignore

# Modified Python files
Write-Host "  - python/analysis.py (Unicode fix)" -ForegroundColor Green
git add python/analysis.py

# New web interface files
Write-Host "  - app_server.py (Flask backend)" -ForegroundColor Green
git add app_server.py

Write-Host "  - web_interface.html (Web UI)" -ForegroundColor Green
git add web_interface.html

Write-Host "  - WEB_APP_GUIDE.md (Documentation)" -ForegroundColor Green
git add WEB_APP_GUIDE.md

Write-Host "  - GIT_COMMIT_GUIDE.md (This guide)" -ForegroundColor Green
git add GIT_COMMIT_GUIDE.md

Write-Host "`nStep 2: Checking status..." -ForegroundColor Yellow
git status

Write-Host "`n=== Ready to Commit ===" -ForegroundColor Cyan
Write-Host "`nFiles staged for commit:" -ForegroundColor Green
git diff --cached --name-only

Write-Host "`n`nTo commit, run:" -ForegroundColor Yellow
Write-Host '  git commit -m "feat: Add structure file support (CIF/XYZ/PDB) and web interface"' -ForegroundColor White

Write-Host "`nOr use the detailed commit message:" -ForegroundColor Yellow
Write-Host '  git commit -F commit_message.txt' -ForegroundColor White
Write-Host "`n(See commit_message.txt for the full message)" -ForegroundColor Gray

Write-Host "`n=== Files Already Tracked (from earlier) ===" -ForegroundColor Cyan
Write-Host "These should already be in your branch:" -ForegroundColor Gray
Write-Host "  - python/structure_reader.py" -ForegroundColor DarkGray
Write-Host "  - python/main.py" -ForegroundColor DarkGray
Write-Host "  - python/example_chain.xyz" -ForegroundColor DarkGray
Write-Host "  - python/example_benzene.cif" -ForegroundColor DarkGray
Write-Host "  - python/example_dna.pdb" -ForegroundColor DarkGray
Write-Host "  - README.md" -ForegroundColor DarkGray
Write-Host "  - CHANGES_SUMMARY.md" -ForegroundColor DarkGray
Write-Host "  - IMPLEMENTATION_SUMMARY.md" -ForegroundColor DarkGray
Write-Host "  - QUICK_START.md" -ForegroundColor DarkGray
Write-Host "  - STRUCTURE_FILE_GUIDE.md`n" -ForegroundColor DarkGray
