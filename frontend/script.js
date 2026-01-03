function checkSystem() {
    fetch("https://silent-failure-detection.onrender.com")
        .then(response => response.json())
        .then(data => {

            // Always show system status
            document.getElementById("status").innerText = data.system_status;

            // Always show metrics (THIS IS THE KEY CHANGE)
            document.getElementById("metrics").innerText =
                `Latency: ${data.latency_ms} ms | Output Size: ${data.output_size_kb} KB`;

            // Alert logic
            if (data.silent_failure) {
                document.getElementById("alert").innerText = "⚠️ Silent Failure Detected";
                document.getElementById("alert").style.color = "red";
            } else {
                document.getElementById("alert").innerText = "No issues detected (Within Baseline)";
                document.getElementById("alert").style.color = "green";
            }

            // Explanation
            document.getElementById("explanation").innerText = data.explanation;
        });
}

