# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui
from PIL import Image



def SEGMENT(event,x,y,flags,param): 
	if event == cv2.EVENT_LBUTTONDOWN: 
		
				
		cv2.floodFill(B, mask, (x,y), 255);
		img1_bg = cv2.bitwise_and(img,img,mask = B)
		img1_bg[np.where((img1_bg == [255,0,0]).all(axis = 2))] = [255,255,255]
		img1_bg[np.where((img1_bg == [0,0,0]).all(axis = 2))] = [255,255,255]
		img1_bg = cv2.cvtColor(img1_bg, cv2.COLOR_RGB2GRAY)
		

		cv2.imshow('Cervical1',threshold1)
		croppedimg = originalimg



		
# Opening an image using a File Open dialog:
img = cv2.imread("Cervical.jpg")
originalimg = img


cv2.namedWindow('Cervical',600)
cv2.setMouseCallback('Cervical',SEGMENT)
#cv2.imshow("Cervical",originalimg)


imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
ret, threshold1 = cv2.threshold(imgGray,200,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


# noise removal
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(threshold1,cv2.MORPH_OPEN,kernel, iterations = 0)
cv2.imshow('Cervical2',opening)

# Background area
background = cv2.dilate(opening,kernel,iterations=2)

# Foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.05*dist_transform.max(),255,0)
cv2.imshow('Cervical3',sure_fg)

# Unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(background,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
 
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]


blue, green, red = cv2.split(img)
#im_color = cv2.applyColorMap(img, cv2.COLORMAP_JET)

ret,B = cv2.threshold(blue,254,255,cv2.THRESH_BINARY)


h, w = B.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

constant = cv2.copyMakeBorder(img,2,2,2,2,cv2.BORDER_CONSTANT,(0,0,0))

while(1):
    
    if cv2.waitKey(20) & 0xFF == 27:
	        break
cv2.destroyAllWindows()
