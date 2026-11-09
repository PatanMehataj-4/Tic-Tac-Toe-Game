
const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");

async function makeMove(index) {
    try {
        const response = await fetch("/move", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({index: index})
        });

        const data = await response.json();

        if (!response.ok) {
            statusText.textContent = data.error;
            return;
        }

        updateBoard(data);
    } catch (error) {
        statusText.textContent = "Server connection error";
    }
}

function updateBoard(data) {
    cells.forEach((cell, index) => {
        cell.textContent = data.board[index];
    });

    statusText.textContent = data.status;
}

async function restartGame() {
    const response = await fetch("/restart", {
        method: "POST"
    });

    const data = await response.json();
    updateBoard(data);
}
