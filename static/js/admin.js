// Admin Panel JavaScript

// Toggle add/edit form visibility
function toggleForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const required = form.querySelectorAll('[required]');
            let valid = true;
            
            required.forEach(field => {
                if (!field.value.trim()) {
                    field.closest('.form-group-admin').classList.add('error');
                    valid = false;
                }
            });
            
            if (!valid) {
                e.preventDefault();
                const firstError = form.querySelector('.form-group-admin.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
        
        // Clear error on input
        form.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('input', function() {
                const group = this.closest('.form-group-admin');
                if (group && group.classList.contains('error')) {
                    group.classList.remove('error');
                }
            });
        });
    });
    
    // Confirm deletions
    const deleteButtons = document.querySelectorAll('.btn-admin-danger');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-generate slug from title
    const titleInputs = document.querySelectorAll('input[name="title"]');
    titleInputs.forEach(input => {
        const slugInput = document.querySelector('input[name="slug"]');
        if (slugInput) {
            input.addEventListener('blur', function() {
                if (!slugInput.value) {
                    const slug = this.value.toLowerCase()
                        .replace(/[^\w\s-]/g, '')
                        .replace(/[\s_-]+/g, '-')
                        .replace(/^-+|-+$/g, '');
                    slugInput.value = slug;
                }
            });
        }
    });
    
    // Toggle sidebar on mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.querySelector('.admin-sidebar').classList.toggle('collapsed');
        });
    }
    
    // Status badge colors
    const statusBadges = document.querySelectorAll('.badge');
    statusBadges.forEach(badge => {
        const status = badge.textContent.toLowerCase();
        if (status.includes('new')) badge.classList.add('badge-new');
        else if (status.includes('following')) badge.classList.add('badge-following');
        else if (status.includes('quoted')) badge.classList.add('badge-quoted');
        else if (status.includes('completed')) badge.classList.add('badge-completed');
    });
});
