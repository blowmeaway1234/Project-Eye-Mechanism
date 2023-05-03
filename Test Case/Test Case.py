import cv2
import numpy as np
# Khởi tạo kích thước khung hình
width = 800
height = 600
frame = np.zeros((height, width, 3), dtype=np.uint8)

# Tính giá trị trung tâm và giới hạn x, y
center_x = int(width/2) 
center_y = int(height/2)
x_min = int(width/2) - 40
x_max = int(width/2) + 40 
y_min = int(height/2) - 40
y_max = int(height/2) + 40

# Tính giá trị trung bình của trục x và y
x_medium = int(height/2)
y_medium = int(width/2)

# Vẽ khung hình
cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

# Vẽ vùng Sub_arg1
sub_arg1 = [(x_min < x_medium) and (x_medium < center_x) and (x_medium < x_max)] # bên trái 
if sub_arg1:
    cv2.rectangle(frame, (x_min, y_min), (x_medium, y_max), (0, 255, 0), -1)

# Hiển thị khung hình
cv2.imshow("Frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
