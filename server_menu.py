import socket as sk
import subprocess as sp
import os
def command(dat,session): #FUNCTION TO EXECUTE COMMAND AND SEND OUTPUT TO CLIENT
	output=sp.getoutput(dat)
	print(output)
	output=output.encode()
	session.send(output)
def camrun(dat,session,address): #FUNCTION TO EXECUTE CAMERA LOCALLY AND SEND THE PHOTO TO CLIENT
	os.system("python3 /root/Desktop/python/Day4-Camera.py")
	os.system("scp /root/Desktop/pic1.png {}:/root/Desktop/".format(address))
	os.system("rm /tmp/pic1.png")
	session.send(dat.encode())
def nodeconfig_hdfs(data,data2):
	os.system("""echo '<?xml version="1.0"?>' > /tmp/hdfs-site.xml""")
	os.system("""echo '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>' >> /tmp/hdfs-site.xml""")
	os.system('echo "<configuration>" >> /tmp/hdfs-site.xml')
	os.system('echo "<property>" >> /tmp/hdfs-site.xml')
	os.system('echo "<name>dfs.{}.dir</name>" >> /tmp/hdfs-site.xml'.format(data))
	os.system('echo "<value>/{}</value>" >> /tmp/hdfs-site.xml'.format(data2))
	os.system('echo "</property>" >> /tmp/hdfs-site.xml')
	os.system('echo "</configuration>" >> /tmp/hdfs-site.xml')
def nodeconfig_mapred(data):
	os.system("""echo '<?xml version="1.0"?>' > /tmp/mapred-site.xml""")
	os.system("""echo '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>' >> /tmp/mapred-site.xml""")
	os.system('echo "<configuration>" >> /tmp/mapred-site.xml')
	os.system('echo "<property>" >> /tmp/mapred-site.xml')
	os.system('echo "<name>mapred.job.tracker</name>" >> /tmp/mapred-site.xml')
	os.system('echo "<value>{}:9002</value>" >> /tmp/mapred-site.xml'.format(data))
	os.system('echo "</property>" >> /tmp/mapred-site.xml')
	os.system('echo "</configuration>" >> /tmp/mapred-site.xml')
def nodeconfig_core(data):
	os.system("""echo '<?xml version="1.0"?>' > /tmp/core-site.xml""")
	os.system("""echo '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>' >> /tmp/core-site.xml""")
	os.system('echo "<configuration>" >> /tmp/core-site.xml')
	os.system('echo "<property>" >> /tmp/core-site.xml')
	os.system('echo "<name>fs.default.name</name>" >> /tmp/core-site.xml')
	os.system('echo "<value>hdfs://{}:9001</value>" >> /tmp/core-site.xml'.format(data))
	os.system('echo "</property>" >> /tmp/core-site.xml')
	os.system('echo "</configuration>" >> /tmp/core-site.xml')
def load_image(data,ip):
	os.system("scp /root/Downloads/{} {}:/tmp/".format(data,ip))
	os.system("ssh {} docker load -i /tmp/{}".format(ip,data))
	os.system("ssh {} rm /tmp/{}".format(ip,data)) 
