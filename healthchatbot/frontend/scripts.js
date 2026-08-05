function renderTable(data) {
    let html = "<table border='1'>";
    data.forEach(row => {
        html += "<tr>";
        row.forEach(col => {
            html += `<td>${col}</td>`;
        });
        html += "</tr>";
    });
    html += "</table>";
    return html;
}

async function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();

    if (!message) return;

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div class="user">${message}</div>`;

    try {
        console.log("Sending POST request...");

        let response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        let data = await response.json();
        console.log("Response:", data);

        if (data.error) {
            chatBox.innerHTML += `<div class="bot">Error: ${data.error}</div>`;
        } else {
            chatBox.innerHTML += `<div class="bot">SQL: ${data.sql}</div>`;
            chatBox.innerHTML += `<div class="bot">${renderTable(data.result)}</div>`;
        }

    } catch (error) {
        console.error("Fetch Error:", error);
        chatBox.innerHTML += `<div class="bot">Server error</div>`;
    }

    input.value = "";
}