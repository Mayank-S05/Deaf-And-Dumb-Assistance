import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        fist_cascade = cv2.CascadeClassifier('fist.xml')
        fgbg = cv2.createBackgroundSubtractorMOG2()

        success, image = self.video.read()
        fist_roi = image[100:300 , 100:300]
        hsv = cv2.cvtColor(fist_roi , cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0,48,80] , dtype="uint8")
        upper_skin = np.array([20,255,255] , dtype="uint8")
        mask = cv2.inRange(hsv , lower_skin , upper_skin)
        res = cv2.bitwise_and(fist_roi , fist_roi , mask=mask)
        fgmask = fgbg.apply(res)
        median = cv2.medianBlur(res,15)

        fist_gray = cv2.cvtColor(fist_roi , cv2.COLOR_BGR2GRAY)
         #faces = face_cascade.detectMultiScale(gray)
        fist = fist_cascade.detectMultiScale(fist_gray)
        cv2.rectangle(image ,(100,100) , (300,300) , (255,0,0),2)
    
        for(x,y,w,h) in fist:
            cv2.rectangle(image , (100+x,100+y), (100+x+w , 100+y+h) , (0,0,255), 2)
            roi_gray = fist_gray[y:y+h , x:x+w]
            roi_color = fist_roi[y:y+h , x:x+w]
            #roi_fist = img[y:y+h+20 , x:x+w+20]
            #if roi_fist is not None:
            #   cv2.imshow('roi' , roi_fist)
        
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()