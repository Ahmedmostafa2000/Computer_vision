import cv2
import time
import os
import mediapipe as mp
import pyautogui
import sys

# initiating detection and drawing 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screen_res = [1280,1024]
Res_x = 640
Res_y = 480
cap = cv2.VideoCapture(1)
# setting resolution
cap.set(3, Res_x) 
cap.set(4, Res_y) 


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
		image = cv2.flip(image, 1)
		results = hands.process(image)
		hand_lm = results.multi_hand_landmarks
		# cv2.rectangle(image, (Res_x//10, Res_y//10), (Res_x-Res_x//10, Res_y-Res_y//10), (0, 255, 0), 2)
		# to be edited later
		small_rect_dim = screen_res #[Res_x - 2*Res_x//10,Res_y - 2*Res_y//10]
		# In right hand:
		# middle finger is used to move the cursor
		# when the index finger is below the tip of the middle finger it counts left click
		# when th thumb is on the right of the base of it it counts a right click
		if hand_lm:
			for handLms in results.multi_hand_landmarks:
				for ide, lm in enumerate(handLms.landmark):
					hand_lm_n[ide]=lm
			x1 = int(hand_lm_n[8].x*Res_x)
			y1 = int(hand_lm_n[8].y*Res_y)
			x2 = int(hand_lm_n[12].x*Res_x)
			y2 = int(hand_lm_n[12].y*Res_y)
			x3 = int(hand_lm_n[4].x*Res_x)
			y3 = int(hand_lm_n[4].y*Res_y)
			x4 = int(hand_lm_n[2].x*Res_x)
			y4 = int(hand_lm_n[2].y*Res_y)
			if x2>=Res_x//10 and x2<=Res_x-Res_x//10 and y2>=Res_y//10 and  y2<=Res_y-Res_y//10:
				pyautogui.moveTo(x2*screen_res[0]/Res_x, y2*screen_res[0]/Res_y)
			if y1>=y2:
				cv2.circle(image, (x1,y1),10,(125,22,87),2)
				pyautogui.click()
			else:
				cv2.circle(image, (x1,y1),10,(125,22,87),cv2.FILLED)

			if x3>=x4:
				cv2.circle(image, (x3,y3),10,(22,125,87),cv2.FILLED)
				pyautogui.click(button='right')
			else:
				cv2.circle(image, (x3,y3),10,(22,125,87),2)
				
			cv2.circle(image, (x2,y2),10,(255,225,255),cv2.FILLED)
			cv2.circle(image, (x4,y4),10,(255,225,255),cv2.FILLED)
		
		
		#cv2.putText(image,str(int(fps)),(600,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		cv2.imshow("Image",image)
		if cv2.waitKey(1) & 0xFF == ord("q"): #millisecond delay
			break
