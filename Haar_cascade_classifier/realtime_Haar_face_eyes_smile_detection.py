#importing libraries
import cv2


face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyes_detector = cv2.CascadeClassifier('haarcascade_eye.xml')
smil_detector = cv2.CascadeClassifier('haarcascade_smile.xml')

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
        cv2.putText(img,"Found a face here", (x,y-10)
                , cv2.FONT_HERSHEY_SIMPLEX
                , .4
                , (255,255,255))

        eyes = eyes_detector.detectMultiScale(img_2[y:y+h,x:x+w], 1.1, 22)
        for (x2,y2,w2,h2) in eyes:
        	cv2.rectangle(img,(x+x2,y+y2),(x+x2+w2,y+y2+h2),(0,0,0),2)
        	cv2.putText(img,"Eye", (x+x2,y2+y-10)
            , cv2.FONT_HERSHEY_SIMPLEX
            , .7
            , (0,0,0))
        smil = smil_detector.detectMultiScale(img_2[y:y+h,x:x+w], 1.7, 22)
        for (x3,y3,w3,h3) in smil:
        	cv2.rectangle(img,(x+x3,y+y3),(x+x3+w3,y+y3+h3),(0,255,0),2)
    cv2.imshow('Hi',img)
    #to quit using 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#closing realtime
realtime.release() 
cv2.destroyAllWindows()






