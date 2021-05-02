import cv2
import time
import os
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#Transforming distance between fingers to volume
def hand2vol(distance):
	distance = ((distance-30)/300)*65
	return distance

def hand2color(distance):
	distance = ((distance-50)/250)*254
	return distance

#initialising media pipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


#inintiating volume controller
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))





cap = cv2.VideoCapture(1)

cap.set(3, 640) #setting height
cap.set(4, 480) #setting width
finegers_imgs = []
for i in range(6):
	finegers_imgs.append(cv2.imread(f"images/{i}.png"))

#landmark list
hand_lm_n = [0]*21


#adjusting Hands module
with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:
	#capturing loop
	while True:
		#calculating fps
		timer = cv2.getTickCount()
		fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
		#reading camera
		success, image = cap.read()
		
		results = hands.process(image)
		hand_lm = results.multi_hand_landmarks
		# print(results.multi_hand_landmarks)
		
		
		if hand_lm:
			for handLms in results.multi_hand_landmarks:
				for ide, lm in enumerate(handLms.landmark):
					hand_lm_n[ide]=lm

			x1 = int(hand_lm_n[4].x*640)
			y1 = int(hand_lm_n[4].y*480)

			x2 = int(hand_lm_n[8].x*640)
			y2 = int(hand_lm_n[8].y*480)

			xc = (x1+x2)//2
			yc = (y1+y2)//2

			distance = ((x1-x2)**2+(y1-y2)**2)**.5
			#Drawing HUD
			cv2.circle(image, (x1,y1),15,(125,22,87),cv2.FILLED)
			cv2.circle(image, (x2,y2),15,(125,22,87),cv2.FILLED)
			cv2.circle(image, (xc,yc),10,(hand2color(distance),hand2color(distance),hand2color(distance)),cv2.FILLED)
			cv2.line(image,(int(hand_lm_n[4].x*640),int(hand_lm_n[4].y*480)),(int(hand_lm_n[8].x*640),int(hand_lm_n[8].y*480)),(125,22,87),3 )
			try:
				volume.SetMasterVolumeLevel(-hand2vol(distance), None)
			except:
				pass
			#drawing landmarks
			for hand_landmarks in hand_lm:
				mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
		#printing HUD info
		image = cv2.flip(image, 1)
		cv2.putText(image,str(int(fps)),(600,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

		cv2.imshow("Image",image)
		if cv2.waitKey(1) & 0xFF == ord("q"): #millisecond delay
			break
