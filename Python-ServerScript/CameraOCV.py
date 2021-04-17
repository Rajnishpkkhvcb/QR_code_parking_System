import cv2
import imutils
import numpy as np
import pytesseract
#from openalpr import Alpr
from PIL import Image
import time, threading

interval = 1

def check():
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    print("Taking a photo")
    img = frame
    img = cv2.resize(img, (620,480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt is None:
        detected = 0
        print("No Contour detected")
    else:
        detected = 1
    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)
        
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        text = pytesseract.image_to_string(Cropped, config='--psm 11')
        print("Detected Number is:",text)

        #cv2.imshow('image',img)
        #cv2.imshow('Cropped',Cropped)



#img = cv2.imread('test.jpg',cv2.IMREAD_COLOR)


cap = cv2.VideoCapture(0)
#alpr = Alpr("in" , "/Users/aryanganotra/openalpr/config/openalpr.conf.defaults" ,
                   # "/Users/aryanganotra/openalpr/runtime_data")


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    #ret, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    #print("Taking a photo")
    #cv2.imshow('image',frame)
    
    n=check()
    #cv2.imshow('Image',frame)
    #cv2.imwrite('sample.jpg', frame)
    #analysis = alpr.recognize_file("/sample.jpg")
    #if len(analysis['results']) == 0:
       # print("No number plate detected")
   # else:
        #print("Number plate detected",analysis['results'][0]['plate'])
    
    c = cv2.waitKey(1)
    if c>65:
        break

def start():
    threading.Timer(interval, start).start()
    check()
#start();
cap.release()
cv2.destroyAllWindows()

#alpr.unload()
