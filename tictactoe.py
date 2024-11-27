import random
import numpy as np

#a simulator for a single game of tic-tac-toe
class TicTacToe:
    def __init__(self):
        self.history_x = []
        self.history_o = []
        self.cells = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.remaining_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.currentMarker = 1

    #returns 1 if X wins, -1 if O wins, 0 if draw, None if nothing
    def place(self, location):
        magicSquare = [8, 3, 4, 1, 5, 9, 6, 7, 2]

        assert self.cells[location] == 0

        if self.currentMarker > 0: #x
            self.history_x.append((self.cells.copy(), location))
        elif self.currentMarker < 0: #o
            self.history_o.append((self.cells.copy(), location))
        self.remaining_moves.remove(location)

        self.cells[location] = self.currentMarker

        #returns 1 if X wins, -1 if O wins, 0 if draw, None if nothing
        def detect_win():
            for i in range(9):
                for j in range(9):
                    for k in range(9):
                        if i == j or k == i or k == j:
                            continue

                        if self.cells[i] + self.cells[j] + self.cells[k] == 3 * self.currentMarker and magicSquare[i] + magicSquare[j] + magicSquare[k] == 15:
                            return self.currentMarker

            if len(self.remaining_moves) == 0:
                return 0
            return None
        winner = detect_win()

        if winner is None:
            self.currentMarker = -self.currentMarker
        else:
            assert winner == 0 or winner == self.currentMarker

        return winner

    #returns 2 elements
    #first element of the tuple is a list of the winning moves
    #second element of the tuple is a list of the loosing moves
    def simulate(self):
        def internal_simulate():
            assert len(self.remaining_moves) == 9
            while True:
                location = random.choice(self.remaining_moves)
                internal_res = self.place(location)

                if internal_res is not None:
                    return internal_res

                assert len(self.remaining_moves) > 0

        #transoforms the o array of moves into the same format as the x's
        def normalize_os():
            for entry in self.history_o:
                for i in range(len(entry[0])):
                    entry[0][i] = -entry[0][i]

        res = internal_simulate()
        normalize_os()

        if res > 0: #x win
            return self.history_x, self.history_o
        elif res < 0: #o win
            return self.history_o, self.history_x
        else: #draw
            return self.history_x + self.history_o, []

#board state is a 9 element array with elements 1, -1, and 0
#1 represents your tic-tac-toe piece
#-1 represents your opponents tic-tac-toe piece
#0 represents unfilled cell
def hash_board_state(board_state):
    #we are effectively converting a base 3 number to base 10
    sum_hash = 0
    for elem in board_state:
        digit = elem + 1
        sum_hash = 3 * sum_hash + digit
    return sum_hash

class Simulator:
    def __init__(self):
        self.board_states = { }

    #executes many tic-tac-toe simulations
    def simulate(self, num_simulations):
        def add(board_state, move, delta_win, delta_loss):
            state_hash = hash_board_state(board_state)
            if state_hash not in self.board_states:
                self.board_states[state_hash] = [board_state, [[0, 0] for _ in range(9)]]

            self.board_states[state_hash][1][move][0] += delta_win
            self.board_states[state_hash][1][move][1] += delta_loss

        for i in range(num_simulations):
            tic_tac_toe = TicTacToe()
            wins, losses =  tic_tac_toe.simulate()

            for entry in wins:
                add(entry[0], entry[1], 1, 0)
            for entry in losses:
                add(entry[0], entry[1], 0, 1)

    #gets the test cases as 2 numpy arrays: input, expected output
    def test_cases(self):
        input_cases = np.array([
            item[0]
            for item in self.board_states.values()
        ])

        expected_output = np.array([
            np.array([(0.5 if wls[0] == wls[1] else (wls[0] / (wls[0] + wls[1]))) for wls in item[1]])
            for item in self.board_states.values()
        ])

        return input_cases, expected_output

#now we actually run the simulations
simulator = Simulator()
simulator.simulate(100000)
test_inputs, expected_outputs = simulator.test_cases()

np.savetxt("input_cases", test_inputs)
np.savetxt("expected_output", expected_outputs)