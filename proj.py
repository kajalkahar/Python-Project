from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
from matplotlib import pyplot as plt
from PIL import ImageTk, Image
import bs4
import os
import socket
import requests




root = Tk()
root.title("Quote of the day")
root.geometry("1000x800+350+50")


#for image
res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup = bs4.BeautifulSoup(res.text,'lxml')
data = soup.find('img',{"class":"p-qotd"})
quote = data['alt']
img="https://www.brainyquote.com" + data['data-img-url']
ir = requests.get(img)
with open("pic.png ", 'wb') as f:
	f.write(ir.content)




#for city
try:
	socket.create_connection(("www.google.com",80))
	res=requests.get("http://api.ipstack.com/103.44.117.139?access_key=499e162a680025a05a0ecaf5b4ac556b&format=1")
	data=res.json()
	city = data['city']
except OSError:
	print("check network")




#for temp
try: 
	socket.create_connection(("www.google.com",80))
	a1="https://api.openweathermap.org/data/2.5/weather?"
	a2="&q="+city +"&units=metric"
	a3="&appid=73f49da0a76543c54f7c6e80901f01da"        
	api_address=a1+a2+a3        
	res1=requests.get(api_address)        
	wdata=requests.get(api_address).json()        
	temp = wdata['main']['temp']
except OSError:        
	print("check network")



img = ImageTk.PhotoImage(file="pic.png")
pic = Label(root, image = img)
pic.pack(side = "top",fill="both", expand = "no")


lblCity = Label(root , text ="City : "+str(city),font=300,padx=25,pady=25)
lblTemp = Label(root , text ="Temp : "+str(temp)+'\u00b0',font=300,padx=25,pady=25)

lblCity.pack()
lblTemp.pack()

root.after(5000, root.destroy)
root.mainloop()




















root = Tk()
root.title("STUDENT MANAGEMENT SYSTEM ")
root.geometry("400x400+200+200")

#add open
def f1():
	adSt.deiconify()
	root.withdraw()




