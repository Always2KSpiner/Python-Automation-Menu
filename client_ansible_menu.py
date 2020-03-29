import cv2
import time
import numpy as np
import webbrowser
import os
from os import listdir
from os.path import isfile, join
import socket as sk
import pyttsx3 as ts # Import Text to Speech
def speak(msg):
	spkr=ts.init() #intialize TTS to a var\n",
	spkr.say(msg) #Give text to be Spoken\n",
	spkr.runAndWait() #RUn the Above text"
confidence=0
flag=0
face_classifier = cv2.CascadeClassifier('/root/Desktop/python/haarcascade_frontalface_default.xml')
#print(cv2.__version__)
# Get the training data we previously made
data_path = '/root/Downloads/myfaces/'
# a=listdir('d:/faces')
# print(a)
# """
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

# Create arrays for training data and labels
Training_Data, Labels = [], []

# Open training images in our datapath
# Create a numpy array for training data
for i, files in enumerate(onlyfiles):
	image_path = data_path + onlyfiles[i]
	images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
	Training_Data.append(np.asarray(images, dtype=np.uint8))
	Labels.append(i)
# 
# Create a numpy array for both training data and labels
Labels = np.asarray(Labels, dtype=np.int32)
model=cv2.face_LBPHFaceRecognizer.create()
# Initialize facial recognizer
# model = cv2.face_LBPHFaceRecognizer.create()
# model=cv2.f
# NOTE: For OpenCV 3.0 use cv2.face.createLBPHFaceRecognizer()

# Let's train our model 
model.train(np.asarray(Training_Data), np.asarray(Labels))
print("Initializing")




def face_detector(img, size=0.5):
    
    # Convert image to grayscale
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = face_classifier.detectMultiScale(gray, 1.3, 5)
	if faces is ():
		return img, []
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
		roi = img[y:y+h, x:x+w]
		roi = cv2.resize(roi, (200, 200))
	return img, roi


# Open Webcam
cap = cv2.VideoCapture(0)
i=0
while i<50:

	ret, frame = cap.read()
    
	image, face = face_detector(frame)
    
	try:
		face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Pass face to prediction model
        # "results" comprises of a tuple containing the label and the confidence value
		results = model.predict(face)
		#print(results)
		if results[1] < 500:
			confidence = int( 100 * (1 - (results[1])/400) )
			display_string = str(confidence) + '% Confident it is User'
            
		cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
        
		if confidence > 75:
			cv2.putText(image, "Welcome Anirudh", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
			cv2.imshow('Face Recognition', image )
			
			
                       
		else:
			cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
			cv2.imshow('Face Recognition', image )

	except:
		cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
		cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
		cv2.imshow('Face Recognition', image )
		pass
        
	if cv2.waitKey(1) == 13: #13 is the Enter Key
		break
	if (confidence>75) & (i>15):
		print ("WELCOME ANIRUDH")
		speak("WELCOME ANIRUDH")
		flag=1
		break
	i+=1

cv2.destroyAllWindows()        
cap.release()
if flag==1:
	s=sk.socket()
	s_ip="192.168.43.39"
	s_port=8095
	s.connect((s_ip,s_port)) #CONNECT TO SERVER
	#speak("ENTER LOCATION(local/remote): ")
	loc=input("ENTER LOCATION(local/remote): ") #ENTER LOCATION
	s.send(loc.encode()) #SEND LOCATION TO SERVER
	if loc == 'remote' or loc == 'r': #IF LOC EQUALS REMOTE
		#speak("ENTER REMOTE IP: ") 
		r_ip=input("ENTER REMOTE IP: ") #INPUT REMOTE MACHINE IP
		s.send(r_ip.encode()) #SEND REMOTE IP TO SERVER
	while True: #LOOP UNTIL EXIT PRESSED
		txt="""
		Press 1: Check Date
		Press 2: Check Calendar
		Press 3: HTTPD Configuration
		Press 4: Docker Configuration
		Press 5: Click Photo
		Press 6: Hadoop Configuration
		Press 7: Monitor Connection
		Press 8: Exit
		"""
		print(txt)
		#speak(txt)
		data=input("ENTER CHOICE: ") 
		data1=data.encode() #SEND CHOICE
		s.send(data1)
		if data=="8":
			break
		elif data=='4':
			print("""
			1.LOAD CENTOS IMAGE
			2.LOAD UBUNTU:14.04 IMAGE
			3.BACK TO MAINMENU""") 
			data=input("ENTER CHOICE:" )
			s.send(data.encode())
		elif data=="6":
			print("""
			1. CLUSTER SETUP
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
		elif data=='7':
			data=input("ENTER IP/HOSTNAME: ")
			s.send(data.encode())
		out=s.recv(2000)
		out=out.decode()
		print(out)
	print("THANK YOU FOR USING OUR SERVICE")
else:
	print("LOGIN FAILED TRY AGAIN")
