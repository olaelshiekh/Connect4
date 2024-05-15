import socket
import threading

# Game settings
NUM_ROWS = 6
NUM_COLS = 7

def init_board():
    return [[0] * NUM_COLS for _ in range(NUM_ROWS)]

def valid_move(col, board):
    return board[0][col] == 0  # Checks if the top of the column is free

def make_move(col, board, player):
    """Attempts to place a player's marker in the specified column."""
    for row in range(NUM_ROWS-1, -1, -1):  # Start from the bottom of the column
        if board[row][col] == 0:
            board[row][col] = player
            return row  # Return the row where the piece was placed
    return None  # If the column is full, return None

def check_win(board):
    # Check horizontal locations for win
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != 0:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS-3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != 0:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != 0:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] != 0:
                return True

    return False

def client_thread(conn, addr, board, player):
    """Handles each client's connection and game moves."""
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            col = int(data)
            if valid_move(col, board):
                row = make_move(col, board, player)
                if row is not None:
                    win = check_win(board)
                    if win:
                        message = f"Player {player} wins!"
                    else:
                        message = f"Player {player} accepted,{row},{col}"
                else:
                    message = "Column full. Try a different move."
            else:
                message = "Invalid move. Try again."
            conn.send(message.encode())
            if win:
                break
    except Exception as e:
        print(f"Error with client {addr}: {str(e)}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

        
def start_server():
    host = '127.0.0.1'
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server is listening for connections...")

    board = init_board()
    current_player = 1

    try:
        while True:
            conn, addr = server_socket.accept()
            print("Connected by", addr)
            threading.Thread(target=client_thread, args=(conn, addr, board, current_player)).start()
            current_player = 2 if current_player == 1 else 1
    finally:
        server_socket.close()
        print("Server shutdown.")

if __name__ == "__main__":
    start_server()
