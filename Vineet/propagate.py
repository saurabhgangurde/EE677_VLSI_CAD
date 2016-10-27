def propagate(Fanout,stuckAtNode,stuckAtFault):


	pathFinder(Fanout,stuckAtNode)

	print (paths)

	for path in paths:
		tempNodeOutput=[RothVariable('X','X') for i in range(len(Fanin))]
		if stuckAtFault==0:
			tempNodeOutput[stuckAtNode]=RothVariable(1,0)
			
		else:
			tempNodeOutput[stuckAtNode]=RothVariable(0,1)

		
		displayRothVariableList(tempNodeOutput)
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


		displayRothVariableList(tempNodeOutput)						

	NodeOutput.append(tempNodeOutput)