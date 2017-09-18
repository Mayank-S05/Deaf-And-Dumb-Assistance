import cv2
import numpy as np
import matplotlib.pyplot as plt

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
fist_cascade = cv2.CascadeClassifier('fist.xml')
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
while True:
 	ret , img = cap.read()
 	fist_roi = img[100:300 , 100:300]
 	hsv = cv2.cvtColor(fist_roi , cv2.COLOR_BGR2HSV)
 	lower_skin = np.array([0,48,80] , dtype="uint8")
 	upper_skin = np.array([20,255,255	] , dtype="uint8")
 	mask = cv2.inRange(hsv , lower_skin , upper_skin)
 	res = cv2.bitwise_and(fist_roi , fist_roi , mask=mask)
 	fgmask = fgbg.apply(res)
 	median = cv2.medianBlur(res,15)

 	fist_gray = cv2.cvtColor(fist_roi , cv2.COLOR_BGR2GRAY)
 	#faces = face_cascade.detectMultiScale(gray)
 	fist = fist_cascade.detectMultiScale(fist_gray)
 	cv2.rectangle(img ,(100,100) , (300,300) , (255,0,0),2)
 	
 	for(x,y,w,h) in fist:
 		cv2.rectangle(img , (100+x,100+y), (100+x+w , 100+y+h) , (0,0,255), 2)
 		roi_gray = fist_gray[y:y+h , x:x+w]
 		roi_color = fist_roi[y:y+h , x:x+w]
 		#roi_fist = img[y:y+h+20 , x:x+w+20]
 		#if roi_fist is not None:
 		#	cv2.imshow('roi' , roi_fist)
 	
 	cv2.imshow('ing' , img)
 	#cv2.imshow('fst' , fist_gray)
 	cv2.imshow('mask'  , mask)
 	cv2.imshow('res' , res)
 	cv2.imshow('median' , median)
 	cv2.imshow('Backred' , fgmask)
 	
 	
 	k = cv2.waitKey(30) & 0xFF
 	if k==27:
 		break

cap.release()
cv2.destroyAllWindows()