#coding:utf-8
'''一个图书管理系统，能够实现增加书籍，删除书籍，
修改书籍和查看图书详情，基于mysql数据库和
wxPython'''
import os
import wx
from book import *
from borrow import *
#from user import *
from dbhelper import *

__metaclass__ = type


class LoginFrame(wx.Frame):
	'''添加登陆界面'''
	def __init__(self, call):

		#self.mainframe = parent
		#wx.Frame.__init__(self, parent, title = title, size = (300,300))
		wx.Frame.__init__(self, None, -1, '登陆页面')
		self.panel = wx.Panel(self, pos = (0,0), size = (300,300))
		self.panel.SetBackgroundColour("#FFFFF0")

		userID_tip = wx.StaticText(self.panel, label="Enter ID:", pos=(15, 18), size=(35, 25))
		userID_tip.SetBackgroundColour("#FFFFFF")
		userID_text = wx.TextCtrl(self.panel, pos=(100, 15), size=(200, 25))
		self.userid = userID_text

		login_button = wx.Button(self.panel, label="登陆", pos=(160, 120))
		login_button.SetBackgroundColour("#000000")
		#save_button.SetForegroundColour("#FF000")
		self.Bind(wx.EVT_BUTTON, self.login, login_button)

		self.call = call

		# 需要用到的数据库接口
		self.dbhelper = DBHelper()

	def login(self, evt):
		userID = self.userid.GetValue()
		cur_user = self.dbhelper.getUserById(userID)
		if cur_user == None:
			warn = wx.MessageDialog(self, message="没有该用户", caption="错误警告",style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		self.call(cur_user)  # 传递值
		self.Destroy()


class AddFrame(wx.Frame):
	'''添加书籍弹出的小窗口'''

	def __init__(self, parent, title):
		'''初始化该小窗口的布局'''

		self.mainframe = parent
		#生成一个450*350的框
		wx.Frame.__init__(self, parent, title = title, size = (450, 350))

		self.panel = wx.Panel(self, pos = (0, 0), size = (450, 350))
		self.panel.SetBackgroundColour("#FFFFF0")                              #背景为白色

		#7个编辑框，分别用来编辑书名，作者，书籍相关信息
		bookNo_tip = wx.StaticText(self.panel, label="序列号:", pos=(5, 8), size=(35, 25))
		bookNo_tip.SetBackgroundColour("#FFFFFF")
		bookNo_text = wx.TextCtrl(self.panel, pos=(60, 5), size=(340, 25))
		self.bookno = bookNo_text

		bookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 38), size = (35, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel, pos = (60, 35), size = (340, 25))
		self.bookname = bookName_text

		publisher_tip = wx.StaticText(self.panel, label = "出版社:", pos = (5, 68), size = (35, 25))
		publisher_tip.SetBackgroundColour("#FFFFFF")
		publisher_text = wx.TextCtrl(self.panel, pos = (60, 65), size = (340, 25))
		self.publisher = publisher_text

		year_tip = wx.StaticText(self.panel, label = "出版日期:", pos = (5, 98), size = (35, 25))
		year_tip.SetBackgroundColour("#FFFFFF")
		year_text = wx.TextCtrl(self.panel, pos = (60, 95), size = (340, 25))
		self.year = year_text

		author_tip = wx.StaticText(self.panel, label = "作者:", pos = (5, 128), size = (35, 25))
		author_tip.SetBackgroundColour("#FFFFFF")
		author_text = wx.TextCtrl(self.panel, pos = (60, 125), size = (340, 25))
		self.author = author_text

		totalnum_tip = wx.StaticText(self.panel, label = "总数:", pos = (5, 158), size = (35, 25))
		totalnum_tip.SetBackgroundColour("#FFFFFF")
		totalnum_text = wx.TextCtrl(self.panel, pos = (60, 155), size = (340, 25))
		self.totalnum = totalnum_text

		onshelf_tip = wx.StaticText(self.panel, label = "在架:", pos = (5, 188), size = (35, 25))
		onshelf_tip.SetBackgroundColour("#FFFFFF")
		onshelf_text = wx.TextCtrl(self.panel, pos = (60, 185), size = (340, 25))
		self.onshelf = onshelf_text


		#保存按钮
		single_add_button = wx.Button(self.panel, label = "保存", pos = (160, 220))
		single_add_button.SetBackgroundColour("#000000")
		self.Bind(wx.EVT_BUTTON, self.singleAdd, single_add_button)

		batch_add_button = wx.Button(self.panel, label = "批量添加", pos = (160, 260))
		batch_add_button.SetBackgroundColour("#000000")
		self.Bind(wx.EVT_BUTTON, self.batchAdd, batch_add_button)

		#需要用到的数据库接口
		self.dbhelper = DBHelper()


	def singleAdd(self, evt):
		'''第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中'''
		BookNo = self.bookno.GetValue()
		BookName = self.bookname.GetValue()
		Publisher = self.publisher.GetValue()
		Year = self.year.GetValue()
		Author = self.author.GetValue()
		TotalNum = self.totalnum.GetValue()
		OnShelf = self.onshelf.GetValue()

		if BookNo == "" or BookName == "" or Publisher == "" or Year == "" or Author == "" or TotalNum == "" or OnShelf == "":
			warn = wx.MessageDialog(self, message = "所有信息不能为空！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			print("开始插入到数据库中")
			book = Book(BookNo, BookName, Publisher, Year, Author, TotalNum, OnShelf)
			ret = self.dbhelper.insertBook(book)  #连接数据库
			if ret == -1:
				warn = wx.MessageDialog(self, message="书号重复", caption="错误警告",
										style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			#self.mainframe.addToList(book_id, 3)
			index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(BookNo))
			self.mainframe.list.SetItem(index, 1, str(BookName))  # 更新主界面信息
			self.mainframe.list.SetItem(index, 2, str(Publisher))
			self.mainframe.list.SetItem(index, 3, str(Year))
			self.mainframe.list.SetItem(index, 4, str(Author))
			self.mainframe.list.SetItem(index, 5, str(TotalNum))
			self.mainframe.list.SetItem(index, 6, str(OnShelf))
		self.Destroy()

	def batchAdd(self, event):
		filesFilter = "Dicom (*.dcm)|*.dcm|" "All files (*.*)|*.*"
		fileDialog = wx.FileDialog(self, message="选择单个文件", wildcard=filesFilter, style=wx.FD_OPEN)
		dialogResult = fileDialog.ShowModal()
		if dialogResult != wx.ID_OK:
			return
		path = fileDialog.GetPath()
		with open(path, 'r') as f:
			for line in f:
				ss=line.split(',')
				book = Book(ss[0],ss[1],ss[2],ss[3],ss[4],ss[5],ss[6])
				ret = self.dbhelper.insertBook(book)
				if ret == -1:
					# warn = wx.MessageDialog(self, message="批量导入失败", caption="错误警告",
					# 						style=wx.YES_DEFAULT | wx.ICON_ERROR)
					# warn.ShowModal()  # 提示错误
					# warn.Destroy()
					continue
				index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(ss[0]))
				self.mainframe.list.SetItem(index, 1, str(ss[1]))  # 更新主界面信息
				self.mainframe.list.SetItem(index, 2, str(ss[2]))
				self.mainframe.list.SetItem(index, 3, str(ss[3]))
				self.mainframe.list.SetItem(index, 4, str(ss[4]))
				self.mainframe.list.SetItem(index, 5, str(ss[5]))
				self.mainframe.list.SetItem(index, 6, str(ss[6]))
				print("新导入:",ss)
		self.Destroy()

