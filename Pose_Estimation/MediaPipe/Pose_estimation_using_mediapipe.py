#importing necessary libraries
import cv2
import pandas as pd
import mediapipe as mp
capture = cv2.VideoCapture("Ahmad720.mp4")
forcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output/new1.avi',forcc,20.0,(1280,720))




mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
fps_record = []
lm_record = []
frame_num = 0
while True:
	try:
		#Calculating fps
		timer = cv2.getTickCount()
		#reading realtime image
		success, image = capture.read()
		frame_num+=1
		if not success:
			break
		results = pose.process(image)
		if results.pose_landmarks:
			mpDraw.draw_landmarks(image,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
			for number, landmark in enumerate(results.pose_landmarks.landmark):
				h, w, c = image.shape
				lm_record.append([frame_num,number,landmark.x,landmark.y,landmark.z,landmark.visibility])

		#Calculating fps
		fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
		if success:
			fps_record.append(fps)
		out.write(image)
		#showing fps
		cv2.putText(image,str(int(fps)),(600,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
		#showing the current frame
		cv2.imshow("Object",image)
	except cv2.error:
		pass

	#to close the loop and end the app
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

df = pd.DataFrame(lm_record)
df.to_csv("A2.csv")
print(min(fps_record),max(fps_record),sum(fps_record)/len(fps_record))
out.release()
