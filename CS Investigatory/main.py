import mysql.connector as mysql
from cryptography.fernet import Fernet
import csv
from tabulate import tabulate

filerand=open("pwd.csv", "a+")
filerand.close()

def mysqlcom(user1,pwd1):
	con=mysql.connect(host="localhost",user=user1,passwd=pwd1)
	if con.is_connected():
   		print("Connection Established")
   		return "w"
	else:
	   print("Connection Errors! Kindly check!!!")
	   return "l"

def enc(k, char):
	cipher_suite = Fernet(k)
	encoded_text = cipher_suite.encrypt(char.encode())
	return encoded_text

def dec(k, char):
	cipher_suite = Fernet(k)
	decoded_text = cipher_suite.decrypt(char)
	decoded_text_updated = decoded_text.decode()
	return decoded_text_updated

def stripp(texa):
	texb=texa[2:-1]
	texc=texb.encode()
	return texc


def login():
	a=True
	while a==True:
		a1=input("Please enter your MySQL username(default=root): ")
		a2=input("Password(default=root): ")
		for lki in [a1,a2]:
			if lki=='':
				lki='root'
		x= mysqlcom(a1,a2)
		if (x=="w"):
			break
		else:
			print("Your Username or Password is incorrect.")

	b=True
	z=0
	while b==True:
		pass
		n= input("Enter your new username: ")
		fields = []
		rows = []
		with open("pwd.csv","r+") as f1:
			z=0
			csvreader = csv.reader(f1)
			for row in csvreader:
				rows.append(row)
			for i in rows:
				for j in i:
					if j!=i[0]:
						j1=stripp(j)
						ap=dec(stripp(i[0]),stripp(j))
						if (ap==n):
							z=1
			if z==1:
				print("Username already exists")
				continue
			p= input("Enter your new password: ")
			p1=input("Enter your new password: ")
			if p==p1:
				b=False
			else:
				print("Passwords don't match, Please try again")


	with open("pwd.csv", 'a+') as csvfile:
		csvw=csv.writer(csvfile,delimiter=',')
		r1=[]
		cred=[n,p,a1,a2]
		key = Fernet.generate_key()
		r1.append(key)
		for o in cred:
			f56=enc(key,o)
			r1.append(f56)
		csvw.writerow(r1)

	print("Welcome",n)
	mnsc(n)

def logon():
	ag=True
	while ag==True:
		usr=input("Enter your username: ")
		fields = []
		rows = []
		f1= open("pwd.csv","r")
		z=0
		k=0
		csvreader = csv.reader(f1)
		for row in csvreader:
			rows.append(row)
		for i in rows:
			for j in i:
				if j!=i[0]:
					j1=stripp(j)
					ap=dec(stripp(i[0]),stripp(j))
					ap1=dec(stripp(i[0]),stripp(i[2]))
					if (ap==usr):
						pwd=input("Enter your password: ")
						if(pwd==ap1):
							print("Welcome Back", usr)
							z=1
							mnsc(usr)
						else:
							print("Wrong Password.")
							k+=1
							if k==3:
								print("Maximum attemps reached. Going back.\n")
								screen1()
					else:
						continue
		if z==0 and k==0:
			print("There is no user called",usr,".Please Try again.\n")
			screen1()
		f1.close()

def screen1():
	print("Good morning")
	a=input("First time?(y/N)[Enter 0 to quit]:")
	if(a.lower() in 'nopenadanot '):
		logon()
	elif (a.lower() in "yesyep"):
		login()
	elif (a=='0'):
		quit()
	else:
		print("Please choose a valid option.\n")
		screen1()

