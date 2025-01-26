document.addEventListener('DOMContentLoaded', () => {
    const scanLine = document.getElementById('scan-line');
    const result = document.getElementById('result');
    const prescriptionDetails = document.getElementById('prescription-details');

    // Show the scan line
    scanLine.style.display = 'block';

    // Start scanning animation
    scanLine.classList.add('scan-line');

    // Wait for the animation to finish before showing the result and prescription details
    const animationDuration = 4000; // Match the CSS animation duration (4 seconds)
    setTimeout(() => {
        scanLine.style.display = 'none'; // Hide the scan line after animation
        result.style.display = 'block'; // Show the prediction result

        // Add class based on result
        if (result.textContent === 'Pneumonia Detected') {
            prescriptionDetails.classList.add('pneumonia');
        } else if (result.textContent === 'Healthy') {
            prescriptionDetails.classList.add('healthy');
        } else if (result.textContent === 'Unknown') {
            prescriptionDetails.classList.add('unknown');
        }
        prescriptionDetails.style.display = 'block'; // Show the prescription details
    }, animationDuration);
});
