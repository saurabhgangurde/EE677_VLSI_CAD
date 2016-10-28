
#from pyeda.inter import*
from RothAlgebra import RothVariable
from copy import deepcopy

ZERO=RothVariable(0,0)
ONE=RothVariable(1,1)
D=RothVariable(1,0)
DBAR=RothVariable(0,1)
X=RothVariable('X','X')


class Node(object):
	def __init__(self,number,operation=None,input1=None,input2=None):

		self._number=number							
		self._operation=operation   								
		self._input1=input1 						# here input 1 and input2 two are number of nodes
		self._input2=input2
		self._output=X

	def setOutput(self,output):
		self._output=output

	def getNumber(self):
		return self._number

	def getOutput(self):
		return self._output

	def getInputs(self):
		return [self._input1,self._input2]

	def getOperation(self):
		return self._operation

	def __repr__(self):
		if self._input1==None:
			return "("+str(self._number)+","+str(self._operation)+")"
		elif self._input2==None:
			return "("+str(self._number)+","+str(self._operation)+","\
					+str(self._input1._number) +")"
		else:
			return "("+str(self._number)+","+str(self._operation)+","\
					+str(self._input1._number)+","+str(self._input2._number)+")"


class CircuitTree(object):
	def __init__(self):

		self._nodes=[]
		self._Fanout=[]

	def addNode(self,node):
		self._nodes.append(node)

	def getNode(self,index):
		return self._nodes[index]


	def createTree(self,Fanin):
		for i in range(len(Fanin)):

			gate=Fanin[i]
			if gate==None:
				self._nodes.append(Node(i))
			elif len(gate)==2:
				input1=self._nodes[Fanin[i][1]]
				self._nodes.append(Node(i,Fanin[i][0],input1))
			else:

				input1=self._nodes[Fanin[i][1]]
				input2=self._nodes[Fanin[i][2]]
				self._nodes.append(Node(i,Fanin[i][0],input1,input2))

	def createFanout(self,Fanin):

		self._Fanout=[[] for i in range(len(Fanin))]
		for i in range(len(Fanin)):							#i is index of node for which Fanout is to be found
			for j in range(len(Fanin)):						#j itertaes over all elements of Fanin to find i in its input
				if Fanin[j]!=None:							#jth node has no Fanin	
					for find in range(1,len(Fanin[j])):
						if i==Fanin[j][find]:				#if ith node found in Fanin of j
							self._Fanout[i].append(j)
							break

	def displayFanout(self):
		print("fanout: ",self._Fanout)

	def __repr__(self):

		print(self._nodes)
		return ""


	def propagate(self,stuckAtNode,stuckAtFault,Fanin):

		#print (paths)

		tempNodeOutput=[X for i in range(len(self._nodes))]
		if stuckAtFault==0:
			tempNodeOutput[stuckAtNode]=D
			
		else:
			tempNodeOutput[stuckAtNode]=DBAR

		tempNodeOutput_copy=deepcopy(tempNodeOutput)

		print("going in recursive propagate")

		return self.recursive_propagate(stuckAtNode,Fanin,tempNodeOutput_copy)

		# 	print(path)
		# 	for i in range(len(path)):

				
		# 		if path[i]==stuckAtNode:
		# 			pass
		# 		else:
		# 			fanin_current_node=Fanin[path[i]]

		# 			print(fanin_current_node)

		# 			#############if operation is and or nand######################

		# 			if fanin_current_node[0]=="And" or fanin_current_node[0]=="Nand":
		# 				if fanin_current_node[1]==path[i-1]:

		# 					if tempNodeOutput[fanin_current_node[2]]== X:	## should add equality operator overload in class

		# 						tempNodeOutput[fanin_current_node[2]]=ONE	

		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] 
		# 						print("irst if and")
		# 						print(fanin_current_node)
		# 						print(tempNodeOutput)

		# 						if fanin_current_node[0]=="Nand":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]
		# 						# print (path[i],tempNodeOutput[path[i]])

		# 					else:

		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] & tempNodeOutput[fanin_current_node[2]]

		# 						if fanin_current_node[0]=="Nand":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

		# 						# print (path[i],tempNodeOutput[path[i]])

		# 						if not (tempNodeOutput[path[i]]==D or tempNodeOutput[path[i]]==DBAR):
		# 							print("inside break and1")
		# 							break

		# 				else:


		# 					if tempNodeOutput[fanin_current_node[1]]== X:	

		# 						tempNodeOutput[fanin_current_node[1]]=RothVariable(1,1)	

		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[2]] 

		# 						if fanin_current_node[0]=="Nand":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]
		# 						# print (path[i],tempNodeOutput[path[i]])

		# 					else:

		# 						print("HERE")
		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] & tempNodeOutput[fanin_current_node[2]]

		# 						print(tempNodeOutput)
		# 						if fanin_current_node[0]=="Nand":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

		# 						# print (path[i],tempNodeOutput[path[i]])

		# 						if not (tempNodeOutput[path[i]]==D or tempNodeOutput[path[i]]==DBAR):
		# 							print("inside break and2")
		# 							break


		# 			############################# if operation is Or or NOR####################################
		# 			elif fanin_current_node[0]=="Or" or fanin_current_node[0]=="Nor":
		# 				if fanin_current_node[1]==path[i-1]:

		# 					if tempNodeOutput[fanin_current_node[2]]== X:	## should add equality operator overload in class

		# 						tempNodeOutput[fanin_current_node[2]]=ZERO	

		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] 

		# 						if fanin_current_node[0]=="Nor":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

		# 						#print (path[i],tempNodeOutput[path[i]])


		# 					else:

		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] & tempNodeOutput[fanin_current_node[2]]

		# 						if fanin_current_node[0]=="Nor":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

		# 						#print (path[i],tempNodeOutput[path[i]])

		# 						if not (tempNodeOutput[path[i]]==D or tempNodeOutput[path[i]]==DBAR):
		# 							break

		# 				else:

		# 					if tempNodeOutput[fanin_current_node[1]]== X:	## should add equality operator overload in class

		# 						tempNodeOutput[fanin_current_node[1]]=ZERO	

		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[2]] 

		# 						if fanin_current_node[0]=="Nor":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

		# 						#print (path[i],tempNodeOutput[path[i]])



		# 					else:


		# 						tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] | tempNodeOutput[fanin_current_node[2]]

		# 						if fanin_current_node[0]=="Nor":
		# 							tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

		# 						#print (path[i],tempNodeOutput[path[i]])

		# 						if not (tempNodeOutput[path[i]]==D or tempNodeOutput[path[i]]==DBAR):
		# 							break

		# 			elif fanin_current_node[0]=="Not":
		# 				tempNodeOutput[path[i]]=~tempNodeOutput[path[i-1]]


		# 	#print(tempNodeOutput)						

		# print(tempNodeOutput)
		# NodeOutputs.append(tempNodeOutput)

	def recursive_propagate(self,current_node,Fanin,tempNodeOutput):

		paths=[]
		p1=[]
		pathFinder(self._Fanout,current_node,paths,p1)
		# print(current_node)
		# print(tempNodeOutput)
		# print(paths)
		vectors=[]
		for path in paths:

			if len(self._Fanout[path[0]])==0:
				return tempNodeOutput

			else:
				fanin_next_node=Fanin[path[1]]

				if fanin_next_node[0]=="And" or fanin_next_node[0]=="Nand":
					if fanin_next_node[1]==path[0]:

						if tempNodeOutput[fanin_next_node[2]]== X:	

							# print("going for two choices")
							##################recursion for 1st decision########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[2]]=ONE	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

							if fanin_next_node[0]=="Nand":
								tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							# print("choice 1 ans:",vector)
							if not (vector==-1):
								vectors.append(vector)


							#################recursion for second decision##########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[2]]=tempNodeOutput[fanin_next_node[1]]	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

							if fanin_next_node[0]=="Nand":
								tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							# print("choice 2 ans:",vector)

							if not (vector==-1 or len(vector)==0 ):
								vectors.append(vector)

							####################################################################
	

						else:

							tempNodeOutput[path[1]]= tempNodeOutput[fanin_next_node[1]] & tempNodeOutput[fanin_next_node[2]]

							if fanin_next_node[0]=="Nand":
								tempNodeOutput[path[1]]=~tempNodeOutput[path[1]]


							if not (tempNodeOutput[path[1]]==D or tempNodeOutput[path[1]]==DBAR):
								return -1

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput)
							if not (vector==-1 or len(vector==0)):
								vectors.append(vector)

		return vectors




	def setOutputs(self,outputs):

		for i in range(len(self._nodes)):
			self._nodes[i].setOutput(outputs[i])






