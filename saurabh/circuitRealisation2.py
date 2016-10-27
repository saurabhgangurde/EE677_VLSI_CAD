class Node(object):
	def __init__(self,number,operation=None,input1=None,input2=None):

		self._number=number							
		self._operation=operation   								
		self._input1=input1 						# here input 1 and input2 two are number of nodes
		self._input2=input2
		self._output=RothVariable('X','X')


	def __str__(self):
		if self._input1==None:
			return "number: "+str(self._number)+" operation: "+str(self._operation)
		elif self._input2==None:
			return "number: "+str(self._number)+" operation: "+str(self._operation)+" input1: "\
					+str(self._input1)
		else:
			return "number: "+str(self._number)+" operation: "+str(self._operation)+" input1: "\
					+str(self._input1)+" input2: "+str(self._input2)

class CircuitTree(object):
	def __init__(self):

		self._nodes=[]

	def addNode(self,node):
		self._nodes.append(node)

	def display(self):

		print("#############Tree display############")
		for node in self._nodes:
			print(node)

		print("###########END#######################")

 

tree=CircuitTree()

