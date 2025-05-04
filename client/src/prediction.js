// Hardcoded for now; logic should be filled out before deployment
const BASE_URL = "http://localhost:5000";

const handleFormSubmit = async event => {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
        const numVal = parseFloat(value);
        data[key] = isNaN(numVal) || value.trim() === "" ? value || null : numVal;
    });

    const payload = { data };
    console.log(payload);

    try {
        const response = await fetch(`${BASE_URL}/api/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const result = await response.json();
        alert(`Prediction result: ${JSON.stringify(result)}`);
    } catch (err) {
        console.error("Prediction failed:", err);
        alert("There was an error submitting the loan application.");
    }
};

document.getElementById("loan-form").addEventListener("submit", handleFormSubmit);