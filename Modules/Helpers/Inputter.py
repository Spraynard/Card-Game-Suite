
class Inputter(object):
	def __init__(self, inputList):
		self.inputList = inputList
		self.choice = None

	def getInputList(self):
		return self.inputList

	def displayHR(self):
		inputs = self.getInputList()

		for i in range(inputs):
			print "#%s: %s" % ((i + 1), inputs[i])