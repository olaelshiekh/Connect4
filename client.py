import tkinter as tk
import socket
from tkinter import messagebox

class Connect4GUI:
    def on_closing(self):
        """Handle the event when the window is closed."""
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            self.server_socket.close()  # Close the network connection
            self.master.destroy()  # Close the GUI window


    def __init__(self, master):
        self.master = master
        master.title("Connect 4")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(('127.0.0.1', 5000))  # Connect to the server

        self.buttons = [[None for _ in range(7)] for _ in range(6)]
        for row in range(6):
            for col in range(7):
                button = tk.Button(master, text="",  # Ensure text is initially set to empty
                                command=lambda r=row, c=col: self.send_move(c), 
                                height=3, width=6, bg='light blue')
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window closing

    def send_move(self, col):
        try:
            self.server_socket.send(str(col).encode())
            response = self.server_socket.recv(1024).decode()
            self.update_board(response)
        except Exception as e:
            messagebox.showinfo("Connection Issue", str(e))

    def update_board(self, message):
        print("Received message:", message)  # Debugging output
        if "wins" in message:
            messagebox.showinfo("Game Over", message)
            self.master.destroy()  # Closes the GUI when the game ends
        elif "accepted" in message:
            try:
                parts = message.split(',')
                player = parts[0].split()[-1]  # Assuming the message format is like "Player 1 accepted,2,4"
                row = int(parts[1])
                col = int(parts[2])
                # Assign color and text based on player
                color = 'red' if player == '1' else 'green'
                text = 'X' if player == '1' else 'O'
                # Update button color and text
                if 0 <= row < 6 and 0 <= col < 7:
                    self.buttons[row][col].config(bg=color, text=text)
                else:
                    print("Invalid indices received:", row, col)  # Debug: Invalid index
            except ValueError as e:
                print("Error processing message:", e)  # Error handling
        else:
            messagebox.showinfo("Info", message)


def main():
    root = tk.Tk()
    gui = Connect4GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
