
// Panel Section 
// Panel Section 
// Panel Section 
document.addEventListener('DOMContentLoaded', function () {
    const passwordCells = document.querySelectorAll('.password');

    passwordCells.forEach(cell => {
        const password = cell.dataset.password;
        const stars = '*'.repeat(password.length); // Generate stars based on password length

        cell.addEventListener('click', function () {
            // On click, reveal the actual password
            this.textContent = password;
        });

        cell.addEventListener('mouseenter', function () {
            // On hover, reveal the actual password
            this.textContent = password;
        });

        cell.addEventListener('mouseleave', function () {
            // On mouse leave, revert to stars
            this.textContent = stars;
        });
    });



});