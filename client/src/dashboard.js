// Hardcoded for now; logic should be filled out before deployment
const BASE_URL = "http://localhost:5000";

const snakeToTitle = (str) => {
    return str
        .split("_")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(" ");
};

const fetchVisualizationURLs = async () => {
    
    try {
    
        const response = await fetch(`${BASE_URL}/api/visualizations`)
    
        if (!response.ok) {
            throw new Error(`HTTP Error - status: ${response.status}`);
        }

        const S3Data = await response.json();
        return S3Data;

    } catch (error) {
        console.error("Error fetching S3 URLs:", error)
    }

};

const attachVisToContainer = (container, visDesc, visUrl) => {
    const img = document.createElement("img");
    img.src = visUrl;
    img.alt = visDesc;
    img.classList.add("visualization-img");

    const caption = document.createElement("p");
    caption.textContent = visDesc;
    caption.classList.add("visualization-caption");

    container.appendChild(caption);
    container.appendChild(img);
};

const loadVisualizations = async () => {

    const visContainer = document.getElementById("visualizations-container");

    const S3Urls = await fetchVisualizationURLs();
    for (const [vis, url] of Object.entries(S3Urls)) {
        const visTitle = snakeToTitle(vis);
        attachVisToContainer(visContainer, visTitle, url);
    }

};

document.addEventListener("DOMContentLoaded", () => {
    loadVisualizations();
})