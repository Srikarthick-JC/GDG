function checkSystem() {
    fetch("http://localhost:5000/status")
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = data.system_status;

            if (data.silent_failure) {
                document.getElementById("alert").innerText = "⚠️ Silent Failure Detected";
                document.getElementById("alert").style.color = "red";
            } else {
                document.getElementById("alert").innerText = "No Issues Detected";
                document.getElementById("alert").style.color = "green";
            }

            document.getElementById("explanation").innerText = data.explanation;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
