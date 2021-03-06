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
		self._isInPath=False

	def setOutput(self,output):
		self._output=output

	def getNumber(self):
		return self._number

	def getOutput(self):
		return self._output

	def getInputs(self):
		if self._input2==None:
			return [self._input1]
		else:
			return [self._input1,self._input2]

	def getOperation(self):
		return self._operation

	def setInPath(self):
		self._isInPath=True
		return

	def isInPath(self):
		return self._isInPath

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
			#print i,Fanin[i]
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

		print("going in recursive propagate",tempNodeOutput_copy)

		paths=[]
		p1=[]
		pathFinder(self._Fanout,stuckAtNode,paths,p1)

		for path in paths:
			for node in path:
				self.getNode(node).setInPath()

		return self.recursive_propagate(stuckAtNode,Fanin,tempNodeOutput_copy)


	def recursive_propagate(self,current_node,Fanin,tempNodeOutput):

		paths=[]
		p1=[]
		pathFinder(self._Fanout,current_node,paths,p1)
		# print(current_node)
		# print(tempNodeOutput)

		vectors=[]
		for path in paths:

			# print "current path", path, tempNodeOutput

			if len(self._Fanout[path[0]])==0:
				return [tempNodeOutput]

			else:
				fanin_next_node=Fanin[path[1]]

				if fanin_next_node[0]=="Not":
					tempNodeOutput[path[1]]= ~tempNodeOutput[fanin_next_node[1]]
					vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput)
					if not (vector==-1 or len(vector)==0):
						for entry in vector:
							#print("appending vector:",entry)
							vectors.append(entry)

					

				if fanin_next_node[0]=="And" or fanin_next_node[0]=="Nand":
					if fanin_next_node[1]==path[0]:

						if tempNodeOutput[fanin_next_node[2]]== X:	

							#print("going for two choices")
							##################recursion for 1st decision########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[2]]=ONE	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

							if fanin_next_node[0]=="Nand":
								tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							#print("choice 1 ans:",vector)
							if not (vector==-1 or len(vector)==0):

								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)

							
							if self.getNode(fanin_next_node[2]).isInPath():
								#################recursion for second decision##########################
								tempNodeOutput_copy=deepcopy(tempNodeOutput)
								tempNodeOutput_copy[fanin_next_node[2]]=tempNodeOutput[fanin_next_node[1]]	

								tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

								if fanin_next_node[0]=="Nand":
									tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

								vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

								#print("choice 2 ans:",vector)

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
					##########################################if required input is fanin_next_node[2]########################

					else:

						if tempNodeOutput[fanin_next_node[1]]== X:	

							#print("going for two choices")
							##################recursion for 1st decision########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[1]]=ONE	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[2]] 

							if fanin_next_node[0]=="Nand":
								tempNodeOutput_copy[path[1]]= ~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							#print("choice 1 ans:",vector)
							if not (vector==-1 or len(vector)==0):

								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)

							
							if self.getNode(fanin_next_node[1]).isInPath():
								#################recursion for second decision##########################
								tempNodeOutput_copy=deepcopy(tempNodeOutput)
								tempNodeOutput_copy[fanin_next_node[1]]=tempNodeOutput[fanin_next_node[2]]	

								tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[2]] 

								if fanin_next_node[0]=="Nand":
									tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

								vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

								#print("choice 2 ans:",vector)

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


			#################################### OR NOR #################################################
				if fanin_next_node[0]=="Or" or fanin_next_node[0]=="Nor":
					if fanin_next_node[1]==path[0]:

						if tempNodeOutput[fanin_next_node[2]]== X:	

							#print("going for two choices")
							##################recursion for 1st decision########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[2]]=ZERO	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

							if fanin_next_node[0]=="Nor":
								tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							#print("choice 1 ans:",vector)
							if not (vector==-1 or len(vector)==0):

								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)

							
							if self.getNode(fanin_next_node[2]).isInPath():
								#################recursion for second decision##########################
								tempNodeOutput_copy=deepcopy(tempNodeOutput)
								tempNodeOutput_copy[fanin_next_node[2]]=tempNodeOutput[fanin_next_node[1]]	

								tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[1]] 

								if fanin_next_node[0]=="Nor":
									tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

								vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

								#print("choice 2 ans:",vector)

								if not (vector==-1 or len(vector)==0 ):
									for entry in vector:
										#print("appending vector:",entry)
										vectors.append(entry)
									

						###################################################################
	

						else:

							tempNodeOutput[path[1]]= tempNodeOutput[fanin_next_node[1]] | tempNodeOutput[fanin_next_node[2]]

							if fanin_next_node[0]=="Nor":
								tempNodeOutput[path[1]]=~tempNodeOutput[path[1]]


							if not (tempNodeOutput[path[1]]==D or tempNodeOutput[path[1]]==DBAR):
								return -1

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput)
							if not (vector==-1 or len(vector)==0):
								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)
					##########################################if required input is fanin_next_node[2]########################

					else:

						if tempNodeOutput[fanin_next_node[1]]== X:	

							#print("going for two choices")
							##################recursion for 1st decision########################
							tempNodeOutput_copy=deepcopy(tempNodeOutput)
							tempNodeOutput_copy[fanin_next_node[1]]=ZERO	

							tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[2]] 

							if fanin_next_node[0]=="Nor":
								tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

							vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

							#print("choice 1 ans:",vector)
							if not (vector==-1 or len(vector)==0):

								for entry in vector:
									#print("appending vector:",entry)
									vectors.append(entry)

							
							if self.getNode(fanin_next_node[1]).isInPath():
								#################recursion for second decision##########################
								tempNodeOutput_copy=deepcopy(tempNodeOutput)
								tempNodeOutput_copy[fanin_next_node[1]]=tempNodeOutput[fanin_next_node[2]]	

								tempNodeOutput_copy[path[1]]= tempNodeOutput[fanin_next_node[2]] 

								if fanin_next_node[0]=="Nand":
									tempNodeOutput_copy[path[1]]=~tempNodeOutput_copy[path[1]]

								vector=self.recursive_propagate(path[1],Fanin,tempNodeOutput_copy)

								#print("choice 2 ans:",vector)

								if not (vector==-1 or len(vector)==0 ):
									for entry in vector:
										#print("appending vector:",entry)
										vectors.append(entry)
								

						###################################################################
	

						else:

							tempNodeOutput[path[1]]= tempNodeOutput[fanin_next_node[1]] | tempNodeOutput[fanin_next_node[2]]

							if fanin_next_node[0]=="Nor":
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

	if operation==None:
		#print "\n","yo",NodeOutputs
		return NodeOutputs
	if len(NodeOutputs)==-1:
		print "No Test Case found"
		return 

	if stuckAtFault==0:

		if operation=="Not":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ZERO
			inputs_desired_outputs=[tempNodeOutput]

		if operation=="And":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ONE
			tempNodeOutput[faultNode_inputs[1].getNumber()]=ONE
			inputs_desired_outputs=[tempNodeOutput]

		elif operation=="Nand":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ZERO
			tempNodeOutput[faultNode_inputs[1].getNumber()]=X

			tempNodeOutput1=[X for i in range(len(tree._nodes))]
			tempNodeOutput1[faultNode_inputs[0].getNumber()]=X
			tempNodeOutput1[faultNode_inputs[1].getNumber()]=ZERO

			inputs_desired_outputs=[tempNodeOutput,tempNodeOutput1]

		elif operation=="Or":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ONE
			tempNodeOutput[faultNode_inputs[1].getNumber()]=X

			tempNodeOutput1=[X for i in range(len(tree._nodes))]
			tempNodeOutput1[faultNode_inputs[0].getNumber()]=X
			tempNodeOutput1[faultNode_inputs[1].getNumber()]=ONE

			inputs_desired_outputs=[tempNodeOutput,tempNodeOutput1]

		elif operation=="Nor":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ZERO
			tempNodeOutput[faultNode_inputs[1].getNumber()]=ZERO
			inputs_desired_outputs=[tempNodeOutput]


	else:
		if operation=="Not":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ONE
			inputs_desired_outputs=[tempNodeOutput]

		if operation=="And":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ZERO
			tempNodeOutput[faultNode_inputs[1].getNumber()]=X

			tempNodeOutput1=[X for i in range(len(tree._nodes))]
			tempNodeOutput1[faultNode_inputs[0].getNumber()]=X
			tempNodeOutput1[faultNode_inputs[1].getNumber()]=ZERO

			inputs_desired_outputs=[tempNodeOutput,tempNodeOutput1]


		elif operation=="Nand":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ONE
			tempNodeOutput[faultNode_inputs[1].getNumber()]=ONE
			inputs_desired_outputs=[tempNodeOutput]

		elif operation=="Or":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ZERO
			tempNodeOutput[faultNode_inputs[1].getNumber()]=ZERO
			inputs_desired_outputs=[tempNodeOutput]

		elif operation=="Nor":
			tempNodeOutput=[X for i in range(len(tree._nodes))]
			tempNodeOutput[faultNode_inputs[0].getNumber()]=ONE
			tempNodeOutput[faultNode_inputs[1].getNumber()]=X

			tempNodeOutput1=[X for i in range(len(tree._nodes))]
			tempNodeOutput1[faultNode_inputs[0].getNumber()]=X
			tempNodeOutput1[faultNode_inputs[1].getNumber()]=ONE

			inputs_desired_outputs=[tempNodeOutput,tempNodeOutput1]


	for entry in NodeOutputs:

		for outputs in inputs_desired_outputs:
			tempNodeOutput=entry
			tempNodeOutput=d_intersection(entry,outputs)

			# print "here",tempNodeOutput
			if tempNodeOutput!=None:				
				if tempNodeOutput not in vectors:
					vectors.append(tempNodeOutput)

	return vectors