def backTrace(tree,NodeOutputs,no_inputs):

		outputAssignments=[]

		for i in range(len(NodeOutputs)):
			tempNodeOutput=NodeOutputs[i]

			tree.setOutputs(NodeOutputs[i])
			backTraceList=[j for j in range(no_inputs-1,len(NodeOutputs[i])) if NodeOutputs[i][j]==ONE or NodeOutputs[i][j]==ZERO]
			print(backTraceList)
			while not(len(backTraceList)==0):

				current_node=tree.getNode(backTraceList[0])
				# print(current_node)
				del backTraceList[0]

				if current_node.getOperation()=="And" or current_node.getOperation()=="Nand":

					
					if current_node.getOutput()==ONE:
						# print("here")
						current_node_inputs=current_node.getInputs()

						# print(current_node)

						if current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X:
							tempNodeOutput[current_node_inputs[0].getNumber()]=ONE
							tempNodeOutput[current_node_inputs[1].getNumber()]=ONE
							backTraceList.append(current_node_inputs[0].getNumber())
							backTraceList.append(current_node_inputs[1].getNumber())
						else:

							if not(current_node_inputs[0].getOutput()==ONE and \
								current_node_inputs[1].getOutput()==ONE):
								return -1

					else:

						tempNodeOutput[current_node_inputs[0].getNumber()]=ZERO
						tempNodeOutput[current_node_inputs[1].getNumber()]=X

						tempNodeOutput_copy1=deepcopy(tempNodeOutput)
						tree_copy1=deepcopy(tree)

						list1=backTrace(tree_copy1,tempNodeOutput_copy1,no_inputs)

						if not (list1==-1):
							tempNodeOutput.append(list1)

						tempNodeOutput[current_node_inputs[0].getNumber()]=ONE
						tempNodeOutput[current_node_inputs[1].getNumber()]=ZERO

						tempNodeOutput_copy1=deepcopy(tempNodeOutput)
						tree_copy1=deepcopy(tree)

						list1=backTrace(tree_copy1,tempNodeOutput_copy1,no_inputs)

						if not (list1==-1):
							tempNodeOutput.append(list1)

			outputAssignments.append(tempNodeOutput)			

		return outputAssignments



				# else:

				# 	if current_node.getOperation()=="Or" or current_node.getOperation()=="Nor":



				# 		if current_node.getOutput()==ZERO:

				# 			current_node_inputs=current_node.getInputs()
				# 			if current_node_inputs[0].getOutput()==X and current_node_inputs.getOutput()==X:
				# 				tempNodeOutput[current_node_inputs[0].getNumber()]=ZERO
				# 				tempNodeOutput[current_node_inputs[1].getNumber()]=ZERO
				# 				backTraceList.append(current_node_inputs[0].getNumber())
				# 				backTraceList.append(current_node_inputs[1].getNumber())
				# 			else:
				# 				return -1


				# 		else:

 

Fanin=[None,None,None,None,["And",0,1],["And",4,1],["And",2,3],["And",4,5],["And",7,6]]

#################some temp global variables#######################
paths = []																	#Final path
p1=[]																		#temp path		
NodeOutputs=[]			
####################################################################
def pathFinder(Fanout,n,paths,p1):
	# global path
	# global p1
	p1.append(n)   															#append current node
	if(Fanout[n]== []):
		p2=p1[:]															#shallow copy
		paths.append(p2) 													#append current list to all paths
		p1.pop()															#pop last node
		return 
	for i in range(len(Fanout[n])):
		pathFinder(Fanout,Fanout[n][i],paths,p1)   									#next Fanout of current node
	p1.pop()																#pop last node
	return

tree=CircuitTree()

tree.createTree(Fanin)
tree.createFanout(Fanin)

# pathFinder(tree._Fanout,5,paths,p1)
# print(paths)

# pathFinder(tree._Fanout,6,paths,p1)
# print(paths)



# print(tree)

# tree.displayFanout()

# path=[]
# paths=[]




NodeOutputs=tree.propagate(4,0,Fanin)

print(NodeOutputs)

# finalAssignments=backTrace(tree,NodeOutputs,4)

# print(finalAssignments)



