import cv2 as cv
import urllib.request
import numpy as np

# Low resolution:
#url="http://192.168.68.114/cam-lo.jpg"
#Medium resolution:
#url="http://192.168.68.114/cam-mid.jpg"
#High resolution:
url="http://192.168.68.114/cam-hi.jpg"

# Place Center 
img_request = urllib.request.urlopen(url)
img_np = np.array(bytearray(img_request.read()), dtype=np.uint8)
frame = cv.imdecode(img_np, -1)
rows,cols,_=frame.shape
x_medium =int(cols/2)
center_x = int(cols/2) 
print("Size of Camera: ",frame.shape)
print("Row value: ",cols)
print("x_medium value: ",x_medium)
print("center_x value: ",center_x)


#Begin position
position_x = 90
position_y = 90
#Run Camera
while True:
    #Read Wifi Camera
    img_request = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_request.read()), dtype=np.uint8)
    frame = cv.imdecode(img_np, -1)

    #Processing
    frame =cv.GaussianBlur(frame,(5,5),1)
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #Detect Red Color
    low_red = np.array([161,155,84])
    high_red = np.array([179,255,255])
    red_mask = cv.inRange(hsv_frame, low_red, high_red)
    #Find center
    contours,hierachy= cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        #print('The Erea of Contour is :',area)
        if area>500:
            #Get coordinate 
            x,y,w,h = cv.boundingRect(cnt)
            x_medium= int((x+x+w)/2)
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),1)
            break

    #Draw intersection x,y and boudin box
    cv.line(frame,(x_medium,0),(x_medium,780),(0,255,0),1)

    #Data Control Motor
    if x_medium <center_x :
        position_x+=1
        print("Position X Value: ",position_x)
    elif x_medium >center_x :
        position_x-=1
        print("Position X Value: ",position_x)
    #Display
    cv.imshow("Esp32", frame)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break
frame.release()
cv.destroyAllWindows()