def backTrace(tree,NodeOutputs,no_inputs):

	outputAssignments=[]

	for i in range(len(NodeOutputs)):

		#print i,NodeOutputs[i]

		tempNodeOutputs=NodeOutputs[i]
		tempOutputAssignments=[]
		tree.setOutputs(tempNodeOutputs)

		backTraceList=[j for j in range(no_inputs,len(tempNodeOutputs)) if tempNodeOutputs[j]==ONE or tempNodeOutputs[j]==ZERO]

		
		#print "backlist",backTraceList
		tempNodeOutputs=[tempNodeOutputs]

		while not(len(tempNodeOutputs)==0)  :

			
			while not(len(backTraceList)==0):

				tree.setOutputs(tempNodeOutputs[0])

				current_node=tree.getNode(backTraceList[0])

				del backTraceList[0]

				current_node_inputs=current_node.getInputs()
				if current_node.getOperation()=="Not":
					if current_node_inputs[0].getOutput()==X:

						if current_node.getOutput()==ONE:
							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ZERO
							if current_node_inputs[0].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[0].getNumber())
							tempOutputAssignments.append(tempNodeOutputs[0])

						else:
							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ONE
							if current_node_inputs[0].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[0].getNumber())
							tempOutputAssignments.append(tempNodeOutputs[0])
					else:
						break

				if current_node.getOperation()=="And" or current_node.getOperation()=="Nand":


					#print current_node, current_node.getOutput()
					if current_node.getOperation()=="And":
						current_node_psuedo_output= current_node.getOutput()
					else:
						current_node_psuedo_output= ~current_node.getOutput()

					if current_node_psuedo_output==ONE :

						if ((current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X)\
							or (current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==ONE)\
							or (current_node_inputs[0].getOutput()==ONE and current_node_inputs[1].getOutput()==X)):

							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ONE
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ONE

							if current_node_inputs[0].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[0].getNumber())

							if current_node_inputs[1].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[1].getNumber())

							#print " and backtrace", tempNodeOutputs[0] , backTraceList
							tempOutputAssignments.append(tempNodeOutputs[0])


						else:
							#tempOutputAssignments.append(tempNodeOutputs[0])
							break

					else:

						if (current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X):
							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ZERO
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=X

							tempNodeOutputs_copy1=deepcopy(tempNodeOutputs[0])
							tree_copy1=deepcopy(tree)

							list1=backTrace(tree_copy1,[tempNodeOutputs_copy1],no_inputs)


							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=X
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

						elif current_node_inputs[1].getOutput()==X:

							if current_node_inputs[0].getOutput()==ONE:

								tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ZERO
								backTraceList.append(current_node_inputs[1].getNumber())
								tempOutputAssignments.append(tempNodeOutputs[0])
							else:
								tempOutputAssignments.append(tempNodeOutputs[0])


						elif(current_node_inputs[0].getOutput()==X ):

							if current_node_inputs[1].getOutput()==ONE:
								tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ZERO
								backTraceList.append(current_node_inputs[0].getNumber())
								tempOutputAssignments.append(tempNodeOutputs[0])
							else:
								tempOutputAssignments.append(tempNodeOutputs[0])


						else:
							#tempOutputAssignments.append(tempNodeOutputs[0])
							break

		#################################backtrace for OR NOR#############################################

				if current_node.getOperation()=="Or" or current_node.getOperation()=="Nor":


					if current_node.getOperation()=="Or":
						current_node_psuedo_output= current_node.getOutput()
					else:
						current_node_psuedo_output= ~current_node.getOutput()


					if current_node_psuedo_output==ZERO:

						if ((current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X)\
							or (current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==ZERO)\
							or (current_node_inputs[0].getOutput()==ZERO and current_node_inputs[1].getOutput()==X)):

							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ZERO
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ZERO

							if current_node_inputs[0].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[0].getNumber())

							if current_node_inputs[1].getNumber() not in backTraceList:
								backTraceList.append(current_node_inputs[1].getNumber())

							tempOutputAssignments.append(tempNodeOutputs[0])


						else:
							#tempOutputAssignments.append(tempNodeOutputs[0])
							break

					else:

						if (current_node_inputs[0].getOutput()==X and current_node_inputs[1].getOutput()==X):
							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ONE
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=X

							tempNodeOutputs_copy1=deepcopy(tempNodeOutputs[0])
							tree_copy1=deepcopy(tree)

							list1=backTrace(tree_copy1,[tempNodeOutputs_copy1],no_inputs)


							tempNodeOutputs[0][current_node_inputs[0].getNumber()]=X
							tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ONE

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

						elif current_node_inputs[1].getOutput()==X:

							if current_node_inputs[0].getOutput()==ZERO:

								tempNodeOutputs[0][current_node_inputs[1].getNumber()]=ONE
								backTraceList.append(current_node_inputs[1].getNumber())
								tempOutputAssignments.append(tempNodeOutputs[0])
							else:
								tempOutputAssignments.append(tempNodeOutputs[0])


						elif(current_node_inputs[0].getOutput()==X ):

							if current_node_inputs[1].getOutput()==ZERO:
								tempNodeOutputs[0][current_node_inputs[0].getNumber()]=ONE
								backTraceList.append(current_node_inputs[0].getNumber())
								tempOutputAssignments.append(tempNodeOutputs[0])
							else:
								tempOutputAssignments.append(tempNodeOutputs[0])


						else:
							#tempOutputAssignments.append(tempNodeOutputs[0])
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
  	if NodeOutputs==-1:
  		print "No Test Case Found"
  		return
 	for entry in NodeOutputs:
 		tempTestVector=[]
 		for i in range(no_inputs):
 			tempTestVector.append(str(entry[i]))
 			#print tempTestVector

 		if tempTestVector not in testVectors:
 			testVectors.append(tempTestVector)
 			# print "yo",testVectors
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
		intersected_output=[]

		for i in range(len(a)):
			if a[i]==b[i]:
				intersected_output.append(b[i])
			elif a[i]==X:
				intersected_output.append(b[i])
			elif b[i]==X:
				intersected_output.append(a[i])
			else:
				return None
		return intersected_output

