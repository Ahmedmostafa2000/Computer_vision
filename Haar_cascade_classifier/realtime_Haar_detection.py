#importing libraries
import cv2
import numpy as np


face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#making a video capture object
realtime = cv2.VideoCapture(0)

while True:
    #starting realtime video
    ret, img = realtime.read()
    #converting image to gray for the haar detection
    img_2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #applying the detecting on the image
    faces = face_detector.detectMultiScale(img_2, 1.3, 5)
    for (x,y,w,h) in faces:
    # drawing recatngles on the detected faces 
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),3)
        cv2.putText(img,"Found one here", (x,y-10)
                , cv2.FONT_HERSHEY_SIMPLEX
                , .4
                , (255,255,255))
    cv2.imshow('Hi',img)
    #to quit using 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#closing realtime
realtime.release() 
cv2.destroyAllWindows()






