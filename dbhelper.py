import pymysql
from book import *

__metaclass__ = type
class DBHelper:
	def getCon(self):
		'''获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名'''
		#为了能用中文，得加上编码方式
		conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "11111111", db = "library", charset = "utf8")
		return conn

	def insertBook(self, book):
		'''向数据库中book表插入书本信息，book为Book类对象，包含书本基本信息'''
		sql = "insert into book(bookNo, bookName, Publisher, Year, Author, TotalNum, OnShelf) \
		values(%s, %s, %s, %s, %s, %s, %s)" #id,书名，作者，出版社，出版日期，库存量，总量，
		conn = self.getCon();
		if conn == None:
			return
		cursor = conn.cursor()
		try:
			cursor.execute(sql, (book.GetBookNo(), book.GetBookName(), book.GetPublisher(), book.GetYear(), book.GetAuthor(), book.GetTotalNum(), book.GetOnShelf()))
		except:
			return -1
		conn.commit()
		cursor.close()
		conn.close()
		#new_id = cursor.lastrowid
		new_id = book.GetBookNo()
		print("新插入键值id为:", new_id)
		return new_id
	def getBorrowRecords(self, uid):
		sql = "select bookno from borrow where borrow.cardno=%s"
		sql2 = "select * from book where book.bookno=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql,(uid,))  # 执行并返回找到的行数
		# 获取查询结果
		rows = cursor.fetchall()
		list = []
		for item in rows:
			cursor.execute(sql2,(item[0],))
			bitem = cursor.fetchone()
			list.append(bitem)
			# bitem = (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
			# list.append(bitem)
		conn.commit()
		cursor.close()
		conn.close()
		return list
	def getAllBook(self):
		'''返回数据库中，book表中所有的书本信息'''
		sql = "select * from book"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		rownum = cursor.execute(sql)              #执行并返回找到的行数
		#获取查询结果
		rows = cursor.fetchall()
		list = []
		for item in rows:
			bitem = (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
			list.append(bitem)
		conn.commit()
		cursor.close()
		conn.close()
		return list

	def getBook(self, book):
		'''根据书本id值来寻找书本信息'''
		sql = "select * from book where "
		param = ()
		if book.GetBookNo() != "":
			sql = sql + "book.bookno=%s and "
			param+=(book.GetBookNo(),)
		if book.GetBookName() != "":
			sql = sql + "book.bookname=%s and "
			param += (book.GetBookName(),)
		if book.GetPublisher() != "":
			sql = sql + "book.publisher=%s and "
			param += (book.GetPublisher(),)
		if book.GetYear() != "":
			sql = sql + "book.year=%s and "
			param += (book.GetYear(),)
		if book.GetAuthor() != "":
			sql = sql + "book.author=%s and "
			param += (book.GetAuthor(),)
		if book.GetTotalNum() != "":
			sql = sql + "book.totalnum=%s and "
			param += (book.GetTotalNum(),)
		if book.GetOnShelf() != "":
			sql = sql + "book.onshelf=%s and "
			param += (book.GetOnShelf(),)
		sql = sql[:-4]#去掉最后一个and
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, param)                  #参数以元组形式给出
		rows = cursor.fetchall()
		list = []
		for item in rows:
			bitem = (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
			list.append(bitem)
		conn.commit()
		cursor.close()
		conn.close()
		return list #返回该书本信息

	def getBookById(self, bookid):
		'''根据书本id值来寻找书本信息'''
		sql = "select * from book  where book.bookno=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (bookid))                     #参数以元组形式给出
		row = cursor.fetchone()                             #取到第一个结果
		conn.commit()
		cursor.close()
		conn.close()
		return row                                          #返回该书本信息

	def getBookByName(self, bookname):
		'''根据书本id值来寻找书本信息'''
		sql = "select * from book  where book.bookname=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (bookname))                     #参数以元组形式给出
		# 获取查询结果
		rows = cursor.fetchall()
		list = []
		for item in rows:
			bitem = (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
			list.append(bitem)
		conn.commit()
		cursor.close()
		conn.close()
		return list                                       #返回该书本信息


	def saveUpdate(self, bookid, book):
		'''用book对象来修改id为bookid的书本信息'''
		sql = "update book set book.bookno=%s, book.bookname=%s, book.publisher=%s, book.year=%s, book.author=%s, book.totalnum=%s, book.onshelf=%s where book.bookno=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (book.GetBookNo(), book.GetBookName(), book.GetPublisher(), book.GetYear(), book.GetAuthor(), book.GetTotalNum(), book.GetOnShelf(), bookid))
		conn.commit()
		cursor.close()
		conn.close()

	def deleteBook(self, bookid):
		'''根据书本id来删除书籍'''
		sql1 = "select onshelf,totalnum from book where book.bookno = %s"
		sql2 = "delete from book where book.bookno = %s"

		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()

		cursor.execute(sql1,(bookid, ))
		row = cursor.fetchone()
		if row[0] != row[1]:
			return -1
		cursor.execute(sql2, (bookid, ))
		conn.commit()
		cursor.close()
		conn.close()

	def getUserById(self, userid):
		'''根据用户id得到用户信息'''
		sql = "select * from user  where user.cardno=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (userid))                     #参数以元组形式给出
		row = cursor.fetchone()                             #取到第一个结果
		conn.commit()
		cursor.close()
		conn.close()
		return row                                          #返回该用户信息

	def commitBorrow(self, borrow):
		'''完成借书操作'''
		if borrow.GetCardNo() == 'Null':
			return -1
		sql1 = "select onshelf from book where book.bookno=%s"
		sql2 = "select * from borrow where borrow.bookno = %s and borrow.cardno = %s"
		sql3 = "insert into borrow(cardno, bookno, lenddate) values(%s, %s, %s)"
		sql4 = "update book set book.onshelf=book.onshelf-1 where book.bookno=%s"
		conn = self.getCon();
		if conn == None:
			return
		cursor = conn.cursor()

		cursor.execute(sql1, (borrow.GetBookNo()))#检查在架数是否满足要求
		row = cursor.fetchone()
		if row[0] == 0:
			return -2
		ret = row[0]-1
		cursor.execute(sql2, (borrow.GetBookNo(),borrow.GetCardNo()))#检查是否已经借过该书
		row = cursor.fetchone()
		if row != None:
			return -3
		cursor.execute(sql3, (borrow.GetCardNo(), borrow.GetBookNo(), borrow.GetLendDate()))#添加借阅记录
		cursor.execute(sql4, (borrow.GetBookNo()))#更新在架数目

		conn.commit()
		cursor.close()
		conn.close()

		return ret

	def returnBook(self, borrow):
		'''完成还书操作'''
		if borrow.GetCardNo() == 'Null':
			return -1
		sql1 = "select * from borrow where borrow.bookno = %s and borrow.cardno = %s"
		sql2 = "delete from borrow where borrow.bookno = %s and borrow.cardno = %s"
		sql3 = "update book set book.onshelf=book.onshelf+1 where book.bookno=%s"
		sql4 = "select onshelf from book where book.bookno=%s"
		conn = self.getCon();
		if conn == None:
			return
		cursor = conn.cursor()

		cursor.execute(sql1, (borrow.GetBookNo(), borrow.GetCardNo()))#检查是否有该借书记录
		row = cursor.fetchone()
		if row == None:
			return -2
		cursor.execute(sql2, (borrow.GetBookNo(), borrow.GetCardNo()))#删除借阅记录
		cursor.execute(sql3, (borrow.GetBookNo()))#更新在架书目
		cursor.execute(sql4, (borrow.GetBookNo()))#得到当前在架数目
		row = cursor.fetchone()

		conn.commit()
		cursor.close()
		conn.close()

		return row[0]

if __name__ == '__main__':
	db = DBHelper()
	#book = Book(2, "西游记", "人民文学出版社",1977, "吴承恩", 10, 10)
	#db.insertBook(book)
	#list = db.getBookById(1)
	list = db.getAllBook()

	for item in list:
		print(item)