Fanin=[None,None,None,["Or",0,1],["Nand",3,1],["And",4,2],["Nor",0,5],["Nand",6,2],["And",7,5],["Not",6],["Not",9]]


#################some temp global variables#######################
paths = []																	#Final path
p1=[]																		#temp path
NodeOutputs=[]
no_inputs=3
stuckAtFault=0
stuckAtNode=6
####################################################################


tree=CircuitTree()

tree.createTree(Fanin)
tree.createFanout(Fanin)

print "printing Circuit tree",tree
NodeOutputs=tree.propagate(stuckAtNode,stuckAtFault,Fanin)

#print(NodeOutputs)

NodeOutputs=PrebackTrace(tree,NodeOutputs,stuckAtNode,stuckAtFault)

#print("after pretraceback:",NodeOutputs)


finalAssignments=backTrace(tree,NodeOutputs,no_inputs)
print("after backtraceback:",finalAssignments)

testVectors=findTestVectors(finalAssignments,no_inputs)

if testVectors!=None:
	if tree.getNode(stuckAtNode).getOperation()!=None:
		for entry in testVectors:
			for output in entry:
				if output=="D" or output=="Dbar":
					testVectors.remove(entry)
					break
	else:
		for entry in testVectors:
			for i in range(len(entry)):
				if i!=stuckAtNode:
					if entry[i]=="D" or entry[i]=="Dbar":
						testVectors.remove(entry)
						break
	print("test vectors:", testVectors)
else:
	print "No Test Case Found"