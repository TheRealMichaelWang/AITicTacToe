import numpy as np
import keras

model = keras.models.load_model("tic_tac_toe.keras")
cells = [0, 0, 0, 0, 0, 0, 0, 0, 0]
magicSquare = [8, 3, 4, 1, 5, 9, 6, 7, 2]

model.summary()

def print_cells():
    symbols = ["O", " ", "X"]
    for i in range(3):
        print("|", end="")
        for j in range(3):
            print(symbols[cells[i * 3 + j] + 1], end="|")
        print()

print("1 - computer goes first, -1 computer goes second")
computerTurn = int(input())
currentTurn = 1
remaining = 9

def detect_win():
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if i == j or k == i or k == j:
                    continue

                if (cells[i] + cells[j] + cells[k] == 3 * currentTurn) and (magicSquare[i] + magicSquare[j] + magicSquare[k] == 15):
                    return currentTurn

    if remaining == 0:
        return 0
    return None

while True:
    if currentTurn == computerTurn:
        res = model.predict([np.array([cells])])[0]
        max = -1
        max_i = None
        for i in range(9):
            if res[i] > max and cells[i] == 0:
                max = res[i]
                max_i = i
        assert max_i is not None
        cells[max_i] = currentTurn
    else:
        print("CURRENT_STATE")
        print_cells()
        print("Select squares 1-9, left-to-right, up-to-down")
        your_move = int(input())
        assert cells[your_move] == 0
        cells[your_move] = currentTurn

        print("AFTER YOUR MOVE")
        print_cells()

    res = detect_win()
    if res is not None:
        print(res)
        break

    currentTurn = -currentTurn
    remaining -= 1

print("END OF GAME")
print_cells()