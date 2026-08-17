// Show Warning Popup
function showWarning() {
    document.getElementById("warningModal").style.display = "flex";
}

// Close Warning Popup
function closeWarning() {
    document.getElementById("warningModal").style.display = "none";
}

// Open Website
function continueOpen() {
    window.open(window.qrUrl, "_blank");
}

// Close popup when clicking outside it
window.onclick = function(event) {
    const modal = document.getElementById("warningModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

// Press ESC to close popup
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeWarning();
    }
});
