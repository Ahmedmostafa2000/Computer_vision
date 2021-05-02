import cv2
import time
import os
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(1)

cap.set(3, 640) #setting height
cap.set(4, 480) #setting width
finegers_imgs = []
for i in range(6):
	finegers_imgs.append(cv2.imread(f"images/{i}.png"))
 #adding useless photo(could be used for)
count = 0
#determining finger tops and bases to know how many fingers are up
fingers_top = [8,12,16,20,4]
fingers_bot = [6,10,14,18,5]
#landmark list
hand_lm_n = [0]*21


#adjusting Hands module
with mp_hands.Hands(
    min_detection_confidence=0.5,
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
			for i in range(5):
				if hand_lm_n[fingers_top[i]].y<hand_lm_n[fingers_bot[i]].y:
					count+=1
			#drawing landmarks
			for hand_landmarks in hand_lm:
				mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
		#printing HUD info
		cv2.putText(image,str(int(fps)),(600,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		cv2.putText(image,str(count),(600,400),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		image[0:47,0:45]=finegers_imgs[count]
		cv2.imshow("Image",image)
		if cv2.waitKey(1) & 0xFF == ord("q"): #millisecond delay
			break
		count = 0
