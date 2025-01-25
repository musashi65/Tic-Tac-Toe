import random

def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def display_board(board):
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < len(board)-1:
            print("-"*9)
            
def check_win(board):
    winning_combinations = [
        [[0, 0], [0, 1], [0, 2]],  # Top row
        [[1, 0], [1, 1], [1, 2]],  # Middle row
        [[2, 0], [2, 1], [2, 2]],  # Bottom row
        [[0, 0], [1, 0], [2, 0]],  # Left column
        [[0, 1], [1, 1], [2, 1]],  # Middle column
        [[0, 2], [1, 2], [2, 2]],  # Right column
        [[0, 0], [1, 1], [2, 2]],  # Left to right diagonal
        [[0, 2], [1, 1], [2, 0]]   # Right to left diagonal
    ]
    
    for combination in winning_combinations:
        values = [board[row][col] for row, col in combination]
        if values.count("X") == 3:
            return "X"
        elif values.count("O") == 3:
            return "O"
        
    if cells_left == 0:
        return "Tie"
    
    return False


def find_empty_pos(board):
    empty_pos = []
    for row_index, row in enumerate(board):
        for col_index, value in enumerate(row):
            if value == " ":
                empty_pos.append((row_index, col_index))
    return empty_pos

def weak_ai_move(board):
    return random.choice(find_empty_pos(board))

def player_move(board, player_symbol):
    while True:
        try:
            n = int(input("Number between 1-9: "))
            if isinstance(n, int) and n > 0 and n < 10:
                row = (n-1) // 3
                col = (n-1) % 3
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    break
                
                else:
                    print("Cell isn't empty")
            else:
                print("Please choose a number between 1 and 9")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9")

def minimax(board, ai_symbol, depth, is_maximizing, alpha, beta):
    opponent_symbol = "X" if ai_symbol == "O" else "O"
    empty_pos = find_empty_pos(board)
    
    winner = check_win(board)
    if winner == ai_symbol:
        return 1000
    elif winner == opponent_symbol:
        return -1000
    elif winner == "Tie" or len(empty_pos) == 0:
        return 0
    
    if is_maximizing:
        best_score = float("-inf")
        
        for row, col in empty_pos: 
            board[row][col] = ai_symbol
            score = minimax(board, ai_symbol, depth + 1, False, alpha, beta)
            
            board[row][col] = " "
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    
    else:
        best_score = float("inf")
        for row, col in empty_pos:
            board[row][col] = opponent_symbol
            score = minimax(board, ai_symbol, depth + 1, True, alpha, beta)
            
            board[row][col] = " "
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score
    

def find_best_move(board, ai_symbol):
    best_score = -1000
    best_move = None
    empty_pos = find_empty_pos(board)
    
    for row, col in empty_pos:
        board[row][col] = ai_symbol
        score = minimax(board, ai_symbol, 0, False, float("-inf"), float("inf"))
        board[row][col] = " "
        
        if score >= best_score:
            best_score = score
            best_move = (row, col)
    print(f"Terminator thinks the best move is: {best_move}")        
    return best_move

def replay_game():
    play_again = input("Press (Y) to play again, (N) to stop: ").lower()
    if play_again.startswith("y"):
        return True
    exit("Thanks for playing!")
    
def main():
    board = create_board()
    display_board(board)
    
    global cells_left
    cells_left = 9
    turn = 0
    
    player_symbol = input("Do you want to play as 'X' or 'O': ").upper()
    while player_symbol not in ["X", "O"]:
        player_symbol = input("Do you want to play as 'X' or 'O': ").upper()
    ai_symbol = "X" if player_symbol == "O" else "O"
    
    game_mode = int(input("Who do you want to play against\n 1. (P v P)\n 2. (P v Weak AI)\n 3. (P v Strong AI):\n"))
    while game_mode not in [1, 2, 3]:
        game_mode = int(input("Who do you want to play against\n 1. (P v P)\n 2. (P v Weak AI)\n 3. (P v Strong AI):\n"))
    
    while True:
        if game_mode == 1:
            if turn % 2 == 0:
                player_move(board, player_symbol)
                turn += 1
                cells_left -= 1
            else:
                player_move(board, ai_symbol)
                turn += 1
                cells_left -= 1
 
        elif game_mode == 2:
            if turn % 2 == 0:
                player_move(board, player_symbol)
                turn += 1
                cells_left -= 1
            else:
                weak_ai_row, weak_ai_col = weak_ai_move(board)
                board[weak_ai_row][weak_ai_col] = ai_symbol
                turn += 1
                cells_left -= 1
                print("Weak AI made its move. Your turn")
                
        else:
            if turn % 2 == 0:
                player_move(board, player_symbol)
                turn += 1
                cells_left -= 1
            else:
                strong_ai_row, strong_ai_col = find_best_move(board, ai_symbol)
                board[strong_ai_row][strong_ai_col] = ai_symbol
                turn += 1
                cells_left -= 1
                
        is_winner = check_win(board)
        
        if is_winner:
            if is_winner == "Tie":
                display_board(board)
                print("Tie!")
                if replay_game():
                    main()
            
            else:
                display_board(board)
                print(f"Congratulations, '{is_winner}' won this game!")
                if is_winner == ai_symbol and game_mode == 3:
                    print("You got terminated 💀💀💀")
                if replay_game():
                    main()
                    
        display_board(board)

if __name__ == "__main__":
    main()
