#--------------[Libary]---------------------------------------#
import cv2 as cv
import urllib.request
import numpy as np
import serial 
import time
#--------------[Resolution]-----------------------------------#
#                                                                
# Low resolution:                                   
#url="http://192.168.68.114/cam-lo.jpg"           
#Medium resolution:                                                            
#url="http://192.168.68.114/cam-mid.jpg"                                      
#High resolution:                                                              
url="http://192.168.68.114/cam-hi.jpg"
#Cam2
#url="http://192.168.68.112/cam-hi.jpg"                                        
#                                                                               
#-------------------------------------------------------------#
#Open PORT
ser = serial.Serial('COM2',baudrate=112500, timeout=1)
#ser = serial.Serial('COM3',baudrate=112500, timeout=1)
time.sleep(3) # delay
print("COM PORT open success !")

# Place Center For Begin Program 
img_request = urllib.request.urlopen(url)
img_np = np.array(bytearray(img_request.read()), dtype=np.uint8)
frame = cv.imdecode(img_np, -1)
weight,height,_=frame.shape
x_medium =int(height/2)
y_medium =int(weight/2)
# Value Center
center_x = int(height/2) 
center_y = int(weight/2)
Stop_range_x_left=int(height/2)-40
Stop_range_x_right=int(height/2)+40 
Stop_range_y_up=int(weight/2)-40
Stop_range_y_down=int(weight/2)+40
print("Camera open success !")
#-------------------------------------------------------------#
# Test
# print("Size of Camera: ",frame.shape)
# print("Row value: ",height)
# print("Col value: ",weight)
# print("x_medium value: ",x_medium)
# print("y_medium value: ",y_medium)
# print("center_x value: ",center_x)
# print("center_y value: ",center_y)
# print("Camera Wifi is Connected !")
#-------------------------------------------------------------#

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
            y_medium= int((y+y+h)/2)
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),1)
            break

    #Draw intersection x,y and boudin box
    cv.line(frame,(x_medium,0),(x_medium,780),(0,255,0),1)
    cv.line(frame,(0,y_medium),(870,y_medium),(0,255,0),1)
    #Origin Coordinate
    cv.line(frame,(center_x,0),(center_x,780),(0,0,255),1)
    cv.line(frame,(0,center_y),(870,center_y),(0,0,255),1)
    #Stop range
    cv.line(frame,(Stop_range_x_left,0),(Stop_range_x_left,780),(255,0,0),1)
    cv.line(frame,(Stop_range_x_right,0),(Stop_range_x_right,780),(255,0,0),1)

    cv.line(frame,(0,Stop_range_y_up),(870,Stop_range_y_up),(255,0,0),1)
    cv.line(frame,(0,Stop_range_y_down),(870,Stop_range_y_down),(255,0,0),1)

    #--------------------------------------Data Control Motor------------------------------------------#
    
    #-------------------MOVE CASE-------------------------------#
    #Case Angle 1:
    if (x_medium < center_x and y_medium < center_y) and not ():
        #Control motor
        if(position_x<180):position_x +=1
        if(position_y<180):position_y +=1
    #Case Angle 2: -> FIX
    elif (x_medium < center_x and y_medium > center_y)and not ():
        #Control motor
        if(position_x>0):position_x -=1
        if(position_y<180):position_y +=1
    #Case Angle 3: -> FIX
    elif (x_medium > center_x and y_medium < center_y)and not ():
        #Control motor
        if(position_x<180):position_x +=1
        if(position_y>180):position_y -=1
    #Case Angle 4:
    elif (x_medium > center_x and y_medium > center_y)and not ():
        #Control motor
        if(position_x>0):position_x -=1
        if(position_y>0):position_y -=1
    #-------------------STOP CASE-------------------------------#
    elif (x_medium >Stop_range_x_left)and(x_medium<Stop_range_x_left):
        position_x=position_x
    elif (y_medium>Stop_range_y_up)and(y_medium<Stop_range_y_down):
        position_y=position_y
    #--------------------------------------Data Transform----------------------------------------------#
    #Max value

    # # Truyền dữ liệu po0=sition_x và position_y qua Serial
    STM32 = ser.write(bytes(f"{position_x},{position_y}/\n", 'utf-8'))
    print(STM32)
    print("Position Y: ",position_x)
    print("Position X: ",position_y)
    
    #Display
    cv.imshow("Esp32", frame)
    if cv.waitKey(10) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break