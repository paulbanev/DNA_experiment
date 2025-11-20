// DNA Transport Simulation - Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('simulationForm');
    const jobListElement = document.getElementById('jobList');

    // Auto-detect CPU cores for workers field
    if (navigator.hardwareConcurrency) {
        const workersInput = document.getElementById('workers');
        workersInput.placeholder = `Auto (${navigator.hardwareConcurrency} cores detected)`;
    }

    // Load job list on page load
    loadJobs();

    // Refresh job list every 5 seconds
    setInterval(loadJobs, 5000);

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const params = {};

        // Collect form data
        for (const [key, value] of formData.entries()) {
            if (value === 'on') {
                // Checkbox
                params[key] = true;
            } else if (key === 'disorder' || key === 'workers' || key === 'dos_bins' || key === 'seed') {
                // Numbers
                const num = parseInt(value);
                if (!isNaN(num) && value !== '') {
                    params[key] = num;
                }
            } else {
                // Strings
                params[key] = value;
            }
        }

        // Set workers to null if 0 (auto-detect)
        if (params.workers === 0) {
            params.workers = null;
        }

        // Add unchecked checkboxes as false
        const checkboxes = ['export', 'disable_dos', 'disable_analytical',
            'disable_fft', 'disable_dipole_fft', 'disable_fourier'];
        checkboxes.forEach(name => {
            if (!(name in params)) {
                params[name] = false;
            }
        });

        try {
            // Submit simulation
            const button = form.querySelector('button[type="submit"]');
            button.disabled = true;
            button.innerHTML = '⏳ Starting...';

            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(params)
            });

            const result = await response.json();

            if (response.ok) {
                // Success - redirect to results page
                window.location.href = `/results/${result.job_id}`;
            } else {
                // Error
                alert(`Error: ${result.error || 'Unknown error'}`);
                button.disabled = false;
                button.innerHTML = '🚀 Run Simulation';
            }
        } catch (error) {
            console.error('Error submitting simulation:', error);
            alert(`Error: ${error.message}`);
            const button = form.querySelector('button[type="submit"]');
            button.disabled = false;
            button.innerHTML = '🚀 Run Simulation';
        }
    });

    async function loadJobs() {
        try {
            const response = await fetch('/api/jobs');
            const jobs = await response.json();

            if (jobs.length === 0) {
                jobListElement.innerHTML = '<p class="loading">No simulations yet. Start one above!</p>';
                return;
            }

            jobListElement.innerHTML = jobs.slice(0, 10).map(job => `
                <div class="job-item" onclick="window.location.href='/results/${job.id}'">
                    <div class="job-info">
                        <div class="job-sequence">${job.sequence || 'Unknown'}</div>
                        <div class="job-time">${formatDate(job.created_at)}</div>
                    </div>
                    <div class="job-status status-${job.status}">
                        ${formatStatus(job.status)}
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading jobs:', error);
            jobListElement.innerHTML = '<p class="loading">Error loading job history</p>';
        }
    }

    function formatStatus(status) {
        const statusMap = {
            'queued': '⏳ Queued',
            'running': '▶️ Running',
            'completed': '✅ Completed',
            'failed': '❌ Failed'
        };
        return statusMap[status] || status;
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;

        // Less than 1 minute
        if (diff < 60000) {
            return 'Just now';
        }
        // Less than 1 hour
        if (diff < 3600000) {
            const mins = Math.floor(diff / 60000);
            return `${mins} minute${mins > 1 ? 's' : ''} ago`;
        }
        // Less than 24 hours
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        }
        // Otherwise show date
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
});
