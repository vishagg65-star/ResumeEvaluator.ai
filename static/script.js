document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const filenameDisplay = document.getElementById('filename');
    const form = document.getElementById('evaluation-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const resultsSection = document.getElementById('results-section');
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // --- Theme Management ---
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        themeToggle.querySelector('i').classList.replace('fa-moon', 'fa-sun');
    }

    themeToggle.addEventListener('click', () => {
        const isLight = body.classList.toggle('light-theme');
        const icon = themeToggle.querySelector('i');
        
        if (isLight) {
            icon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('theme', 'light');
        } else {
            icon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('theme', 'dark');
        }
    });

    // --- Drag & Drop Handlers ---
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drop-zone--over');
    });
    ['dragleave', 'dragend'].forEach(type => {
        dropZone.addEventListener(type, () => dropZone.classList.remove('drop-zone--over'));
    });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect();
        }
        dropZone.classList.remove('drop-zone--over');
    });

    fileInput.addEventListener('change', handleFileSelect);

    function handleFileSelect() {
        if (fileInput.files.length) {
            filenameDisplay.textContent = fileInput.files[0].name;
            fileInfo.classList.remove('hidden');
        }
    }

    // --- Form Submission ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        
        submitBtn.disabled = true;
        btnText.textContent = "Processing...";
        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/evaluate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || "Evaluation failed");
            }

            const data = await response.json();
            renderResults(data);
            resultsSection.classList.remove('hidden');
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            alert("Error: " + error.message);
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = "Analyze Resume";
            loader.classList.add('hidden');
        }
    });

    function renderResults(data) {
        document.getElementById('personal-info').innerHTML = `
            <div class="info-item"><strong>Name</strong> ${data.name || 'Not extracted'}</div>
            <div class="info-item"><strong>Email</strong> ${data.email || 'Not extracted'}</div>
            <div class="info-item"><strong>Phone</strong> ${data.phone_number || 'Not extracted'}</div>
            <div class="info-item"><strong>Inferred Role</strong> ${data.role_inferred || data.best_fit_role || 'Unknown'}</div>
        `;

        const suitability = (data.is_suitable || 'Unknown').toLowerCase();
        const suitabilityClass = suitability === 'yes' ? 'suitability-yes' : (suitability === 'no' ? 'suitability-no' : '');

        document.getElementById('evaluation-summary').innerHTML = `
            <p>${data.final_summary || 'No summary generated.'}</p>
            <div style="margin-top: 1.25rem; display: flex; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <strong>Suitability:</strong> <span class="suitability-box ${suitabilityClass}">${(data.is_suitable || 'Unknown')}</span>
            </div>
            <div style="margin-top: 0.5rem;"><small>${data.suitability_reason || ''}</small></div>
        `;

        const scores = [
            { label: 'Overall Match', value: data.final_score || 0 },
            { label: 'Skills Alignment', value: (data.skills_score || 0) * 100 },
            { label: 'Experience Depth', value: (data.experience_score || 0) * 100 },
            { label: 'Project Quality', value: (data.project_score || 0) * 100 }
        ];

        document.getElementById('score-breakdown').innerHTML = scores.map(s => `
            <div class="score-item">
                <div class="score-label"><span>${s.label}</span><span>${Math.round(s.value)}%</span></div>
                <div class="progress-container"><div class="progress-bar" style="width: ${s.value}%"></div></div>
            </div>
        `).join('');

        document.getElementById('skills-detail').innerHTML = `
            <div style="margin-bottom: 1.5rem">
                <strong>Matched Skills</strong>
                <div class="tags">${(data.matched_skills || []).map(s => `<span class="tag">${s}</span>`).join('') || 'None'}</div>
            </div>
            <div>
                <strong style="color: var(--error-color)">Missing Skills</strong>
                <div class="tags">${(data.missing_skills || []).map(s => `<span class="tag tag-missing">${s}</span>`).join('') || 'None'}</div>
            </div>
        `;

        // Detailed Experience
        document.getElementById('experience-detail').innerHTML = `
            <div class="info-item"><strong>Total Experience</strong> ${data.total_experience ? data.total_experience.toFixed(1) + ' years' : 'Not specified'}</div>
            <div class="info-item"><strong>Job Switch Pattern</strong> ${data.job_switch_pattern || 'Not analyzed'}</div>
            <div style="margin-top: 1rem">
                <strong>Companies</strong>
                <div class="tags">${(data.companies || []).map(c => `<span class="tag">${c}</span>`).join('') || 'None'}</div>
            </div>
        `;

        // Detailed Projects
        document.getElementById('projects-detail').innerHTML = `
            <div style="margin-bottom: 1.5rem">
                <strong>Tech Stack used in Projects</strong>
                <div class="tags">${(data.project_tech_stack || []).map(t => `<span class="tag" style="background: rgba(139, 92, 246, 0.15); border-color: rgba(139, 92, 246, 0.3); color: #c084fc;">${t}</span>`).join('') || 'None'}</div>
            </div>
            <div class="project-summary-box">
                <strong>Key Details</strong>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-secondary); white-space: pre-wrap;">${data.projects_section || 'No detailed project section found.'}</div>
            </div>
        `;
    }
});
