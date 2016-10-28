
class RothVariable(object):
	def __init__(self,correct,faulty,name=None):
		#name will be one of the entry in set{'0','1','D','Dbar','X'}
		#D corresponds to (1/0)

		self.correct=correct
		self.faulty=faulty

		if correct==0 and faulty==0:
			self.name='0'
		elif correct==1 and faulty==1:
			self.name='1'
		elif correct==1 and faulty==0:
			self.name='D'
		elif correct==0 and faulty==1:
			self.name='Dbar'
		else:
			self.name='X'

	def __and__(self,b):

		if(self.name=='X' or b.name=='X'):
			raise "error cannot do operations with X " 
		else:
			return RothVariable((self.correct & b.correct),(self.faulty & b.faulty) )

	def __invert__(self):

		if(self.name=='X'):
			raise "error cannot do operations with X " 
		else:
			return RothVariable(int(not self.correct),int(not self.faulty) )

	def __or__(self,b):

		if(self.name=='X' or b.name=='X'):
			raise "error cannot do operations with X " 
		else:
			return RothVariable((self.correct | b.correct),(self.faulty | b.faulty) )

	def __xor__(self,b):

		if(self.name=='X' or b.name=='X'):
			raise "error cannot do operations with X " 
		else:
			return RothVariable((self.correct ^ b.correct),(self.faulty ^ b.faulty) )
	def __or__(self,b):

		if(self.name=='X' or b.name=='X'):
			raise "error cannot do operations with X " 
		else:
			return RothVariable((self.correct | b.correct),(self.faulty | b.faulty) )

	def __eq__(self,b):
		if self.name==b.name:
			return True
		else:
			return False

	def __repr__(self):
		if self.name==None:
			return "None"
		else:
			return self.name



# a=[]
# d=RothVariable(1,0,'D')
# b=~d
# a=[b,d]

#print(b)
# d=RothVariable('X','X','D')

# print(b)
# print(b==d)
# #print d & b

# c=a & b & d
# print c
