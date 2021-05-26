import cv2
import numpy as np



Res_x = 640
Res_y = 480
cap = cv2.VideoCapture(0)
# setting resolution
cap.set(3, Res_x) 
cap.set(4, Res_y) 

def nothing(x):
	pass

#finding and drawing contours function
def find_countours(image,draw =True, bbox = False):
	contours,hierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	for cnt in contours:
		area = cv2.contourArea(cnt)
		#area threshold
		if area>50:
			if draw:
				cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
			peri = cv2.arcLength(cnt,True)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True)
			x, y, w, h = cv2.boundingRect(approx)
			if bbox:
				cv2.rectangle(imgResult,(x,y),(x+w,y+h),(0,255,0),2)
			return x,y
	return False,False
			
drawn_image = np.zeros((Res_y,Res_x,3))

### uncomment to find other colors' threshold
# cv2.resizeWindow("TrackBars",600,100)
# cv2.namedWindow("TrackBars")
# cv2.createTrackbar("Hue Min","TrackBars",0,179,nothing)
# cv2.createTrackbar("Hue Max","TrackBars",19,179,nothing)
# cv2.createTrackbar("Sat Min","TrackBars",110,255,nothing)
# cv2.createTrackbar("Sat Max","TrackBars",240,255,nothing)
# cv2.createTrackbar("Val Min","TrackBars",153,255,nothing)
# cv2.createTrackbar("Val Max","TrackBars",255,255,nothing)

x1,y1 = False,False
while True:
	success, image = cap.read()
	
	imgHSV = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)

	### uncomment to find other colors' threshold
	# h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
	# h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
	# s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
	# s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
	# v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
	# v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
	# lower = np.array([h_min,s_min,v_min])
	# upper = np.array([h_max,s_max,v_max])
	# mask = cv2.inRange(imgHSV,lower,upper)

	# yellow threshold and mask
	yellow = np.array([[ 71, 140, 192],[103, 255, 255]])
	yellow_mask = cv2.inRange(imgHSV,yellow[0],yellow[1])
	imgResult = cv2.bitwise_and(image,image,mask=yellow_mask)
	x2, y2 = find_countours(yellow_mask,1,1)
	if x2:
		if x1:
			cv2.line(drawn_image,(x1,y1),(x2,y2),(28,168,243),5)
	cv2.rectangle(image, (0,0), (50,50), (255,255,255), 5)
	if 0<x2<50 and 0<y2<50:
		drawn_image = np.zeros((Res_y,Res_x,3))
	x1,y1 = x2,y2
	image = drawn_image.astype(np.uint8)|image.astype(np.uint8)
	cv2.imshow("Original",image)

	cv2.imshow("Result", imgResult)
	# millisecond delay
	if cv2.waitKey(1) & 0xFF == ord("q"):
		### uncomment to find other colors' threshold
		# print(lower)
		# print(upper)
		break