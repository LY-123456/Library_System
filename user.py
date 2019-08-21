__metaclass__ = type
class User:
	'''borrow类，记录书本与用户借阅关系'''
	def __init__(self, cardNo = "", Name = "", IsAdmin = False):
		self.cardNo = cardNo
		self.Name = Name
		#self.Department = Department
		self.IsAdmin = IsAdmin

	def SetUserNo(self, no):
		self.cardNoNo = no

	def GetUserNo(self):
		return self.cardNoNo

	def SetUserName(self, name):
		self.Name = name

	def GetUserName(self):
		return self.Name

	# def SetUserDepartment(self, department):
	# 	self.Department = department
	#
	# def GetUserDepartment(self):
	# 	return self.Department

#
# if __name__ == "__main__":
# 	print("borrow")