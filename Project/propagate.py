from pyeda.inter import*
from RothAlgebra import RothVariable
from copy import deepcopy

#Or(Xor(And(Not(Or(Or(And(a, b), c), d)), d), c), And(b, d))

AND=[[(0,'X'),(1,0)],[(1,1)]]
NAND=[[(1,1)],[(0,'X'),(1,0)]]
OR=[[(1,'X'),(0,1)],[(0,0)]]
NOR=[[(0,0)],[(1,'X'),(0,1)]]

Fanin=[None,None,None,None,[Or,0,1],[And,4,2],[Not,5],[Or,6,3]]

Fanout=[[] for i in range(len(Fanin))]
NodeOutput=[]


for i in range(len(Fanin)):							#i is index of node for which Fanout is to be found
	for j in range(len(Fanin)):						#j itertaes over all elements of Fanin to find i in its input
		if Fanin[j]!=None:							#jth node has no Fanin	
			for find in range(1,len(Fanin[j])):
				if i==Fanin[j][find]:				#if ith node found in Fanin of j
					Fanout[i].append(j)
					break

#print(Fanout)

paths = []																	#Final path
p1=[]																		#temp path
def pathFinder(Fanout,n):
	# global path
	# global p1
	p1.append(n)   															#append current node
	if(Fanout[n]== []):
		p2=p1[:]															#shallow copy
		paths.append(p2) 													#append current list to all paths
		p1.pop()															#pop last node
		return 
	for i in range(len(Fanout[n])):
		pathFinder(Fanout,Fanout[n][i])   									#next Fanout of current node
	p1.pop()																#pop last node
	return


pathFinder(Fanout,5)

paths=[]
p1=[]

def propagate(Fanout,stuckAtNode,stuckAtFault):


	pathFinder(Fanout,stuckAtNode)

	print (paths)

	for path in paths:
		tempNodeOutput=[RothVariable('X','X') for i in range(len(Fanin))]
		if stuckAtFault==0:
			tempNodeOutput[stuckAtNode]=RothVariable(1,0)
			
		else:
			tempNodeOutput[stuckAtNode]=RothVariable(0,1)

		
		print(tempNodeOutput)
		for i in range(len(path)):

			
			if path[i]==stuckAtNode:
				pass
			else:
				fanin_current_node=Fanin[path[i]]



				#############if operation is and or nand######################

				if fanin_current_node[0]==And or fanin_current_node[0]==Nand:
					if fanin_current_node[1]==path[i-1]:

						if tempNodeOutput[fanin_current_node[2]]== RothVariable('X','X'):	## should add equality operator overload in class

							tempNodeOutput[fanin_current_node[2]]=RothVariable(1,1)	

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] 

							if fanin_current_node[0]==Nand:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]
							print (path[i],tempNodeOutput[path[i]])

						else:

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] & tempNodeOutput[fanin_current_node[2]]

							if fanin_current_node[0]==Nand:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

							print (path[i],tempNodeOutput[path[i]])

							if not (tempNodeOutput[path[i]]==RothVariable(1,0) or tempNodeOutput[path[i]]==RothVariable(0,1)):
								break

					else:

						if tempNodeOutput[fanin_current_node[1]]== RothVariable('X','X'):	## should add equality operator overload in class

							tempNodeOutput[fanin_current_node[1]]=RothVariable(1,1)	

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[2]] 

							if fanin_current_node[0]==Nand:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]
							print (path[i],tempNodeOutput[path[i]])

						else:

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] | tempNodeOutput[fanin_current_node[2]]

							if fanin_current_node[0]==Nand:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

							print (path[i],tempNodeOutput[path[i]])

							if not (tempNodeOutput[path[i]]==RothVariable(1,0) or tempNodeOutput[path[i]]==RothVariable(0,1)):
								break


				############################# if operation is Or or NOR####################################
				elif fanin_current_node[0]==Or or fanin_current_node[0]==Nor:
					if fanin_current_node[1]==path[i-1]:

						if tempNodeOutput[fanin_current_node[2]]== RothVariable('X','X'):	## should add equality operator overload in class

							tempNodeOutput[fanin_current_node[2]]=RothVariable(0,0)	

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] 

							if fanin_current_node[0]==Nor:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

							print (path[i],tempNodeOutput[path[i]])


						else:

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] & tempNodeOutput[fanin_current_node[2]]

							if fanin_current_node[0]==Nand:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

							print (path[i],tempNodeOutput[path[i]])

							if not (tempNodeOutput[path[i]]==RothVariable(1,0) or tempNodeOutput[path[i]]==RothVariable(0,1)):
								break

					else:

						if tempNodeOutput[fanin_current_node[1]]== RothVariable('X','X'):	## should add equality operator overload in class

							tempNodeOutput[fanin_current_node[1]]=RothVariable(0,0)	

							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[2]] 

							if fanin_current_node[0]==Nor:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

							print (path[i],tempNodeOutput[path[i]])



						else:


							tempNodeOutput[path[i]]= tempNodeOutput[fanin_current_node[1]] | tempNodeOutput[fanin_current_node[2]]

							if fanin_current_node[0]==Nor:
								tempNodeOutput[path[i]]=~tempNodeOutput[path[i]]

							print (path[i],tempNodeOutput[path[i]])

							if not (tempNodeOutput[path[i]]==RothVariable(1,0) or tempNodeOutput[path[i]]==RothVariable(0,1)):
								break

				elif fanin_current_node[0]==Not:
					tempNodeOutput[path[i]]=~tempNodeOutput[path[i-1]]


		print(tempNodeOutput)						

	NodeOutput.append(tempNodeOutput)

finnalOutput=[]
def backtrace(Fanin,NodeOutput):



	backtraceList=[]

	for i in range(len(NodeOutput)):
		if NodeOutput[len(NodeOutput)-i]==RothVariable(1,1):
			backtraceList.append([len(NodeOutput)-i,1])
		if NodeOutput[len(NodeOutput)-i]==RothVariable(0,0):
			backtraceList.append([len(NodeOutput)-i,0])
			

	while not(len(backtraceList==0)):

		fanin_current_back_node=Fanin[backtraceList[0][0]]
		if(fanin_current_back_node[0]== And):
			if(NodeOutput[fanin_current_back_node[1]==RothAlgebra('X','X')]):
				if not(NodeOutput[fanin_current_back_node[2]]==RothAlgebra('X','X')\
					or 
				if(backtraceList[0][1]==1):
					NodeOutput[fanin_current_node]




propagate(Fanout,4,0)
print(NodeOutput)









