
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
				return [tempNodeOutput]

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
							if not (vector==-1 or len(vector)==0):

								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)

							
							#################recursion for second decision##########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[2]]=tempNodeOutput[fanin_next_node[1]]	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

							if fanin_next_node[0]=="Nand":
								tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							# print("choice 2 ans:",vector)

							if not (vector==-1 or len(vector)==0 ):
								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)
								

						###################################################################
	

						else:

							tempNodeOutput[path[1]]= tempNodeOutput[fanin_next_node[1]] & tempNodeOutput[fanin_next_node[2]]

							if fanin_next_node[0]=="Nand":
								tempNodeOutput[path[1]]=~tempNodeOutput[path[1]]


							if not (tempNodeOutput[path[1]]==D or tempNodeOutput[path[1]]==DBAR):
								return -1

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput)
							if not (vector==-1 or len(vector)==0):
								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)

		return vectors




	def setOutputs(self,outputs):

		for i in range(len(self._nodes)):
			self._nodes[i].setOutput(outputs[i])



def PrebackTrace(tree,NodeOutputs,stuckAtNode,stuckAtFault):
	vectors=[]
	faultNode=tree.getNode(stuckAtNode)
	operation=faultNode.getOperation()
	faultNode_inputs=faultNode.getInputs()

	if stuckAtFault==0:

		if operation=="And":
			inputs_desired_outputs=[[RothVariable(1,1),RothVariable(1,1)]]

	else:
		if operation=="And":
			inputs_desired_outputs=[[RothVariable('X','X'),RothVariable(0,0)],[RothVariable(0,0),RothVariable('X','X')]]



	for entry in NodeOutputs:

		for outputs in inputs_desired_outputs:
			tempNodeOutput=entry
			tempNodeOutput[faultNode_inputs[0].getNumber()]=outputs[0]
			tempNodeOutput[faultNode_inputs[1].getNumber()]=outputs[1]
			if tempNodeOutput not in vectors:
				vectors.append(tempNodeOutput)

	print "vectors",vectors
	return vectors


def backTrace(tree,NodeOutputs,no_inputs):

	outputAssignments=[]

	for i in range(len(NodeOutputs)):

		tempNodeOutputs=NodeOutputs[i]
		tempOutputAssignments=[]
		tree.setOutputs(tempNodeOutputs)

		backTraceList=[j for j in range(no_inputs,len(tempNodeOutputs)) if tempNodeOutputs[j]==ONE or tempNodeOutputs[j]==ZERO]

		
		tempNodeOutputs=[tempNodeOutputs]
		while not(len(backTraceList)==0):

			current_node=tree.getNode(backTraceList[0])
	

			del backTraceList[0]
			while not(len(tempNodeOutputs)==0):
				
				if current_node.getOperation()=="And" or current_node.getOperation()=="Nand":

					current_node_inputs=current_node.getInputs()

					if current_node.getOutput()==ONE:

						if ((current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X)\
							or (current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==ONE)\
							or (current_node_inputs[0].getOutput()==ONE and current_node_inputs[1].getOutput()==X)):

							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ONE
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ONE

							if current_node_inputs[0].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[0].getNumber())

							if current_node_inputs[1].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[1].getNumber())

							tempOutputAssignments.append(tempNodeOutputs[0])


						else:
							tempOutputAssignments.append(tempNodeOutputs[0])
							break

					else:

						if (current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X):
							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ZERO
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=X

							tempNodeOutputs_copy1=deepcopy(tempNodeOutputs[0])
							tree_copy1=deepcopy(tree)

							list1=backTrace(tree_copy1,[tempNodeOutputs_copy1],no_inputs)


							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ONE
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ZERO

							tempNodeOutputs_copy1=deepcopy(tempNodeOutputs[0])
							tree_copy1=deepcopy(tree)

							list2=backTrace(tree_copy1,[tempNodeOutputs_copy1],no_inputs)

							if not (list1==-1):
								for entry in list1:
									if entry not in tempOutputAssignments: 
										tempOutputAssignments.append(entry)

							if not (list2==-1):
								for entry in list2:
									if entry not in tempOutputAssignments: 
										tempOutputAssignments.append(entry)

						elif(current_node_inputs[0].getOutput()==ONE and current_node_inputs[1].getOutput()==X):

							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ZERO
							backTraceList.append(current_node_inputs[1].getNumber())
							tempOutputAssignments.append(tempNodeOutputs[0])

						elif(current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==ONE):

							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ZERO
							backTraceList.append(current_node_inputs[0].getNumber())
							tempOutputAssignments.append(tempNodeOutputs[0])

						else:
							tempOutputAssignments.append(tempNodeOutputs[0])
							break

				
				del tempNodeOutputs[0]

		# 	print(tempOutputAssignments)
		# print(tempOutputAssignments)
		for entry in tempOutputAssignments:
			if entry not in outputAssignments:
				outputAssignments.append(entry)			

	if len(outputAssignments)==0:
		return -1
	else:
		return outputAssignments


def findTestVectors(NodeOutputs,no_inputs):
  	testVectors=[]
 	for entry in NodeOutputs:
 		tempTestVector=[]
 		for i in range(no_inputs):
 			tempTestVector.append(str(entry[i]))

 		if tempTestVector not in testVectors:
 			testVectors.append(tempTestVector)
 	return testVectors

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
		pathFinder(Fanout,Fanout[n][i],paths,p1)   							#next Fanout of current node
	p1.pop()																#pop last node
	return

def d_intersection(a,b):
	if (len(a)!=len(b)):
		return None
	else:
		new=[]
		for i in range(len(a)-1): 
			if a[i]==RothVariable('X','X'):
				p.append(b[i])
			elif b[i]==RothVariable('X','X'):
				p.append(a[i])
			else:
				return None
		return new	

Fanin=[None,None,None,None,["And",0,1],["And",2,3],["And",4,5],["And",6,5],["And",7,3]]
#Fanin=[None,None,None,["And",0,1],["And",2,3],["And",4,0],["And",5,2]]

#################some temp global variables#######################
paths = []																	#Final path
p1=[]																		#temp path		
NodeOutputs=[]	
no_inputs=3		
stuckAtFault=1
stuckAtNode=4
####################################################################


tree=CircuitTree()

tree.createTree(Fanin)
tree.createFanout(Fanin)


NodeOutputs=tree.propagate(stuckAtNode,stuckAtFault,Fanin)

print(NodeOutputs)

NodeOutputs=PrebackTrace(tree,NodeOutputs,stuckAtNode,stuckAtFault)

print("after pretraceback:",NodeOutputs)


finalAssignments=backTrace(tree,NodeOutputs,no_inputs)
print("after backtraceback:",finalAssignments)

testVectors=findTestVectors(finalAssignments,no_inputs)

for entry in testVectors:
	for output in entry:
		if output=='D' or output=="Dbar":
			testVectors.remove(entry)
			break
print("test vectors:", testVectors)

