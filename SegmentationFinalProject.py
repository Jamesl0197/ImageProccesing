# Title:    Cell Segmentation
# Module:   Image Processing - DT021A/4 - Dublin Institute of Technology   
# Author:   Safiah Sadeq, Christopher Byrne and James Lowe
# Date:     19/04/2018
#
# OBJECTIVE: 
# The objective of this project is to take in an image of a group of cells
# and give the user of the application the power to select a cell that is 
# of interest to them. Then isolate that cell from everything else in the image.

# PROCEDURE:
# First an image of a group of cells is read into the program. A denoising filter is 
# used to smooth out the original image to remove areas of noise. A binary mask is 
# created which outlines what is a cell and what is not a cell. With the areas that 
# are a cell having a value of 255 and background having a value of 0. A watershed 
# algorithm is applied using that mask and the original image which outlines the boundary
# of all the cells in the image. The user is shown the original image with a set of 
# instructions "Left Click to Segment -- Right Click to Return to Original Image". 
# When the user left clicks on a cell the coordinates of the that mouse click is taken.
# The coordinates are then used in the watershed algorithm mask to fill from those 
# coordinates to the boundary of the cell. This creates a mask that masks everything but 
# the cell that the user selected and the outline of each of the other cells. This mask 
# is then applied to the original image and will display the cell and the outline of each
# other cell. The user can right click to return to the original image or left click on a 
# different cell to segment that cell. The user may also press escape to exit.
 
# PSEUDOCODE:
# ....... START
# ....... ( Read in image )
# ....... ( Display image )				
# ....... ( Filter image using denoising filter )							
# ....... ( Create mask of cells )
# ....... ( Apply watershed to get borders )
# ....... ( While escape is not pressed)
# 	....... ( If right mouse button pressed down )
#		....... ( segment the cell selected )
#	....... ( If left mouse button pressed down )
# 		....... ( Display original image ) 	
#	....... ( If escape is pressed )
# 		....... ( Close while loop )
# ....... END

 
# import packages
import numpy as np
import cv2

# ----------------------------------- Functions ----------------------------------- #

#####################################################################################
# Function: 		Display - Displays image with border and instructions	  		#              
# 																					#
# Pseudocode:		....... ( Create border around the image )						#
#        			....... ( Place white text on top border )						#
#					....... ( Show image with border  )			 				    #
#																					#
# Calls: 			-																#
#																					#
# Called by:		Main , Segment() 												#
#																					#
# Input Parameters: displayImage													#
# 																					#
# Returns: 			none															#
#####################################################################################

def Display(displayImage):
		
	# Create border around the image 
	displayImage = cv2.copyMakeBorder(displayImage,40,40,40,40,cv2.BORDER_CONSTANT,(0,0,0))

	# Place white text on top border 
	cv2.putText(displayImage,'Left Click to Segment -- Right Click to Return to Original Image',(40,30), font, 1,(255,255,255),1,cv2.LINE_AA)

	# Show image with border 
	cv2.imshow('Cervical',displayImage)

#####################################################################################
# Function: 		FilterAndMask - Filters image and creates a mask 		  		#              
# 																					#
# Pseudocode:		....... ( Convert image to greyscale )							#
#        			....... ( Apply denoising filter )								#
#					....... ( Create mask by thresholding )			 			    #
#					....... ( Invert mask  )			 						    #
#					....... ( Return mask  )					 				    #
#																					#
# Calls: 			-																#
#																					#
# Called by:		Main 			 												#
#																					#
# Input Parameters: img																#
# 																					#
# Returns: 			binaryInvert													#
#####################################################################################
	
def FilterAndMask(img):
	
	# Convert image to greyscale and apply denoising filter  
	imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	imgGrayDenoise = cv2.fastNlMeansDenoising(imgGray,None,21,15,33)
	
	# Create mask 
	ret, binary = cv2.threshold(imgGrayDenoise, thresh = 131, maxval = 255, type = cv2.THRESH_BINARY)
	binaryInvert= cv2.bitwise_not(binary)
	
	return binaryInvert

