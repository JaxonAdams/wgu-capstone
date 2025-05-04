// Hardcoded for now; logic should be filled out before deployment
const BASE_URL = "http://localhost:5000";
let currentSlide = 0;
let autoplayInterval;

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

const createSlide = (visDesc, visUrl) => {

    const slide = document.createElement("div");
    slide.classList.add("slide");

    const img = document.createElement("img");
    img.src = visUrl;
    img.alt = visDesc;
    img.classList.add("visualization-img");

    const caption = document.createElement("p");
    caption.textContent = visDesc;
    caption.classList.add("visualization-caption");

    slide.appendChild(caption);
    slide.appendChild(img);

    return slide

};

const showSlide = index => {

    const slides = document.querySelectorAll(".slide");
    if (slides.length === 0) return;

    slides.forEach((slide, i) => {
        slide.style.display = i === index ? "block" : "none";
    });

    currentSlide = index;

};

const nextSlide = () => {

    const slides = document.querySelectorAll(".slide");
    const next = (currentSlide + 1) % slides.length;
    showSlide(next);

};

const prevSlide = () => {

    const slides = document.querySelectorAll(".slide");
    const prev = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(prev);

};

const startAutoplay = () => {

    autoplayInterval = setInterval(nextSlide, 5000);

};

const stopAutoplay = () => {

    clearInterval(autoplayInterval);

};

const loadVisualizations = async () => {

    const visWrapper = document.getElementById("visualizations-wrapper");
    const S3Urls = await fetchVisualizationURLs();
    
    for (const [vis, url] of Object.entries(S3Urls)) {
        const visTitle = snakeToTitle(vis);
        const slide = createSlide(visTitle, url);
        visWrapper.appendChild(slide);
    }

    showSlide(0);

};

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("next-btn").addEventListener("click", () => {
        nextSlide();
        stopAutoplay();
        startAutoplay();
    });

    document.getElementById("prev-btn").addEventListener("click", () => {
        prevSlide();
        stopAutoplay();
        startAutoplay();
    });

    loadVisualizations().then(() => startAutoplay());

})