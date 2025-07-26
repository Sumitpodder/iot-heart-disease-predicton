function openProfile() {
    document.getElementById("profilePopup").style.display = "block";
}

function closeProfile() {
    document.getElementById("profilePopup").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    // Booking button animation (without alert)
    document.querySelector(".Test-now").addEventListener("click", function () {
        this.textContent = "cheking...";
        setTimeout(() => {
            this.textContent = "Test Now";
            // alert removed
        }, 2000);
    });

    // Simple hover effect for services
    document.querySelectorAll(".service").forEach(service => {
        service.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.1)";
            this.style.transition = "0.3s";
        });
        service.addEventListener("mouseleave", function () {
            this.style.transform = "scale(1)";
        });
    });

});