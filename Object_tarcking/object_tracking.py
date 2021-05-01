#importing necessary libraries
import cv2
import pandas as pd
capture = cv2.VideoCapture("blank1.mp4")
forcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output/blank1_CSRT.avi',forcc,20.0,(720,480))
# tracker = cv2.TrackerMOSSE_create()
tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerKCF_create()
# tracker = cv2.TrackerMedianFlow_create()
# tracker = cv2.TrackerGOTURN_create()
success, image = capture.read()

box = cv2.selectROI("Tracked Object", image ,False)
print(box)
exit()
tracker.init(image, box)

fps_record = []
track_record = []
while True:
	try:
		#Calculating fps
		timer = cv2.getTickCount()
		#reading realtime image
		success, image = capture.read()
		
		success, box = tracker.update(image)
		if success:
			cv2.rectangle(image,(int(box[0]),int(box[1])),(int(box[0])+int(box[2]),int(box[1])+int(box[3])),(0,255,0),3)
			cv2.putText(image,"Locked on Ahmad",(300,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
			
		else:
			cv2.putText(image,"Ahmad object fount",(300,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
		
		#Calculating fps
		fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
		if success:
			fps_record.append(fps)
		cv2.putText(image,str(int(fps)),(600,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)


		track_record.append([box[0]+box[2]/2,box[1]+box[3]/2])
		out.write(image)
		#showing the current frame
		cv2.imshow("Object",image)
	except cv2.error:
		pass
	#box is a tuple of initals, height and width x1,y1,h,w
	

	#to close the loop and end the app
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

df = pd.DataFrame(track_record, columns = ['x','y'])
df.to_csv('A2CSRTfull2.csv')
print(min(fps_record),max(fps_record),sum(fps_record)/len(fps_record))