def socket1():
	s=sk.socket() #SET SOCKET
	s.setsockopt( sk.SOL_SOCKET, sk.SO_REUSEADDR, 1 ) #ALLOW FOR SOCKET REUSING
	ip="192.168.43.39"
	port=8095
	s.bind((ip,port)) #BIND IP AND PORT(SOCKET)
	s.listen() #LISTEN TO PORT
	while True: #ACCEPT CLIENTS INFINITE
		csess,caddr=s.accept() #ACCEPT CONNECTION FROM CLIENT (CSESS(SESSION) AND CADDR(IP_ADDRESS))
		print(caddr,"CONNECTED")
		loc=csess.recv(10) #RECIEVE LOCATION FROM CLIENT
		loc=loc.decode() #DECODE FROM BYTE TO STR
		loc=loc.lower()
		if loc=='local' or loc=='l':
			while True: # LOC EQUALS LOCAL RUN LOCAL COMMAND INIFINITE
				data=csess.recv(10)
				data=data.decode()
				if data == '1':
					command("date",csess)
				elif data == '2':
					command("cal",csess)
				elif data == '5':
					camrun("Picture Saved at /root/Desktop",csess,caddr[0])
				elif data == '7':
					break
				elif data == '6':
					hmsg=csess.recv(10)
					hmsg=hmsg.decode()
					print(hmsg)
					if hmsg=='1':
						os.system("scp /root/Downloads/hadoop-1.2.1-1.x86_64.rpm {}:/tmp".format(caddr[0]))
						os.system("ssh {} rpm -ivh /tmp/hadoop-1.2.1-1.x86_64.rpm --force".format(caddr[0]))
						os.system("ssh {} rm /tmp/hadoop-1.2.1-1.x86_64.rpm".format(caddr[0]))
						msg="HADOOP INSTALLED"
						csess.send(msg.encode())
					elif hmsg=='2':
						nodeconfig_hdfs("name","name")
						nodeconfig_core(caddr[0])
						os.system("scp /tmp/hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(caddr[0]))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(caddr[0]))
						os.system("ssh {} rm -r -f /name".format(caddr[0]))
						os.system("ssh {} mkdir /name".format(caddr[0]))
						os.system("echo Y | ssh {} hadoop namenode -format".format(caddr[0]))
						os.system("ssh {} hadoop-daemon.sh start namenode".format(caddr[0]))
						os.system("rm /tmp/hdfs-site.xml")
						os.system("rm /tmp/core-site.xml")
						msg="HADOOP NAMENODE READY"
						csess.send(msg.encode())
					elif hmsg=='3':
						nn=csess.recv(20)
						print(nn)
						nodeconfig_hdfs("data","sdata")
						nodeconfig_core(nn.decode())
						os.system("scp /tmp/hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(caddr[0]))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(caddr[0]))
						os.system("ssh {} rm -r -f /sdata".format(caddr[0]))
						os.system("ssh {} mkdir /sdata".format(caddr[0]))
						os.system("echo Y | ssh {} hadoop namenode -format".format(caddr[0]))
						os.system("ssh {} hadoop-daemon.sh start datanode".format(caddr[0]))
						os.system("rm /tmp/hdfs-site.xml")
						os.system("rm /tmp/core-site.xml")
						msg="HADOOP DATANODE READY"
						csess.send(msg.encode())
					elif hmsg=='4':
						nn=csess.recv(20)
						print(nn)
						jt=csess.recv(20)
						print(jt)
						nodeconfig_core(nn.decode())
						nodeconfig_mapred(jt.decode())
						os.system("scp /tmp/mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(caddr[0]))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(caddr[0]))
						os.system("rm /tmp/core-site.xml")
						os.system("rm /tmp/core-site.xml")
						msg="HADOOP CLIENT READY\n YOU CAN ACCESS CLUSTER THOUGH 'http://{}:50070'".format(nn.decode())
						csess.send(msg.encode())
					elif hmsg=='5':
						nn=csess.recv(20)
						print(nn)
						nodeconfig_core(nn.decode())
						nodeconfig_mapred(caddr[0])
						os.system("scp /tmp/mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(caddr[0]))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(caddr[0]))
						os.system("ssh {} hadoop-daemon.sh start jobtracker".format(caddr[0]))
						os.system("rm /tmp/mapred-site.xml")
						os.system("rm /tmp/core-site.xml")
						msg="HADOOP JOBTRACKER READY"
						csess.send(msg.encode())
					elif hmsg=='6':
						jt=csess.recv(20)
						print(jt)
						nodeconfig_mapred(jt.decode())
						os.system("scp /tmp/mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(caddr[0]))
						os.system("ssh {} hadoop-daemon.sh start tasktracker".format(caddr[0]))
						os.system("rm /tmp/mapred-site.xml")
						msg="HADOOP TASKTRACKER READY"
						csess.send(msg.encode())
					elif hmsg=='7':
						msg="TAKING YOU BACK TO MAIN MENU"
						csess.send(msg.encode())
				elif data == '3':
					msg="Functionality Still Under Works"
					csess.send(msg.encode())
				elif data == '4':
					hmsg=csess.recv(10)
					hmsg=hmsg.decode()
					print(hmsg)
					if hmsg=='1':
						os.system("ssh {} yum install docker-ce -y".format(caddr[0]))
						os.system("ssh {} systemctl enable docker".format(caddr[0]))
						os.system("ssh {} systemctl start docker".format(caddr[0]))
						msg="DOCKER READY TO ROLL"
						csess.send(msg.encode())
					elif hmsg=='2':
						nn=csess.recv(20)
						nn=nn.decode()
						if nn=='1':
							load_image("ubuntu-14.04.tar",caddr[0])
						elif nn=='2':
							load_image("centos-latest.tar",caddr[0])
						msg="OS IMAGE LOADED"
						csess.send(msg.encode())
				else:
					command("#INVALID INPUT",csess)
		elif loc == 'remote' or loc == 'r': # LOC EQUALS RUN REMOTE COMMAND INFINITE
			r_ip=csess.recv(25) #RECIEVE REMOTE IP
			r_ip=r_ip.decode()
			while True:
				data=csess.recv(10)
				data=data.decode()
				print(data)
				if data == '1':
					command("ssh {} date".format(r_ip),csess)
				elif data == '2':
					command("ssh {} cal".format(r_ip),csess)
				elif data == '5':
						os.system("scp /root/Desktop/python/Day4-Camera.py {}:/tmp".format(r_ip))						
						os.system("ssh {} python3 /tmp/Day4-Camera.py".format(r_ip))
						os.system("scp {}:/tmp/pic1.png {}:/root/Desktop/".format(r_ip,caddr[0]))
						os.system("ssh {} rm /tmp/pic1.png")
						os.system("ssh {} rm /tmp/Day4-Camera.py")
						msg="PIC SAVED AT /root/Desktop"
						csess.send(msg.encode())
				elif data == '6':
					hmsg=csess.recv(10)
					hmsg=hmsg.decode()
					print(hmsg)
					if hmsg=='1':
						os.system("scp /root/Downloads/hadoop-1.2.1-1.x86_64.rpm {}:/tmp".format(r_ip))
						os.system("ssh {} rpm -ivh /tmp/hadoop-1.2.1-1.x86_64.rpm --force".format(r_ip))
						os.system("ssh {} rm /tmp/hadoop-1.2.1-1.x86_64.rpm".format(r_ip))
						msg="HADOOP INSTALLED"
						csess.send(msg.encode())
					elif hmsg=='2':
						nodeconfig_hdfs("name","name")
						nodeconfig_core(r_ip)
						os.system("scp /tmp/hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(r_ip))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(r_ip))
						os.system("ssh {} rm -r -f /name".format(r_ip))
						os.system("ssh {} mkdir /name".format(r_ip))
						os.system("echo Y | ssh {} hadoop namenode -format".format(r_ip))
						os.system("ssh {} hadoop-daemon.sh start namenode".format(r_ip))
						msg="HADOOP NAMENODE READY"
						csess.send(msg.encode())
					elif hmsg=='3':
						nn=csess.recv(20)
						print(nn)
						nodeconfig_hdfs("data","sdata")
						nodeconfig_core(nn.decode())
						os.system("scp /tmp/hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(r_ip))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(r_ip))
						os.system("ssh {} rm -r -f /sdata".format(r_ip))
						os.system("ssh {} mkdir /sdata".format(r_ip))
						#os.system("ssh {} hadoop namenode -format".format(r_ip))
						os.system("ssh {} hadoop-daemon.sh start datanode".format(r_ip))
						msg="HADOOP DATANODE READY"
						csess.send(msg.encode())
					elif hmsg=='4':
						nn=csess.recv(20)
						print(nn)
						jt=csess.recv(20)
						print(jt)
						nodeconfig_core(nn.decode())
						nodeconfig_mapred(jt.decode())
						os.system("scp /tmp/mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(r_ip))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(r_ip))
						os.system("rm /tmp/core-site.xml")
						os.system("rm /tmp/core-site.xml")
						msg="HADOOP CLIENT READY\n YOU CAN ACCESS CLUSTER THOUGH 'http://{}:50070'".format(nn.decode())
						csess.send(msg.encode())
					elif hmsg=='5':
						nn=csess.recv(20)
						print(nn)
						nodeconfig_core(nn.decode())
						nodeconfig_mapred(r_ip)
						os.system("scp /tmp/mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(r_ip))
						os.system("scp /tmp/core-site.xml {}:/etc/hadoop/core-site.xml".format(r_ip))
						os.system("ssh {} hadoop-daemon.sh start jobtracker".format(r_ip))
						os.system("rm /tmp/mapred-site.xml")
						os.system("rm /tmp/core-site.xml")
						msg="HADOOP JOBTRACKER READY"
						csess.send(msg.encode())
					elif hmsg=='6':
						jt=csess.recv(20)
						print(jt)
						nodeconfig_mapred(jt.decode())
						os.system("scp /tmp/mapred-site.xml {}:/etc/hadoop/mapred-site.xml".format(r_ip))
						os.system("ssh {} hadoop-daemon.sh start tasktracker".format(r_ip))
						os.system("rm /tmp/mapred-site.xml")
						msg="HADOOP TASKTRACKER READY"
						csess.send(msg.encode())
					elif hmsg=='7':
						msg="TAKING YOU BACK TO MAIN MENU"
						csess.send(msg.encode())
				elif data == '7':
					break
				elif data == '4':
					hmsg=csess.recv(10)
					hmsg=hmsg.decode()
					print(hmsg)
					if hmsg=='1':
						os.system("ssh {} yum install docker-ce -y".format(r_ip))
						os.system("ssh {} systemctl enable docker".format(r_ip))
						os.system("ssh {} systemctl start docker".format(r_ip))
						msg="DOCKER READY TO ROLL"
						csess.send(msg.encode())
					elif hmsg=='2':
						nn=csess.recv(20)
						nn=nn.decode()
						print(nn)
						if nn=='1':
							load_image("ubuntu-14.04.tar",r_ip)
						elif nn=='2':
							load_image("centos-latest.tar",r_ip)
						msg="OS IMAGE LOADED"
						csess.send(msg.encode())
				elif data == '3':
					msg="Functionality Still Under Works"
					csess.send(msg.encode())
				else:
					command("#INVALID INPUT",csess)
	
		csess.close()
socket1()
