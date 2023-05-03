import cv2 as cv
import urllib.request
import numpy as np
# Low resolution:
#url="http://192.168.68.114/cam-lo.jpg"
#Medium resolution:
#url="http://192.168.68.114/cam-mid.jpg"
#High resolution:
url="http://192.168.68.114/cam-hi.jpg"
while(1):
    #Read Wifi Camera
    img_request = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_request.read()),dtype=np.uint8)
    img= cv.imdecode(img_np,-1)
    #Processing
    blur = cv.GaussianBlur(img,(3,3),1)
    gray= cv.cvtColor(blur,cv.COLOR_BGR2GRAY)
    #binary = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV)[1]
    #contours,hierachy= cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #for cnt in contours:
    #    area = cv.contourArea(cnt)
        # print('The Erea of Contour is :',area)
        # if 3000<area<7000:
        #     #Lấy tọa độ x y z h từ q
        #     x,y,w,h = cv.boundingRect(cnt)
        #     cv.rectangle(img, (x,y), (x+w,y+h), (255,255,255),1)
    #Display
    cv.imshow("Esp32",img)
    if cv.waitKey(10) & 0xFF==ord('q'):
        img.release()
        cv.destroyAllWindows()
        break