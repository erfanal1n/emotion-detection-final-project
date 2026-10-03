const form = document.getElementById("emotion-form");
const textInput = document.getElementById("textToAnalyze");
const result = document.getElementById("system_response");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = textInput.value.trim();

    if (!text) {
        result.textContent = "Please enter text to analyze.";
        result.classList.add("error");
        textInput.focus();
        return;
    }

    result.textContent = "Analyzing your text...";
    result.classList.remove("error");

    try {
        const query = new URLSearchParams({ textToAnalyze: text });
        const response = await fetch(`/emotionDetector?${query}`);
        result.textContent = await response.text();
        result.classList.toggle("error", !response.ok);
    } catch {
        result.textContent = "The emotion service is temporarily unavailable.";
        result.classList.add("error");
    }
});