#####################################################################################
# Function: 		Watershed - Finds the borders of the cells				  		#              
# 																					#
# Pseudocode:		....... ( Find definite background area (ie. not a cell) ) 		#
#					....... ( Find definite foreground area	(ie. is a cell) )		#
#					....... ( Find the unknown area (not sure if cell or background)# 
#					....... ( label markers for foreground )						#
#					....... ( Apply watershed )										#
#                   ....... ( Set the boundary colour to blue )						#
#																					#
# Calls: 			-																#
#																					#
# Called by:		Main															#
#																					#
# Input Parameters: mask,img														#
# 																					#
# Returns: 			img																#
# 																					#
# References: 		Docs.opencv.org. (2018). OpenCV: Image Segmentation with 		#
#					Watershed Algorithm. [online] Available at: 					#	
#					https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html #
#					[Accessed 12 Apr. 2018].										#
#####################################################################################
	
def Watershed(mask,img):

	# Find definite background area
	kernel = np.ones((5,5),np.uint8)
	opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 1)
	background = cv2.dilate(opening,kernel,iterations=3)
	

	# Find definite foreground area
	dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
	ret, foreground = cv2.threshold(dist_transform,0.06*dist_transform.max(),255,0)
	
	# Find the unknown region
	foreground = np.uint8(foreground)
	unknown = cv2.subtract(background,foreground)

	# Marker labelling
	ret, markers = cv2.connectedComponents(foreground)
	markers = markers+1
	markers[unknown==255] = 0

	# Apply Watershed 
	markers = cv2.watershed(img,markers)
	
	# Set the boundary colour to blue
	img[markers == -1] = [255,0,0]
	
	return img
	
#####################################################################################
# Function: 		Segment - Segments cell from background and other cells  		#              
# 																					#
# Pseudocode:		....... ( if left mouse button is pressed down: )				#
#						....... ( Take blue component of watershed image 			#
#								  and apply binary threshold leaving only boundary )#
#        				....... ( make copy of binary threshold image )				#
#						....... ( Using the coordinates of the mouse click 			#
#								  fill from that area on the boundary mask until 	#
#								  boundary is reached leaving a mask with cell of 	#
#								  interest and boundaries of the other cells.)	    #
#						....... ( Apply mask to original image )					#
#						....... ( Display resulting image )							#
#						....... ( set pixels in mask to 255 so it can be reused )	#
# 					....... ( if right mouse button is pressed down: )				#
# 						....... ( Display original image)							#
# Calls: 			Display()														#
#																					#
# Called by:		Main															#
#																					#
# Input Parameters: event , x , y , flags , param , watershedImg , mask				#
# 																					#
# Returns: 			none															#
#####################################################################################
	
def Segment(event,x,y,flags,param,): 
	if event == cv2.EVENT_LBUTTONDOWN:
		
		
		# Take blue component of Watershed image as it contains the border information
		# and create mask
		blue, green, red = cv2.split(watershedImg)
		ret,isolateMask = cv2.threshold(blue,254,255,cv2.THRESH_BINARY) 
		maskCopy = isolateMask.copy()
		
		# Use floodlill to fill the area of the mask containing the cell of interest 
		# NOTE: -40 is used on the x and y axis to take acount of the border
		h, w = isolateMask.shape[:2]
		maskZeros = np.zeros((h+2, w+2), np.uint8)
		cv2.floodFill(isolateMask, maskZeros, (x-40,y-40), 255);
		
		# Apply the isolateMask to the original image leaving the cell isolated (imgLonleyCell)
		# which outlines of his friends who are no longer there with a white background
		imgLonleyCell = cv2.bitwise_and(originalImage,originalImage,mask = isolateMask)
		imgLonleyCell[np.where((imgLonleyCell == [0,0,0]).all(axis = 2))] = [255,255,255]	

		Display(imgLonleyCell)

		# set all pixels in mask to 255 so it can be reused
		isolateMask[:,:] = 255

	if event == cv2.EVENT_RBUTTONDOWN:
		Display(originalImage)
	
# --------------------------------- End Functions -------------------------------- #
	
# ------------------------------------- Main ------------------------------------- #	

# Set font for text in GUI
font = cv2.FONT_HERSHEY_SIMPLEX

# Read in image and make copy
img = cv2.imread("cervical.jpg")
originalImage  = img.copy()

# Window set up
cv2.namedWindow('Cervical',500)
cv2.setMouseCallback('Cervical',Segment)

Display(img)
mask = FilterAndMask(img)
watershedImg = Watershed(mask,img)

# While loop waits for user input and breaks when escape is pressed
while(1):
    
    if cv2.waitKey(20) & 0xFF == 27:
	        break
	
cv2.destroyAllWindows()

# ----------------------------------- End Main ----------------------------------- #	

# ------------------------------------- End -------------------------------------- #
