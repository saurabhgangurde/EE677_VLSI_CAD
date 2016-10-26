from pyeda.inter import*
from RothAlgebra import RothVariable


#Or(Xor(And(Not(Or(Or(And(a, b), c), d)), d), c), And(b, d))


class node:
	def __init__(self,number,operation,input1,input2):

		self.number=number
		self.op=operation
		self.input1=input1
		self.input2=input2
		self.output=RothVariable('X','X')


Fanin=[None,None,None,None,[And,0,1],[Or,4,2],[Or,5,3],[Not,6],[And,7,3],[And,8,2],[And,1,3],[Or,9,10]]

Fanout=[[] for i in range(len(Fanin))]

for i in range(len(Fanin)):							#i is index of node for which Fanout is to be found
	for j in range(len(Fanin)):						#j itertaes over all elements of Fanin to find i in its input
		if Fanin[j]!=None:							#jth node has no Fanin	
			for find in range(1,len(Fanin[j])):
				if i==Fanin[j][find]:				#if ith node found in Fanin of j
					Fanout[i].append(j)
					break


def propagation(Fanin,stuckAtNode,stuckAtFault,path):


#Assume we are checking for node 5 s-a-0
# CorrectValue=[RothVariable('X','x') 'X' for i in range(len(Fanin))]
# CorrectValue[5]=RothVariable() 
# FaultyValue=[] 

# c=Fanin[6][0](Fanin[6][1],Fanin[6],[2])
# print (c)
# print (Fanout)
