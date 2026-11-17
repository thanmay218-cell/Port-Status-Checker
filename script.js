async function checkPort() {
    const host = document.getElementById("host").value.trim();
    const port = document.getElementById("port").value.trim();
    const result = document.getElementById("result");

    if (!host || !port) {
        result.innerHTML = "Please enter all details.";
        return;
    }

    result.innerHTML = "Checking port...";

    try {
        const response = await fetch("http://127.0.0.1:5000/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ host, port })
        });

        const data = await response.json();

        if (!response.ok) {
            result.innerHTML = data.error;
            return;
        }

        result.innerHTML = `
            Host: ${data.host}<br>
            Port: ${data.port}<br>
            Status: <span style="color:${data.status === 'OPEN' ? 'green' : 'red'}">${data.status}</span>
        `;

    } catch (error) {
        result.innerHTML = "Unable to connect to the server.";
    }
}

function clearResult() {
    document.getElementById("host").value = "";
    document.getElementById("port").value = "";
    document.getElementById("result").innerHTML = "";
}