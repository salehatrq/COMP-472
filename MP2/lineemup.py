# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3


	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend

	# Parametrized constructor
	def __init__(self, n, b, pb, s, d1, d2, t, recommend = True):
		self.n = n
		self.b = b
		self.pb = pb
		self.s = s
		self.d1 = d1
		self.d2 = d2
		self.t = t
		self.current_state = []
		self.initialize_game()
		self.recommend = recommend

		self.f = open(F'gameTrace-{self.n}{self.b}{self.s}{self.t}.txt', "w")
		self.f.write(F'n={self.n} b={self.b} s={self.s} t={self.t}\n')
		self.f.write(F'blocs={self.pb}\n\n')
		
	def initialize_game(self):
		for y in range(self.n):
			arr = []
			for x in range(self.n):				
				for (bloc) in self.pb:
					if (bloc) == (y, x):
						arr.append("#")  # put blocs(#)
					else:
						arr.append(",")
			self.current_state.append(arr)

		self.insert_blocs()
		# Player X always plays first
		self.player_turn = 'X'

	def double_check(self):
		for i in range(self.n):
			for j in range(self.n):
				for (bloc) in self.pb:
					if(bloc) == (i,j):
						#print((i,j))										
						self.current_state[i][j] = "#"

	def insert_blocs(self):
		for x in range(self.n):
			for y in range(self.n):
				for (bloc) in self.pb:
					if(bloc) != (x,y):				
						self.current_state[x][y] = "."

		self.double_check()
						

	def draw_board(self):
		print()
		self.f.write("\n")
		for y in range(0, self.n):
			for x in range(0, self.n):
				print(F'{self.current_state[x][y]}', end="")
				self.f.write(F'{self.current_state[x][y]}')
			print()
			self.f.write("\n")
		print()
		self.f.write("\n")		

	def is_valid(self, px, py):
		if px < 0 or px > self.n or py < 0 or py > self.n:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		# Vertical win
		lineCount = 0
		for i in range(self.n):
			for j in range(self.n-1):
				if(self.current_state[i][j] == "#" or self.current_state[i][j] == "." or self.current_state[i][j] != self.current_state[i][j+1]):
					lineCount = 0
				else:
					lineCount += 1
				if(lineCount == self.s-1):
					return self.current_state[i][j]
		
		# Horizontal win
		lineCount = 0
		for i in range(self.n):
			for j in range(self.n-1):
				if(self.current_state[j][i] == "#" or self.current_state[j][i] == "." or self.current_state[j][i] != self.current_state[j][i+1]):
					lineCount = 0
				else:
					lineCount += 1
				if(lineCount == self.s-1):
					return self.current_state[j][i]
		
		# Main diagonal win
		lineCount = 0
		for i in range((self.n + 1) - self.s):
			for j in range(self.n - 1 - i):
				if(self.current_state[j][j+i] == "#" or self.current_state[j][j+i] == "." or self.current_state[j][j+i] != self.current_state[j+1][j+i+1]):
					lineCount = 0
				else:
					lineCount += 1
				if(lineCount == self.s-1):
					return self.current_state[j][j + i]
		
		# Second diagonal win
		lineCount = 0
		for i in range((self.n + 1) - self.s):
			for j in range(self.n - 1 - i):
				if(self.current_state[j][self.n - 1 - j - i] == "#" or self.current_state[j][self.n - 1 - j- i] == "."
				or self.current_state[j][self.n - 1 - j - i] != self.current_state[j+1][self.n - 1 - (j + 1) - i]):
					lineCount = 0
				else: 
					lineCount += 1
				if(lineCount == self.s-1):
					return self.current_state[j+1][self.n - 1 - j - i]

		# Diagonals with self.s smaller than self.n
		# Right
		lineCount = 0
		if self.s < self.n:
			for m in range(self.n - self.s):
				for n in range(self.n - 2 - m):
					if (self.current_state[n + m + 1][self.n - 1 - n] == "#" or self.current_state[n + m + 1][self.n - 1 - n] == "."
						or self.current_state[n + m + 1][self.n - 1 - n] != self.current_state[n + m + 2][self.n - 1 - (n+1)]):
						lineCount = 0
					else: 
						lineCount += 1
					if lineCount == self.s-1:
						return self.current_state[n + m + 1][self.n - 1 - n]
		
		# Left
		lineCount = 0
		if self.s < self.n:
			for m in range(self.n - self.s):
				for n in range(self.n - 2 - m):
					if (self.current_state[n + m + 1][n] == "#" or self.current_state[n + m + 1][n] == "."
					or self.current_state[n + m + 1][n] != self.current_state[n + m + 2][n + 1]):
						lineCount = 0
					else: 
						lineCount += 1
					if lineCount == self.s-1:
						return self.current_state[n + m + 1][n]
		
		# Is whole board full?
		for i in range(0, self.n):
			for j in range(0, self.n):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
				self.f.write('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
				self.f.write('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
				self.f.write("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		# Dictionary that maps all values of x to an integer value to allow for validation
		dict_x_coord = {
						'A': 0,
						'B': 1,
						'C': 2,
						'D': 3,
						'E': 4,
						'F': 5,
						'G': 6,
						'H': 7,
						'I': 8,
						'J': 9
		}

		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = input('enter the x coordinate: ')
			py = int(input('enter the y coordinate: '))

			mapped_x = dict_x_coord[px]

			if self.is_valid(mapped_x, py):
				return (mapped_x,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, depth, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if depth == 0:
					return (value, x, y)
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == self.d2:
							x = i
							y = j
						(v, _, _) = self.minimax(depth = depth - 1, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == self.d1:
							x = i
							y = j	
						(v, _, _) = self.minimax(depth = depth - 1, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, depth=0, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if depth == 0:
					return (value, x, y)
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == self.d2:
							x = i
							y = j
						(v, _, _) = self.alphabeta(alpha, beta, depth = depth - 1, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == self.d1:
							x = i
							y = j
						(v, _, _) = self.alphabeta(alpha, beta, depth = depth - 1, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self, algo=None,player_x=None,player_o=None, player_x_heuristic=None, player_o_heuristic=None):
		# Dictionary that maps all coordiante values of x to its corresponding string for display purposes
		dict_x_coord = {
						0: 'A',
						1: 'B',
						2: 'C',
						3: 'D',
						4: 'E',
						5: 'F',
						6: 'G',
						7: 'H',
						8: 'I',
						9: 'J'
		}

		# Write parameters of each player to the file
		if player_x == self.AI:
			self.f.write(F'Player 1: AI d={self.d1} ')
		else:
			self.f.write(F'Player 1: HUMAN d={self.d1} ')
		if algo == self.ALPHABETA:
			self.f.write(F'a=True ')
		else:
			self.f.write(F'a=False ')

		if(player_x_heuristic == self.e1):
			self.f.write(F'e1 (regular) \n')
		else:
			self.f.write(F'e2 (defensive)\n')

		if player_o == self.AI:
			self.f.write(F'Player 2: AI d={self.d2} ')
		else:
			self.f.write(F'Player 2: HUMAN d={self.d2} ')
		if algo == self.ALPHABETA:
			self.f.write(F'a=True ')
		else:
			self.f.write(F'a=False ')
		
		if(player_o_heuristic == self.e1):
			self.f.write(F'e1 (regular)')
		else:
			self.f.write(F'e2 (defensive)')

		self.f.write('\n')

		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		if player_x_heuristic == None:
			player_x_heuristic == self.e1
		if player_o_heuristic == None:
			player_x_heuristic == self.e2
		
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(depth = self.d1, max=False)
				else:
					(_, x, y) = self.minimax(depth = self.d2, max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(depth = self.d1, max=False)
				else:
					(m, x, y) = self.alphabeta(depth = self.d2, max=True)
			end = time.time()
			elapsed_t = end - start
			if (elapsed_t > self.t):
				print(F'Player {self.player_turn} is eliminated for taking too much time to return a move.')
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						self.f.write("Evaluation time: " + str(round(end - start, 7)))
						self.f.write("\n")
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						self.f.write("Evaluation time: " + str(round(end - start, 7)))
						self.f.write("\n")
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')

			mapped_x = dict_x_coord[x]
			self.f.write("Move taken: " + mapped_x + " " + str(y))

			self.current_state[x][y] = self.player_turn
			self.switch_player()
	
	# Determining number of white pieces
	def num_white(self):
		num_X = 0
		for y in range(0, self.n):
			for x in range(0, self.n):
				if self.current_state[x][y] == 'X':
					num_X = num_X + 1
		return num_X			

	# Determining number of black pieces
	def num_black(self):
		num_O = 0
		for y in range(0, self.n):
			for x in range(0, self.n):
				if self.current_state[x][y] == 'O':
					num_O = num_O + 1
		return num_O

	# Developing e1 (simple heuristic)
	def e1(self):
		e = self.num_black() - self.num_white()
		return e

	# Developing e2 (complex heuristic)
	def e2(self):
		m_constant = (self.n % self.s) + 1
		line_c = m_constant * (3 * self.s - (self.n - 2)) # the number of possible solution lines for a board given the line size
		e = line_c - (self.num_black() + self.num_white())
		
		return e

def main():
	n = 4
	b = 4
	pb = [(0, 0), (0, 3), (3,3), (3,0)]
	s = 3
	d1 = 6
	d2 = 6
	t = 1


	g = Game(n, b, pb, s, d1, d2, t, recommend=True)
	#g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN, player_x_heuristic=None, player_o_heuristic=None)
	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.HUMAN, player_x_heuristic=None, player_o_heuristic=None)


if __name__ == "__main__":
	main()