#view open and load data
def f3():
	viSt.deiconify()
	root.withdraw()
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg = ''
		for d in data:
			msg = msg + "RNO " + str(d[0]) + " NAME " + str(d[1]) + " MARKS " + str(d[2]) + "\n"
		stData.configure(state='normal')
		stData.delete( '0.0' , END)	
		stData.insert(INSERT, msg)
		stData.configure(state='disabled')
	except cx_Oracle.DatabaseError as e:
		print("select issue ", e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

#update open
def f6():
	upSt.deiconify()
	root.withdraw()

#delete open
def f9():
	deSt.deiconify()
	root.withdraw()

#graph
def f12():
	
	con = None 	
	cursor = None
	try:
		stu_name=[]
		stu_marks=[]
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql = "select * from student "
		cursor.execute(sql)
		data = cursor.fetchall()
		for column in data:
			stu_name.append(column[1])
			stu_marks.append(column[2])
	
		plt.bar(stu_name, stu_marks, color='red', edgecolor='black')
		plt.title("Student's Scores")
		plt.xlabel("Names", fontsize=10)
		plt.ylabel("Marks", fontsize=10)
		plt.grid()
		plt.show()


	except cx_Oracle.DatabaseError as e:
		print("Select Issue ", e)
		
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()



btnAdd = Button(root, text="ADD ", font=("arial",16,'bold'),width=10, command=f1)
btnView = Button(root, text="VIEW ", font=("arial",16,'bold'),width=10, command=f3)
btnUpdate = Button(root, text="UPDATE ", font=("arial",16,'bold'),width=10, command=f6)
btnDelete = Button(root, text="DELETE ", font=("arial",16,'bold'),width=10, command=f9)
btnGraph = Button(root, text="GRAPH ", font=("arial",16,'bold'),width=10, command=f12)

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnGraph.pack(pady=10)

#ADD--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
adSt = Toplevel(root)
adSt.title("ADD STUDENT ")
adSt.geometry("400x400+200+200")
adSt.withdraw()

def f2():
	root.deiconify()
	adSt.withdraw()



def f5():
	con=None
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = int(entAddRno.get())
		name = entAddName.get()
		marks = int(entAddMarks.get())
		if(rno>0 and name.isalpha() and marks<=100 and marks>=0):
			cursor = con.cursor()
			sql = "insert into student values('%d' , '%s' , '%d')"
			args = (rno,name,marks)
			cursor.execute(sql % args)
			con.commit()
			msg = str(cursor.rowcount) + "rows inserted"
			messagebox.showinfo("Success ",msg)
			entAddRno.delete(0,END)
			entAddRno.focus()
			entAddName.delete(0,END)
			entAddMarks.delete(0,END)
			
		else:
			if rno<=0:
				messagebox.showerror("Error","RNO MUST BE GREATER THAN 0")
				entAddRno.delete(0,END)
				entAddRno.focus()
				entAddName.delete(0,END)
				entAddMarks.delete(0,END)
			if(not(name.isalpha())):
				messagebox.showerror("Error" ,"NAME MUST BE CHARACTERS ONLY")
				entAddRno.delete(0,END)
				entAddRno.focus()
				entAddName.delete(0,END)
				entAddMarks.delete(0,END)

			if(marks>100 or marks <0):
				messagebox.showerror("Error","MARKS MUST BE GREATER THAN OR EQUAL TO 0 AND LESS THAN OR EQUAL TO 100")
				entAddRno.delete(0,END)
				entAddRno.focus()
				entAddName.delete(0,END)
				entAddMarks.delete(0,END)
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure " , "insert issues:" + str( e))
		entAddRno.delete(0,END)
		entAddRno.focus()
		entAddName.delete(0,END)
		entAddMarks.delete(0,END)
		con.rollback()
	except ValueError as e:
		messagebox.showerror("Failure " , e )
		entAddRno.delete(0,END)
		entAddRno.focus()
		entAddName.delete(0,END)
		entAddMarks.delete(0,END)
		con.rollback()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()


lblAddRno = Label(adSt, text="ENTER RNO ")
lblAddName = Label(adSt, text="ENTER NAME ")
lblAddMarks = Label(adSt, text="ENTER MARKS ")
entAddRno = Entry(adSt, bd=5)
entAddName = Entry(adSt, bd=5)
entAddMarks = Entry(adSt, bd=5)
btnAddSave = Button(adSt, text="SAVE ", command=f5)
btnAddBack = Button(adSt, text="BACK ", command=f2)
entAddRno.focus()

lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddMarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

#view---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->
def f4():
	root.deiconify()
	viSt.withdraw()
	

viSt = Toplevel(root)
viSt.title("VIEW STUDENT ")
viSt.geometry("400x400+200+200")
viSt.withdraw()

stData = scrolledtext.ScrolledText(viSt, width=30 , height=5)
btnViewBack = Button(viSt, text="BACK ", command=f4)


stData.pack(pady=10)
btnViewBack.pack(pady=10)

#for update-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
upSt = Toplevel(root)
upSt.title("UPDATE STUDENT ")
upSt.geometry("400x400+200+200")
upSt.withdraw()

def f7():
	con=None
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = int(entUpdateRno.get())
		name = entUpdateName.get()
		marks = int(entUpdateMarks.get())
		if(rno>0  and name.isalpha() and marks<=100 and marks >=0):
			cursor = con.cursor()
			sql = "update  student set marks = '%d', name='%s' where rno = '%d' "
			args = (marks,name,rno)
			cursor.execute(sql % args)
			con.commit()
			if(cursor.rowcount>0):
				msg = str(cursor.rowcount) + "rows updated"
				messagebox.showinfo("Success " , msg )
				entUpdateRno.delete(0,END)
				entUpdateRno.focus()
				entUpdateName.delete(0,END)
				entUpdateMarks.delete(0,END)
			else:

				messagebox.showwarning("Failure ","THER IS NO SUCH RECORD ")
				entUpdateRno.delete(0,END)
				entUpdateRno.focus()
				entUpdateName.delete(0,END)	
				entUpdateMarks.delete(0,END)
		elif rno<=0:
			messagebox.showerror("Error","RNO MUST BE GREATER THAN 0")
			entUpdateRno.delete(0,END)
			entUpdateRno.focus()
			entUpdateName.delete(0,END)
			entUpdateMarks.delete(0,END)
		elif (marks>100 or marks <0):
			messagebox.showerror("Error","MARKS MUST BE GREATER THAN OR EQUAL TO 0 AND LESS THAN OR EQUAL TO 100")
			entUpdateRno.delete(0,END)
			entUpdateRno.focus()
			entUpdateName.delete(0,END)
			entUpdateMarks.delete(0,END)
		elif (not(name.isalpha())):
			messagebox.showerror("Error","NAME MUST BE CHARACTERS ONLY")
			entUpdateRno.delete(0,END)
			entUpdateRno.focus()
			entUpdateName.delete(0,END)
			entUpdateMarks.delete(0,END)
	
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure " , "insert issues" + str( e))
		entUpdateRno.delete(0,END)
		entUpdateRno.focus()
		entUpdateName.delete(0,END)
		entUpdateMarks.delete(0,END)
		con.rollback()
	except ValueError as e:
		messagebox.showerror("Failure" , e )
		entUpdateRno.delete(0,END)
		entUpdateRno.focus()
		entUpdateName.delete(0,END)
		entUpdateMarks.delete(0,END)
		con.rollback()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
def f8():
	root.deiconify()
	upSt.withdraw()


lblUpdateRno = Label(upSt , text = "ENTER RNO ",width=15)
entUpdateRno = Entry(upSt , bd=5,width=15)
entUpdateRno.focus()
lblUpdateName = Label(upSt ,text = "ENTER NAME ",width=15)
entUpdateName = Entry(upSt , bd=5,width=15)
lblUpdateMarks = Label(upSt , text = "ENTER MARKS ",width=15)
entUpdateMarks = Entry(upSt , bd=5,width=15)
btnUpdateSave = Button(upSt , text = "Save",width=15, command=f7)
btnUpdateBack = Button(upSt , text = "Back",width=15,command=f8)



lblUpdateRno.pack(pady=10)
entUpdateRno.pack(pady=10)
lblUpdateName.pack(pady=10)
entUpdateName.pack(pady=10)
lblUpdateMarks.pack(pady=10)
entUpdateMarks.pack(pady=10)
btnUpdateSave.pack(pady=10)
btnUpdateBack.pack(pady=10)

#delete-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
deSt = Toplevel(root)
deSt.title("DELETE ENTRY ")
deSt.geometry("400x400+200+200")
deSt.withdraw()

def f10():
	con=None
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = int(entDeleteRno.get())	
				
		if(rno>0 ):
			cursor = con.cursor()
			sql = "delete from  student  where rno = '%d' "
			args = (rno)
			cursor.execute(sql%args)
			con.commit()
			if(cursor.rowcount>0):
				msg = str(cursor.rowcount) + "rows deleted"
				messagebox.showinfo("Success " , msg )
				entDeleteRno.delete(0,END)
				entDeleteRno.focus()
			else:

				messagebox.showwarning("Failure ","There is no such record ")
				entDeleteRno.delete(0,END)
				entDeleteRno.focus()
		
		else:
			if rno<=0:
				messagebox.showerror("Error","rno must be greater than 0")	
				entDeleteRno.delete(0,END)
				entDeleteRno.focus()	
		
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure " , "insert issues" + str( e))
		entDeleteRno.delete(0,END)
		entDeleteRno.focus()
		con.rollback()
	except ValueError as v:
		messagebox.showerror("Failure " , "rno must be integer" )
		entDeleteRno.delete(0,END)
		entDeleteRno.focus()
		con.rollback()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

def f11():
	deSt.withdraw()
	root.deiconify()


lblDeleteRno = Label(deSt , text = "ENTER RNO ",width=15)
entDeleteRno = Entry(deSt , bd=5, width=15)

btnDeleteSave = Button(deSt , text = "SAVE ",width=15 ,command=f10)
btnDeleteBack = Button(deSt , text = "BACK ",width=15 ,command=f11)

lblDeleteRno.pack(pady=10)
entDeleteRno.pack(pady=10)
btnDeleteSave.pack(pady=10)
btnDeleteBack.pack(pady=10)




#graph-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
grSt = Toplevel(root)
grSt.title("STUDENTS GRAPH ")
grSt.geometry("400x400+200+200")
grSt.withdraw()



root.mainloop()


