def mnsc(userr):
	rows=[]
	f1= open("pwd.csv","r")
	csvreader = csv.reader(f1)
	for row in csvreader:
		rows.append(row)
	for i in rows:
		#print(dec(stripp(i[0]),stripp(i[1])))
		if userr==dec(stripp(i[0]),stripp(i[1])):
			usr=dec(stripp(i[0]),stripp(i[1]))
			pwd=dec(stripp(i[0]),stripp(i[2]))
			sqlusr=dec(stripp(i[0]),stripp(i[3]))
			sqlpwd=dec(stripp(i[0]),stripp(i[4]))
	mydb=mysql.connect(host='localhost',user=sqlusr,passwd=sqlpwd)
	cursor=mydb.cursor()
	cursor.execute("show databases;")
	z1=0
	for x in cursor:
		#tables.append(x)
		if "loans" in x:
			z1+=1
			#print("hi")
	if (z1==0):
		cursor.execute("create database loans;")
		mydb.commit()
	tables=[]

	cursor.execute("use loans;")
	cursor.execute("show tables;")
	if cursor.fetchall()==[]:
		x=str("create table "+userr+" (sno int,loanname varchar(50), loantype varchar(20),loanamt float, loandate date, months int, roi float,PRIMARY KEY(sno));")
		cursor.execute(x)
	cursor.execute("show tables;")
	for y in cursor:
		tables.append(y)	
	for table in tables:
		#print("a")
		if userr in table:
			print("Success")
		else:
			x=str("create table if not exists "+userr+" (sno int,loanname varchar(50), loantype varchar(20),loanamt float, loandate date, months int, roi float,PRIMARY KEY(sno));")
			cursor.execute(x)

	asdas=True
	while asdas==True:
		inp=input("""You can do the following:\n1.View Loans\n2.Add Loans\n3.View Details of Loan\n4.Delete loans\n5.Exit\nWhat do you want to do?: """)
		if inp=='1':
			cursor.execute("select * from "+userr+";")
			if cursor.fetchall()==[]:
				print("No records found.\n")
			else:
				cursor.execute("select * from "+userr+";")
				print(tabulate(cursor,headers=["Serial number","Name","Type","Amount","Date of Issue","Months","Interest rate % p.a"],tablefmt='fancy_grid'))
				# for l in cursor:
				# 	for n0 in l:
				# 		print(str(n0),end='|')
				print("")
		elif inp=='2':
			kl=[]
			cursor.execute("select * from "+userr+";")
			for l in cursor:
				kl.append(l[0])
			if kl==[]:
				k1=1
			else:
				k1=str(int(kl[-1])+1)
			a11=input("Item/Purpose for which loan was taken: ")
			a12=input("Interest type(Coumpound/Simple)(C/S): ")
			a13=input("Amount borrowed: ")
			a14=input("Date of issue(YYYY-MM-DD): ")
			#a15=input("Amount Paid: ")
			a16=input("Time to return loan(Months): ")
			#a17=input("Last paid(YYYY-MM-DD): ")
			a18=input("Rate of Interest per annum:")
			#dat=[cursor.rowcount,a11,a12,a13,a14,a15,a16,a17]
			

			#	print(str("insert into "+userr+" values("+str(k1)+",'"+str(a11)+"'"+",'"+str(a12)+"',"+str(a13)+",'"+str(a14)+"',"+str(a16)+","+str(a18)+");"))
			cursor.execute(str("insert into "+userr+" values("+str(k1)+",'"+str(a11)+"'"+",'"+str(a12)+"',"+str(a13)+",'"+str(a14)+"',"+str(a16)+","+str(a18)+");"))
			mydb.commit()
			print("Successfully added.\n")
		

		elif inp=='3':
			cursor.execute("select * from "+userr+";")
			if cursor.fetchall()==[]:
				print("No records found.\n")
				continue
			h=input("Enter the serial number of loan you want to view: ")
			cursor.execute("select * from "+userr+" where sno="+h+";")
			print(tabulate(cursor,headers=["Serial number","Name","Type","Amount","Date of Issue","Months","Interest rate % p.a"],tablefmt='fancy_grid'))
			print("")
			cursor.execute("select * from "+userr+" where sno="+h+";")
			for l in cursor:
				
				# for n0 in l:
				# 	print(str(n0),end='|')

				if l[2].lower() in 'compound':
					
					emi=((int(l[3]))*((1 + ((int(l[-1]))/1200))**int(l[-2]))*((int(l[-1]))/1200))/(((1+(int(l[-1])/1200))**int(l[-2]))-1)
					ta= (emi*int(l[-2]))
					ti=ta-int(l[3])
					print("Your EMI is ",emi)
					print("Your total amount is ",ta,"(excluding fees and charges from lender)")
					print("Your total interest is ",ti,"\n")

				elif l[2].lower() in 'simple':
					ta= int(l[3])*(1 + (int(l[-1])*int(l[-2])/1200))
					emi=int(l[3])*int(l[-1])*int(l[-2])/(1200)
					print("Your total interest is ",emi)
					print("Your total amount is ",ta,"\n")
					

		elif inp=='4':
			cursor.execute("select * from "+userr+";")
			if cursor.fetchall()==[]:
				print("No records found.\n")
				continue
			else:
				inp1=input("Enter the serial number of the loan you want to delete:(enter 0 if not sure) ")
				if inp1=='0':
					continue
				cursor.execute("delete from "+userr+" where sno="+inp1+";")
				mydb.commit()
				print("Successfully deleted.\n")


		elif inp=='5':
			f1.close()
			quit()
			

		else:
			print("Choose a valid option.\n")

screen1()