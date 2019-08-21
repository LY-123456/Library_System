from datetime import *                                               #导入日期模块
__metaclass__ = type
class Book:
	'''一个书本信息类，包括书本名字，作者名字和书本简单信息'''
	def __init__(self, BookNo = "", BookName = "", Publisher = "", Year = "", Author = "", TotalNum = "", OnShelf = ""):
		self.BookNo = BookNo
		self.BookName = BookName                                      #书本名字
		self.Publisher = Publisher
		self.Year = Year
		self.Author = Author                                          #作者名字
		self.TotalNum = TotalNum
		self.OnShelf = OnShelf
		#self.content = content                                        #书本信息
		#self.add_date = date.today()                                  #书本添加日期

	def SetBookNo(self, no):
		self.BookNo = no

	def GetBookNo(self):
		return self.BookNo

	def SetBookName(self, name):
		self.BookName = name

	def GetBookName(self):
		return self.BookName

	def SetPublisher(self, publisher):
		self.Publisher = publisher

	def GetPublisher(self):
		return self.Publisher

	def SetYear(self, year):
		self.Year = year

	def GetYear(self):
		return self.Year

	def SetAuthor(self, author):
		self.Author = author

	def GetAuthor(self):
		return self.Author

	def SetTotalNum(self, totalnum):
		self.TotalNum = totalnum

	def GetTotalNum(self):
		return self.TotalNum

	def SetOnShelf(self, onshelf):
		self.OnShelf = onshelf

	def GetOnShelf(self):
		return self.OnShelf


	# def setContent(self, content):
	# 	self.content = content

	# def getContent(self):
	# 	return self.content

	# def getAddDate(self):
	# 	return self.add_date

#
# if __name__ == "__main__":
# 	mybook = Book()
# 	print(mybook.date)