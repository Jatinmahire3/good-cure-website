document.getElementById('symptom-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting

    // Get symptom input
    const symptoms = document.getElementById('symptoms').value.trim();

    if (!symptoms) {
        alert("Please enter your symptoms.");
        return;
    }

    // Simulating an AI diagnosis result
    let diagnosisResult = "Based on your symptoms, we recommend the following doctors:";

    // Simulate AI logic here (e.g., if-else or API call to a backend AI model)
    const aiResults = [
        "Dr. John Doe (General Practitioner)",
        "Dr. Jane Smith (Dermatologist)",
        "Dr. Alex Black (Cardiologist)"
    ];

    // Display results
    const resultContainer = document.getElementById('ai-result');
    resultContainer.innerHTML = diagnosisResult + "<br><br>" + aiResults.join("<br>");
    resultContainer.classList.add('show');
});
