from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9
current_player = "X"

winning_positions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner():
    for position in winning_positions:
        a, b, c = position
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def make_move():
    global current_player

    data = request.get_json()
    index = data.get("index")

    if not isinstance(index, int) or not 0 <= index < 9:
        return jsonify({"error": "Invalid position"}), 400

    if board[index] != "" or check_winner() or "" not in board:
        return jsonify({"error": "Invalid move"}), 400

    board[index] = current_player
    winner = check_winner()

    if winner:
        status = f"Player {winner} wins!"
    elif "" not in board:
        status = "It's a draw!"
    else:
        current_player = "O" if current_player == "X" else "X"
        status = f"Player {current_player}'s turn"

    return jsonify({
        "board": board,
        "status": status,
        "winner": winner
    })

@app.route("/restart", methods=["POST"])
def restart():
    global board, current_player
    board = [""] * 9
    current_player = "X"

    return jsonify({
        "board": board,
        "status": "Player X's turn"
    })

if __name__ == "__main__":
    app.run(debug=True)
