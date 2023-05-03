#--------------[Libary]--------------------------------------------------------------------------#
import cv2 as cv
import urllib.request
import numpy as np
import serial 
#--------------[Resolution]----------------------------------------------------------------------#
#High resolution:                                                              
#url="http://192.168.68.114/cam-hi.jpg"
#Cam2
url="http://192.168.68.112/cam-hi.jpg"                                                                                                                   
print('Found URL ! ',url)

#--------------[Open PORT]-----------------------------------------------------------------------#
#Test Port
#ser = serial.Serial('COM',baudrate=112500, timeout=1)
#Port STM32
ser = serial.Serial('COM3',baudrate=112500, timeout=1)
print("COM PORT open success !")

#---------[OPen Camera]--------------------------------------------------------------------------#
#Wifi cam
img_request = urllib.request.urlopen(url)
img_np = np.array(bytearray(img_request.read()), dtype=np.uint8)
frame = cv.imdecode(img_np, -1)
weight,height,_=frame.shape
x_medium =int(height/2)
y_medium =int(weight/2)
print("Camera open success !")
Transmit=ser.write(b'0\n')

# Value Center
center_x = int(height/2) 
center_y = int(weight/2)
x_min=int(height/2)-40
x_max=int(height/2)+40 
y_min=int(weight/2)-40
y_max=int(weight/2)+40


#Run Camera
while True:
    #Read Wifi Camera
    img_request = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_request.read()), dtype=np.uint8)
    frame = cv.imdecode(img_np, -1)
    #Case 0 : no move 
    Transmit=ser.write(b'0\n')

    print('Case 0 USE')
    #-------------------PROCESSING IMAGE---------------------------------------------------------------------#
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
            y_medium= int((y+y+h)/2)
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),1)
                #-------------------MOVE CASE----------------------------------------------------------------------#
            #Case Angle 1:
            if (x_medium < center_x ) and (y_medium < center_y) :
                Transmit=ser.write(b'1\n')
                print("Case 1 USE")
            #Case Angle 2: -> FIX
            elif (x_medium < center_x) and (y_medium > center_y):
                Transmit=ser.write(b'2\n')
                print("Case 2 USE")
            #Case Angle 3: -> FIX
            elif (x_medium > center_x) and (y_medium < center_y):
                Transmit=ser.write(b'3\n')
                print("Case 3 USE")
            #Case Angle 4:
            elif (x_medium > center_x) and (y_medium > center_y):
                Transmit=ser.write(b'4\n')
                print("Case 4 USE")
            break

    #Draw intersection x,y and boudin box
    cv.line(frame,(x_medium,0),(x_medium,780),(0,255,0),1)
    cv.line(frame,(0,y_medium),(870,y_medium),(0,255,0),1)
    #Origin Coordinate
    cv.line(frame,(center_x,0),(center_x,780),(0,0,255),1)
    cv.line(frame,(0,center_y),(870,center_y),(0,0,255),1)

    #Display
    cv.imshow("Esp32", frame)
    if cv.waitKey(10) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break