// Auto Rezyume - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Close alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// File validation for photo upload
function validatePhotoFile(input) {
    const file = input.files[0];
    if (file) {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const maxSize = 5 * 1024 * 1024; // 5MB

        if (!allowedTypes.includes(file.type)) {
            alert('Faqat JPG, JPEG yoki PNG formatida rasm yuklashingiz mumkin!');
            input.value = '';
            return false;
        }

        if (file.size > maxSize) {
            alert('Rasm hajmi 5MB dan oshmasligi kerak!');
            input.value = '';
            return false;
        }

        return true;
    }
}
