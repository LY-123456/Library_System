__metaclass__ = type
class Borrow:
	'''borrow类，记录书本与用户借阅关系'''
	def __init__(self, borrowId = "", cardNo = "", bookNo = "", lendDate = ""):
		self.borrowId = borrowId
		self.cardNo = cardNo
		self.bookNo = bookNo
		self.lendDate = lendDate
		#self.returnDate = returnDate


	def SetBorrowId(self, id):
		self.borrowId = id

	def GetBorrowId(self):
		return self.borrowId

	def SetCardNo(self, no):
		self.cardNo = no

	def GetCardNo(self):
		return self.cardNo

	def SetBookNo(self, no):
		self.bookNo = no

	def GetBookNo(self):
		return self.bookNo

	def SetLendDate(self, lenddate):
		self.lendDate = lenddate

	def GetLendDate(self):
		return self.lendDate

	# def SetReturnDate(self, returndate):
	# 	self.returnDate = returndate
	#
	# def GetReturnDate(self):
	# 	return self.returnDate


#
# if __name__ == "__main__":
# 	myborrow = Borrow()
# 	print("borrow")