# Tic-Tac-Toe Game in Python

# Section 1: Set Up Game
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

# Section 2: Gathering Player's Move
def get_player_move(board, player):
    while True:
        try:
            row, col = map(int, input("Enter row and column (0-2, space-separated): ").split())
            if board[row][col] == " ":
                board[row][col] = player
                break
            else:
                print("Cell already occupied. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column as two numbers between 0 and 2.")

# Section 3: Determine AI's Move (To be implemented next week)
def get_ai_move(board, ai_player):
    pass  # Placeholder for AI logic

# Section 4: Check if Player or AI Won
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

# Main Game Loop
def tic_tac_toe():
    board = initialize_board()
    players = ["X", "O"]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    
    for turn in range(9):
        player = players[turn % 2]
        print(f"Player {player}'s turn.")
        
        if player == "X":
            get_player_move(board, player)
        else:
            get_ai_move(board, player)
        
        print_board(board)
        
        if check_winner(board, player):
            print(f"Player {player} wins!")
            return
        
        if is_full(board):
            print("It's a tie!")
            return

if __name__ == "__main__":
    tic_tac_toe()