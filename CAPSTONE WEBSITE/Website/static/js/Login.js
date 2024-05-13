// Login And Register Form Animation
// Login And Register Form Animation
// Login And Register Form Animation
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});


// Validate Password
// Validate Password
// Validate Password
function validatePassword(password) {
    var passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[A-Z]).{12,}$/;
    return passwordRegex.test(password);
}

// Send signup data to Flask route
function sendSignupData(name, email, password) {
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        console.log(data.message); // Log server response
        // Redirect to home page upon successful signup
        window.location.href = '/';
    })
    .catch((error) => {
        console.error('Error:', error.message); // Log error message
        // Display error message at the top of the page
        const errorMessageDiv = document.getElementById('error-message');
        errorMessageDiv.textContent = 'Signup failed: ' + error.message;
        errorMessageDiv.style.display = 'block';
    });
}

// Send login data to Flask route
function sendLoginData(email, password) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        console.log(data.message); // Log server response
        // Redirect to home page upon successful signup
        window.location.href = '/';
    })
    .catch((error) => {
        console.error('Error:', error.message); // Log error message
        // Display error message at the top of the page
        const errorMessageDiv = document.getElementById('error-message');
        errorMessageDiv.textContent = 'Login failed: ' + error.message;
        errorMessageDiv.style.display = 'block';
    });
}

// Add event listeners for form submission
document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("signup-password").value;
    if (!validatePassword(password)) {
        document.getElementById("signup-password-message").innerText = "Password for sign-up must be at least 12 characters long and contain at least one special character, one uppercase letter, and one number.";
        return false;
    }
    document.getElementById("signup-password-message").innerText = ""; // Clear error message
    sendSignupData(name, email, password); // Call function to send signup data
});

document.getElementById("signin-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
    var email = document.getElementById("signin-email").value;
    var password = document.getElementById("signin-password").value;
    if (!validatePassword(password)) {
        document.getElementById("signin-password-message").innerText = "Email or Password is Wrong.";
        return false;
    }
    document.getElementById("signin-password-message").innerText = ""; // Clear error message
    sendLoginData(email, password); // Call function to send login data
});
