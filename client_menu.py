import socket as sk
s=sk.socket()
s_ip="192.168.43.39"
s_port=8095
s.connect((s_ip,s_port)) #CONNECT TO SERVER
loc=input("ENTER LOCATION(local/remote): ") #ENTER LOCATION
s.send(loc.encode()) #SEND LOCATION TO SERVER
if loc == 'remote' or loc == 'r': #IF LOC EQUALS REMOTE
	r_ip=input("ENTER REMOTE IP: ") #INPUT REMOTE MACHINE IP
	s.send(r_ip.encode()) #SEND REMOTE IP TO SERVER
while True: #LOOP UNTIL EXIT PRESSED
	print("""
	Press 1: Check Date
	Press 2: Check Calendar
	#Press 3: Create File(Under works)
	Press 4: Docker Configuration
	Press 5: Click Photo
	Press 6: Hadoop Configuration
	Press 7: Exit
	""")
	data=input("ENTER CHOICE: ") 
	data1=data.encode() #SEND CHOICE
	s.send(data1)
	if data=="7":
		break
	elif data=='4':
		print("""
		1.INSTALL HADOOP(JDK REQ.)
		2.LOAD OS IMAGE""")
		data=input("ENTER CHOICE:" )
		s.send(data.encode())
		if data=='2':
			nn=input("NAMENODEIP: ")
			s.send(nn.encode())
	elif data=="6":
		print("""
		1.INSTALL HADOOP(JDK REQ.)
		2.SETUP NAMENODE
		3.SETUP DATANODE
		4.SETUP CLIENT
		5.SETUP JOBTRACKER
		6.SETUP TASKTRACKER
		7.EXIT HADOOP INSTALLATION/CONFIGURATION""")
		data=input("ENTER CHOICE:" )
		s.send(data.encode())
		if data=='3' or data=='5':
			nn=input("NAMENODEIP: ")
			s.send(nn.encode())
		elif data=='4':
			nn=input("NAMENODE IP: ")
			s.send(nn.encode())
			jt=input("JOBTRACKER IP: ")
			s.send(jt.encode())
		elif data=='6':
			jt=input("JOBTRACKER IP: ")
			s.send(jt.encode())
	out=s.recv(200)
	out=out.decode()
	print(out)
print("THANK YOU FOR USING OUR SERVICE")

