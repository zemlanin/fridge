from random import randint
from Tkinter import E, W, Frame, Button, Entry, Tk

class valve:
	def __init__(self, parent, x, y, t = False):
		self.parent = parent
		self.state = t
		self.x, self.y = x, y

	def click(self):
		self.state = not self.state

class door:
	def __init__(self, X, Y):
		self.plate = [[valve(self, j, i) for i in xrange(Y)] for j in xrange(X)]
		for k in xrange(X*Y):
		#for k in xrange(1):
			a, b = randint(0, X-1), randint(0, Y-1)
			#print a, b
			self.turn(a, b)

	def turn(self, X, Y):
		for t in self.plate[X]:
			t.click()
		for t in self.plate[:X]+self.plate[X+1:]:
			t[Y].click()

	def check(self):
		out = True
		for r in [item for sublist in self.plate for item in sublist]:
				if self.plate[0][0].state != r.state:
					out = False
					break
		return out

	def main(self):
		print '\n'.join([str([1 if t.state else 0 for t in y]) for y in self.plate])

class App:
	def __init__(self, master):
		rows = 10
		columns = 7
		self.d = door(rows, columns)
		master.title("The Fridge")
		self.frame = Frame(master)

		controls = Frame(self.frame)
		self.start = Button(controls,
						text = "Restart",
						width = 6,
						command = self.restart
						)
		self.start.grid(row = 0, column = 4, columnspan = 2, sticky = E)
		self.rowtext = Entry(controls, width = 4)
		self.rowtext.grid(row = 0, column = 0, columnspan = 2, sticky = W)
		self.coltext = Entry(controls, width = 4)
		self.coltext.grid(row = 0, column = 2, columnspan = 2, sticky = E)
		controls.grid(row = 0, column = 0, columnspan = 7)

		self.bttns = []
		for i in xrange(rows):
			for j in xrange(columns):
				cb = Button(self.frame,
						bg = "green" if self.d.plate[i][j].state else "red",
						text = " ",
						command = self.click(self.bttns, self.d, i, j) # coolhack
						)
				cb.grid(row = i+1, column = j)
				self.bttns.append(cb)

		self.frame.grid(column = 0, row = 0)

	def restart(self):
		rows = int(self.rowtext.get()) if self.rowtext.get() else 10
		columns = int(self.coltext.get()) if self.coltext.get() else 7
		if columns < 5:
			columns = 5
		if rows < 4:
			rows = 4 
		self.d = door(rows, columns)
		for b in self.bttns:
			b.destroy()

		self.bttns = []
		for i in xrange(rows):
			for j in xrange(columns):
				cb = Button(self.frame,
						bg = "green" if self.d.plate[i][j].state else "red",
						text = " ",
						command = self.click(self.bttns, self.d, i, j) # coolhack
						)
				cb.grid(row = i+1, column = j)
				self.bttns.append(cb)

		self.start.configure(text = "Restart")

	def click(self, buttons, dr, x, y):
		def real(): # Those coolhack
			dr.turn(x, y)
			b_state = "disabled" if dr.check() else "normal"
			if dr.check():
				self.start.configure(text = "WIN")
			rows = len(dr.plate)
			columns = len(dr.plate[0])
			b_iter = iter(buttons)
			for i in xrange(rows):
				for j in xrange(columns):
					b_iter.next().configure(bg = "green" if dr.plate[i][j].state else "red", state = b_state)
		return real

if __name__ == "__main__":
	root = Tk()
	app = App(root)
	root.mainloop()