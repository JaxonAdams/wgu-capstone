// Hardcoded for now; logic should be filled out before deployment
const BASE_URL = "http://localhost:5000";

const handleFormSubmit = async event => {
    event.preventDefault();

    const predictionContainer = document.getElementById("prediction-container");

    const form = event.target;
    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
        const numVal = parseFloat(value);
        data[key] = isNaN(numVal) || value.trim() === "" ? value || null : numVal;
    });

    const payload = { data };

    try {
        const response = await fetch(`${BASE_URL}/api/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const result = await response.json();
        console.log(result);
        
        if ("will_default" in result) {
            predictionContainer.innerHTML = `<strong>Prediction:</strong> The applicant is <span style="color: ${result.will_default ? 'red' : 'green'};">${result.will_default ? 'likely to default' : 'not likely to default'}.</span>`;
        } else {
            predictionContainer.innerHTML = `<span style="color: red;">Error: Invalid response format from server.</span>`;
        }
    } catch (err) {
        console.error("Prediction failed:", err);
        predictionContainer.innerHTML = `<span style="color: red;">Error: ${error.message}</span>`;
    }
};

document.getElementById("loan-form").addEventListener("submit", handleFormSubmit);