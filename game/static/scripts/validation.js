function init() {
    ValidateRegistration();
}

function ValidateRegistration() {
    var roleSelect = document.querySelector('select[name="role_id"]');
    roleSelect.value = '2'
    // Disable options except for the "Student" option
    for (var i = 0; i < roleSelect.options.length; i++) {
        if (roleSelect.options[i].value !== '2') {
            roleSelect.options[i].disabled = true; // Disable non-student options
        }
    }
}

window.onload = init;