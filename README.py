# Title:    Cell Segmentation
# Module:   Image Processing - DT021A/4 - Dublin Institute of Technology   
# Author:   Safiah Sadeq, Christopher Byrne and James Lowe
# Date:     19/04/2018
# 
#
# OBJECTIVE: 
# The objective of this project is to take in an image of a group of cells
# and give the user of the application the power to select a cell that is 
# of interest to them. Then isolate that cell from everything else in the image.
#
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