class UpdateFrame(wx.Frame):
	def __init__(self, parent, title, select_id):
		'''初始化更新图书信息界面总布局'''

		wx.Frame(parent, title = title, size = (400, 250))

		#用来调用父frame,便于更新
		self.mainframe = parent
		#生成一个300*300的框
		wx.Frame.__init__(self, parent, title = title, size = (400, 300))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 250))
		self.panel.SetBackgroundColour("#FFFFF0")                              #背景为白色

		#三个编辑框，分别用来编辑书名，作者，书籍相关信息
		bookNo_tip = wx.StaticText(self.panel, label="序列号:", pos=(5, 8), size=(35, 25))
		bookNo_tip.SetBackgroundColour("#FFFFFF")
		bookNo_text = wx.TextCtrl(self.panel, pos=(60, 5), size=(340, 25))
		bookNo_text.SetEditable(False)   #序列号一旦确定，不可更改
		self.bookno = bookNo_text

		bookName_tip = wx.StaticText(self.panel, label="书名:", pos=(5, 38), size=(35, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel, pos=(60, 35), size=(340, 25))
		self.bookname = bookName_text

		publisher_tip = wx.StaticText(self.panel, label="出版社:", pos=(5, 68), size=(35, 25))
		publisher_tip.SetBackgroundColour("#FFFFFF")
		publisher_text = wx.TextCtrl(self.panel, pos=(60, 65), size=(340, 25))
		self.publisher = publisher_text

		year_tip = wx.StaticText(self.panel, label="出版日期:", pos=(5, 98), size=(35, 25))
		year_tip.SetBackgroundColour("#FFFFFF")
		year_text = wx.TextCtrl(self.panel, pos=(60, 95), size=(340, 25))
		self.year = year_text

		author_tip = wx.StaticText(self.panel, label="作者:", pos=(5, 128), size=(35, 25))
		author_tip.SetBackgroundColour("#FFFFFF")
		author_text = wx.TextCtrl(self.panel, pos=(60, 125), size=(340, 25))
		self.author = author_text

		totalnum_tip = wx.StaticText(self.panel, label="总数:", pos=(5, 158), size=(35, 25))
		totalnum_tip.SetBackgroundColour("#FFFFFF")
		totalnum_text = wx.TextCtrl(self.panel, pos=(60, 155), size=(340, 25))
		self.totalnum = totalnum_text

		onshelf_tip = wx.StaticText(self.panel, label="在架:", pos=(5, 188), size=(35, 25))
		onshelf_tip.SetBackgroundColour("#FFFFFF")
		onshelf_text = wx.TextCtrl(self.panel, pos=(60, 185), size=(340, 25))
		self.onshelf = onshelf_text


		#设置保存按键
		save_button = wx.Button(self.panel, label="保存修改", pos=(160, 250))
		save_button.SetBackgroundColour("#FFFFF0")
		self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)

		#选中的id和bookid
		self.select_id = select_id
		self.bookid = self.mainframe.list.GetItem(select_id, 0).Text             #获取第select_id行的第0列的值

		#需要用到的数据库接口
		self.dbhelper = DBHelper()
		self.showAllText()                     #展现所有的text原来取值


	def showAllText(self):
		'''显示概述本原始信息'''
		data = self.dbhelper.getBookById(self.bookid)                      #通过id获取书本信息
		self.bookno.SetValue(str(data[0]))                                        #设置值
		self.bookname.SetValue(data[1])
		self.publisher.SetValue(data[2])
		self.year.SetValue(str(data[3]))
		self.author.SetValue(data[4])
		self.totalnum.SetValue(str(data[5]))
		self.onshelf.SetValue(str(data[6]))


	def saveUpdate(self, evt):
		'''保存修改后的值'''
		BookNo = self.bookno.GetValue()                                    #获得修改后的值
		BookName = self.bookname.GetValue()
		Publisher = self.publisher.GetValue()
		Year = self.year.GetValue()
		Author = self.author.GetValue()
		TotalNum = self.totalnum.GetValue()
		OnShelf = self.onshelf.GetValue()

		print("书名:"+BookName)
		if BookNo == "" or BookName == "" or Publisher == "" or Year == "" or Author == "" or TotalNum == "" or OnShelf == "":
			print("进来了")
			warn = wx.MessageDialog(self, message = "所有信息不能为空！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			print("开始将修改后的数据保存到数据库中")
			book = Book(BookNo, BookName, Publisher, Year, Author, TotalNum, OnShelf)      #将数据封装到book对象中
			self.dbhelper.saveUpdate(self.bookid, book)
			self.mainframe.list.SetItem(self.select_id, 1, BookName) #更新主界面信息
			self.mainframe.list.SetItem(self.select_id, 2, Publisher)
			self.mainframe.list.SetItem(self.select_id, 3, Year)
			self.mainframe.list.SetItem(self.select_id, 4, Author)
			self.mainframe.list.SetItem(self.select_id, 5, TotalNum)
			self.mainframe.list.SetItem(self.select_id, 6, OnShelf)

		self.Destroy()                                                     #修改完后自动销毁

class QueryFrame(wx.Frame):
	'''用来显示书籍的信息'''

	def __init__(self, parent, title):
		'''初始化该小窗口的布局'''

		#便于调用父窗口
		self.mainframe = parent

		#生成一个400*300的框
		wx.Frame.__init__(self, parent, title = title, size = (400, 300))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 250))
		self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

		bookNo_tip = wx.StaticText(self.panel, label="序列号:", pos=(5, 8), size=(35, 25))
		bookNo_tip.SetBackgroundColour("#FFFFFF")
		bookNo_text = wx.TextCtrl(self.panel, pos=(60, 5), size=(340, 25))
		#bookNo_text.SetEditable(False)
		self.bookno = bookNo_text

		bookName_tip = wx.StaticText(self.panel, label="书名:", pos=(5, 38), size=(35, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel, pos=(60, 35), size=(340, 25))
		#bookName_text.SetEditable(False)
		self.bookname = bookName_text

		publisher_tip = wx.StaticText(self.panel, label="出版社:", pos=(5, 68), size=(35, 25))
		publisher_tip.SetBackgroundColour("#FFFFFF")
		publisher_text = wx.TextCtrl(self.panel, pos=(60, 65), size=(340, 25))
		#publisher_text.SetEditable(False)
		self.publisher = publisher_text

		year_tip = wx.StaticText(self.panel, label="出版日期:", pos=(5, 98), size=(35, 25))
		year_tip.SetBackgroundColour("#FFFFFF")
		year_text = wx.TextCtrl(self.panel, pos=(60, 95), size=(340, 25))
		#year_text.SetEditable(False)
		self.year = year_text

		author_tip = wx.StaticText(self.panel, label="作者:", pos=(5, 128), size=(35, 25))
		author_tip.SetBackgroundColour("#FFFFFF")
		author_text = wx.TextCtrl(self.panel, pos=(60, 125), size=(340, 25))
		#author_text.SetEditable(False)
		self.author = author_text

		totalnum_tip = wx.StaticText(self.panel, label="总数:", pos=(5, 158), size=(35, 25))
		totalnum_tip.SetBackgroundColour("#FFFFFF")
		totalnum_text = wx.TextCtrl(self.panel, pos=(60, 155), size=(340, 25))
		#totalnum_text.SetEditable(False)
		self.totalnum = totalnum_text

		onshelf_tip = wx.StaticText(self.panel, label="在架:", pos=(5, 188), size=(35, 25))
		onshelf_tip.SetBackgroundColour("#FFFFFF")
		onshelf_text = wx.TextCtrl(self.panel, pos=(60, 185), size=(340, 25))
		#onshelf_text.SetEditable(False)
		self.onshelf = onshelf_text

		query_button = wx.Button(self.panel, label="搜索", pos=(160, 220))
		query_button.SetBackgroundColour("#000000")
		self.Bind(wx.EVT_BUTTON, self.doQuery, query_button)
		#需要用到的数据库接口
		self.dbhelper = DBHelper()


	def doQuery(self, evt):
		'''保存修改后的值'''
		BookNo = self.bookno.GetValue()                                    #获得修改后的值
		BookName = self.bookname.GetValue()
		Publisher = self.publisher.GetValue()
		Year = self.year.GetValue()
		Author = self.author.GetValue()
		TotalNum = self.totalnum.GetValue()
		OnShelf = self.onshelf.GetValue()

		book = Book(BookNo, BookName, Publisher, Year, Author, TotalNum, OnShelf)      #将数据封装到book对象中
		ret = self.dbhelper.getBook(book)

		if len(ret) == 0:
			warn = wx.MessageDialog(self, message="没有符合条件的项", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			show_f = ShowFrame(self, "查询结果",ret)
			show_f.Show(True)

class UserFrame(wx.Frame):
	def __init__(self, parent, title):
		self.mainframe = parent
		wx.Frame.__init__(self, parent, title=title, size=(644, 200))
		# 定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		# 生成一个列表
		self.list = wx.ListCtrl(self, -1, size=(644, 200),
								style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)  # | wx.LC_SINGLE_SEL


class ShowFrame(wx.Frame):
	def __init__(self, parent, title, message):
		self.mainframe = parent
		wx.Frame.__init__(self, parent, title = title, size = (644,200))
		# 定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		# 生成一个列表
		self.list = wx.ListCtrl(self, -1, size=(644, 200),
								style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)  # | wx.LC_SINGLE_SEL

		# 列表有散列，分别是书本ID,书名，添加日期
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")
		self.list.InsertColumn(2, "出版社")
		self.list.InsertColumn(3, "出版日期")
		self.list.InsertColumn(4, "作者")
		self.list.InsertColumn(5, "总数")
		self.list.InsertColumn(6, "在架数")
		# 设置各列的宽度
		self.list.SetColumnWidth(0, 92)  # 设置每一列的宽度
		self.list.SetColumnWidth(1, 92)
		self.list.SetColumnWidth(2, 92)
		self.list.SetColumnWidth(3, 92)
		self.list.SetColumnWidth(4, 92)
		self.list.SetColumnWidth(5, 92)
		self.list.SetColumnWidth(6, 92)
		self.main_layout.Add(self.list, 7)
		self.SetSizer(self.main_layout)
		for data in message:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, str(data[1]))
			self.list.SetItem(index, 2, str(data[2]))
			self.list.SetItem(index, 3, str(data[3]))
			self.list.SetItem(index, 4, str(data[4]))
			self.list.SetItem(index, 5, str(data[5]))
			self.list.SetItem(index, 6, str(data[6]))



class LibraryFrame(wx.Frame):
	def __init__(self, parent, title):
		'''初始化系统总体布局，包括各种控件'''


		#初始化当前用户
		self.cur_user=('Null', 'Null', 0)

		#生成一个宽为644，高为600的frame框
		wx.Frame.__init__(self, parent, title=title, size=(644, 600))

		#定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		#生成一个列表
		self.list = wx.ListCtrl(self, -1, size = (644,400), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES) #| wx.LC_SINGLE_SEL

		#列表有散列，分别是书本ID,书名，添加日期
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")
		self.list.InsertColumn(2, "出版社")
		self.list.InsertColumn(3, "出版日期")
		self.list.InsertColumn(4, "作者")
		self.list.InsertColumn(5, "总数")
		self.list.InsertColumn(6, "在架数")
		#设置各列的宽度
		self.list.SetColumnWidth(0, 92)                                         #设置每一列的宽度
		self.list.SetColumnWidth(1, 92)
		self.list.SetColumnWidth(2, 92)
		self.list.SetColumnWidth(3, 92)
		self.list.SetColumnWidth(4, 92)
		self.list.SetColumnWidth(5, 92)
		self.list.SetColumnWidth(6, 92)


		# 添加一组按钮，实现增删改查,用一个panel来管理该组按钮的布局
		self.panel = wx.Panel(self, pos=(0, 400), size=(644, 100))
		#显示当前用户信息
		userid_tip = wx.StaticText(self.panel, label="用户ID:", pos=(20, 15), size=(35, 25))
		#userid_tip.SetBackgroundColour("#FFFFFF")
		userid_text = wx.TextCtrl(self.panel, pos=(70, 13), size=(60, 25))
		userid_text.SetEditable(False)
		self.uid = userid_text

		username_tip = wx.StaticText(self.panel, label="用户姓名:", pos=(140, 15), size=(35, 25))
		# username_tip.SetBackgroundColour("#FFFFFF")
		username_text = wx.TextCtrl(self.panel, pos=(220, 13), size=(60, 25))
		username_text.SetEditable(False)
		self.uname = username_text

		userpriority_tip = wx.StaticText(self.panel, label="用户权限:", pos=(300, 15), size=(35, 25))
		# userpriority_tip.SetBackgroundColour("#FFFFFF")
		userpriority_text = wx.TextCtrl(self.panel, pos=(380, 13), size=(60, 25))
		userpriority_text.SetEditable(False)
		self.upriority = userpriority_text

		self.uid.SetValue(str(self.cur_user[0]))
		self.uname.SetValue(str(self.cur_user[1]))
		self.upriority.SetValue(str(self.cur_user[2]))

		#定义一组按钮
		login_button = wx.Button(self.panel, label = "登陆", pos = (470, 10), size = (60, 30))
		info_button = wx.Button(self.panel, label="我的借阅", pos=(550, 10), size=(60, 30))

		add_button = wx.Button(self.panel, label = "添加", pos = (20, 45), size = (60, 30))    #, size = (75, 30)
		del_button = wx.Button(self.panel, label = "删除", pos = (130, 45), size = (60, 30))    #, size = (75, 30)
		update_button = wx.Button(self.panel, label = "修改", pos = (240, 45), size = (60, 30)) #, size = (75, 30)
		query_button = wx.Button(self.panel, label = "查询", pos = (350, 45), size = (60, 30))  #, size = (75, 30)
		borrow_button = wx.Button(self.panel, label = "借阅", pos = (460,45), size = (60,30))
		return_button = wx.Button(self.panel, label = "归还", pos = (570,45), size = (60,30))

		login_button.SetBackgroundColour("#000000")
		info_button.SetBackgroundColour("#000000")
		add_button.SetBackgroundColour("#000000")
		del_button.SetBackgroundColour("#000000")
		update_button.SetBackgroundColour("#000000")
		query_button.SetBackgroundColour("#000000")
		borrow_button.SetBackgroundColour("#000000")
		return_button.SetBackgroundColour("#000000")

		#w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
		self.Bind(wx.EVT_BUTTON, self.login, login_button)
		self.Bind(wx.EVT_BUTTON, self.usrinfo, info_button)
		self.Bind(wx.EVT_BUTTON, self.addBook, add_button)
		self.Bind(wx.EVT_BUTTON, self.delBook, del_button)
		self.Bind(wx.EVT_BUTTON, self.updateBook, update_button)
		self.Bind(wx.EVT_BUTTON, self.queryBook, query_button)
		self.Bind(wx.EVT_BUTTON, self.borrowBook, borrow_button)
		self.Bind(wx.EVT_BUTTON, self.returnBook, return_button)
		#将列表和panel添加到主面板
		self.main_layout.Add(self.list, 7)
		self.main_layout.Add(self.panel, 1)

		self.SetSizer(self.main_layout)

		#添加数据库操作对象
		self.dbhelper = DBHelper()
		datas = self.dbhelper.getAllBook()

		for data in datas:
			#print(self.list.GetItemCount())
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, str(data[1]))
			self.list.SetItem(index, 2, str(data[2]))
			self.list.SetItem(index, 3, str(data[3]))
			self.list.SetItem(index, 4, str(data[4]))
			self.list.SetItem(index, 5, str(data[5]))
			self.list.SetItem(index, 6, str(data[6]))
		
	def login(self, evt):
		log_f = LoginFrame(self.CallBack)
		log_f.Show(True)

	def CallBack(self, value):
		self.cur_user = value
		self.uid.SetValue(str(self.cur_user[0]))
		self.uname.SetValue(str(self.cur_user[1]))
		self.upriority.SetValue(str(self.cur_user[2]))

	def addBook(self, evt):
		'''添加书籍按钮，弹出添加书籍框'''
		if self.cur_user[2]== False:
			warn = wx.MessageDialog(self, message="权限不够", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		add_f = AddFrame(self, "添加书籍窗口")
		add_f.Show(True)


	def usrinfo(self, evt):
		if self.cur_user[0]=="Null":
			warn = wx.MessageDialog(self, message="请先登录", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		lended = self.dbhelper.getBorrowRecords(self.uid.GetValue())
		#print("a",lended)
		info_f = ShowFrame(self, "我的借阅", lended)
		info_f.Show(True)

	def delBook(self, evt):
		'''删除书籍按钮，先选中,然后删除'''
		if self.cur_user[2]== False:
			warn = wx.MessageDialog(self, message="权限不够", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何条目！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			bookid = self.list.GetItem(selectId, 0).Text       #得到书本id
			#self.list.DeleteItem(selectId)                     #先在listctrl中删除选中行
			ret = self.dbhelper.deleteBook(bookid)
			if ret == -1:
				warn = wx.MessageDialog(self, message="还有未归还书目，不可删除", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			else:
				self.list.DeleteItem(selectId)  # 先在listctrl中删除选中行
				warn = wx.MessageDialog(self, message="删除成功", caption="成功", style=wx.YES_DEFAULT )
				warn.ShowModal()
				warn.Destroy()
				return

	def updateBook(self, evt):
		'''修改按钮响应事件，点击修改按钮，弹出修改框'''
		if self.cur_user[2] == False:
			warn = wx.MessageDialog(self, message="权限不够", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何条目！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			update_f = UpdateFrame(self, "修改书籍窗口", selectId)
			update_f.Show(True)


	def queryBook(self, evt):
		'''查看按钮响应事件'''
		query_f = QueryFrame(self, "查询书籍窗口")
		query_f.Show(True)

	def borrowBook(self, evt):
		'''借阅按钮响应事件'''
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			bookid = self.list.GetItem(selectId, 0).Text  # 得到书本id
			borrow = Borrow(cardNo=self.cur_user[0], bookNo=bookid)
			ret = self.dbhelper.commitBorrow(borrow)
			if ret == -1:
				warn = wx.MessageDialog(self, message="请先登录", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			elif ret == -2:
				warn = wx.MessageDialog(self, message="当前书目不可借", caption="错误警告",
										style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			elif ret == -3:
				warn = wx.MessageDialog(self, message="您已借过此书", caption="错误警告",
										style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			else:
				self.list.SetItem(selectId, 6, str(ret))
				warn = wx.MessageDialog(self, message="借阅成功", caption="成功", style=wx.YES_DEFAULT )
				warn.ShowModal()
				warn.Destroy()
				return


	def returnBook(self, evt):
		'''还书按钮响应事件'''
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何条目！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			bookid = self.list.GetItem(selectId, 0).Text
			borrow = Borrow(cardNo=self.cur_user[0], bookNo=bookid)
			ret = self.dbhelper.returnBook(borrow)
			if ret == -1:
				warn = wx.MessageDialog(self, message="请先登录", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			elif ret == -2:
				warn = wx.MessageDialog(self, message="没有对应的借书记录", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
			else:
				self.list.SetItem(selectId, 6, str(ret))
				warn = wx.MessageDialog(self, message="归还成功", caption="成功", style=wx.YES_DEFAULT )
				warn.ShowModal()
				warn.Destroy()
				return



	# def addToList(self, id, book):
	# 	index = self.list.InsertItem(self.list.GetItemCount(), str(id))
	# 	self.list.SetItem(index, 1, book.getBookName())
	# 	self.list.SetItem(index, 2, str(book.getAddDate()))



AppBaseClass = wx.App

class LibraryApp(AppBaseClass):
	def OnInit(self):
		frame = LibraryFrame(None, "library-system")
		frame.Show()

		return True


#类似于c中的main函数，但被其他模块导入时，__name__值不是"__main__"
if __name__ == "__main__":
	app = LibraryApp()
	app.MainLoop()

