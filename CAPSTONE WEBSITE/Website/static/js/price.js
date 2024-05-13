// Pricing Section
// Pricing Section
// Pricing Section
document.addEventListener("DOMContentLoaded", function () {
    const monthlyButton = document.querySelector(".monthly-payments");
    const annualButton = document.querySelector(".annual-payments");
    const monthlySessions = document.querySelectorAll(".box.month");
    const annualSessions = document.querySelectorAll(".box.annual");

    monthlyButton.addEventListener("click", function () {
        // Show monthly sessions
        monthlySessions.forEach(function (session) {
            session.style.display = "block";
        });

        // Hide annual sessions
        annualSessions.forEach(function (session) {
            session.style.display = "none";
        });

        // Add active class to monthly button and remove from annual button
        monthlyButton.classList.add("active");
        annualButton.classList.remove("active");
    });

    annualButton.addEventListener("click", function () {
        // Show annual sessions
        annualSessions.forEach(function (session) {
            session.style.display = "block";
        });

        // Hide monthly sessions
        monthlySessions.forEach(function (session) {
            session.style.display = "none";
        });

        // Add active class to annual button and remove from monthly button
        annualButton.classList.add("active");
        monthlyButton.classList.remove("active");
    });
});
