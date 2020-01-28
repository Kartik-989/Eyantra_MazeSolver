
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1C of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ 4695 ]
# Author List:		[ Kartik]
# Filename:			task_1c.py
# Functions:		computeSum
# 					[ Comma separated list of functions in this file ]
# Global variables:	None
# 					[ List of global variables defined in this file ]


# Import necessary modules
import cv2
import numpy as np
import os
import sys


#############	You can import other modules here	#############
import matplotlib.pyplot as plt
import Load_Model
import tensorflow as tf


###########################  Global Vriables  ##########################
(h,w)=0,0
cell_size=40
digitvalue={}

####################################################################


def computeSum(img_file_path, shortestPath):

	"""
	Purpose:
	---
	the function takes file path of original image and shortest path as argument and returns
	list of digits in image, digits on path and sum of digits on path in the maze image

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Returns:
	---
	`digits_list` :	[ list ]
		list of all digits on image
	`digits_on_path` :	[ list ]
		list of digits adjacent to the path from initial_point to final_point
	`sum_of_digits_on_path` :	[ int ]
		sum of digits on path

	Example call:
	---
	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

	"""

	digits_list = []
	digits_on_path = []
	sum_of_digits_on_path = 0

	#############  Add your Code here   ###############
	global h,w
	global cell_size 
	global digitvalue
	shortestPath=shortestPath
	no_cells_height=10
	no_cells_width=10
	digitcell=[]
	cellon_path=[]
	digitvalue={}
	h,w=0,0
	i,j=0,0
	d=check = 0
	image=cv2.imread(img_file_path)
	grey_img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # binary to grey
	
	threshold,img=cv2.threshold(grey_img,120,255,cv2.THRESH_BINARY_INV)
	
	############### finding cells wwith digit  #################

	while(i<no_cells_height):
		while(j<no_cells_width):
			m=np.mean(img[(i+1)*cell_size-cell_size+4:(i+1)*cell_size-4,(j+1)*cell_size-cell_size+4:(j+1)*cell_size-4])
			if(m>5):
				digitcell.append((i,j))
			j+=1
		j=0
		i+=1

	################### classify  digit by model ############ 
	while d<len(digitcell):
		(a,b)=digitcell[d]
		d+=1
		simg=img[(a+1)*cell_size-cell_size+4:(a+1)*cell_size-4,(b+1)*cell_size-cell_size+4:(b+1)*cell_size-4]

		#plt.imshow(simg, cmap="gray") # Import the image
		#plt.show()
		simg=cv2.resize(simg,(28,28),interpolation=cv2.INTER_AREA)
	
		threshold,simg=cv2.threshold(simg,120,255,cv2.THRESH_BINARY)
		simg = tf.keras.utils.normalize(simg, axis=1)
		#plt.imshow(simg, cmap="gray") # Import the image
		#plt.show()
		#print(simg.shape)
		image=simg.reshape(-1,28,28,1)
		digit=(Load_Model.predict(image))
		#print(digit,d)
		digitvalue[(a,b)]=digit
	#print(digitvalue)
	###################3 DIGIT LIST READY #########################
	for x in digitvalue.values():
		digits_list.append(int(x))	
	#print(digits_list)
	#print(digitcell)
	############## FINDING CELLS NEAR SHORTEST PATH ########
	while(check<len(digitcell)):
		(h,w)=digitcell[check]
		check+=1
		if incw(img)==1:
			#print("y1")
			w+=1
			if search(h,w,shortestPath)==1:
				#print("yrrr")
				cellon_path.append((h,w-1))
			w-=1
		if decw(img)==1:
			#print("y2")
			w-=1
			if search(h,w,shortestPath)==1:
				#print("yrrr")
				cellon_path.append((h,w+1))
			w+=1
		if inch(img)==1:
			#print("y3")
			h+=1
			if search(h,w,shortestPath)==1 :
				#print("yrrr")
				cellon_path.append((h-1,w))
			h-=1
		if dech(img)==1:
			#print("y4")
			h-=1
			if search(h,w,shortestPath)==1:
				#print("yrrr")
				cellon_path.append((h+1,w))
			h+=1
		
	#print(cellon_path)


	############## GETTING READY DIGITS ON PATH	############

	z=0
	while z<len(cellon_path):
		item=cellon_path[z]
		value=findValue(item)
		
		if value!=0:
			digits_on_path.append(int(value))
		z+=1




	############ SUM OF DIGIT NEAR SHORTEST PATH ############
	
	sum_of_digits_on_path=int(sum(digits_on_path))
	
	###################################################

	return digits_list, digits_on_path, sum_of_digits_on_path


#############	You can add other helper functions here		#############


########## check width is increaseble OR there is a wall #############
def incw(img) :
	x=np.mean(img[(h+1)*cell_size-cell_size:(h+1)*cell_size,(w+1)*cell_size-2:(w+1)*cell_size])  # w inc
	if x>100:
		return 0
	else :
		return 1
    
        	
################# check width of maze is decreasable OR there is a wall #################
def decw (img):
    x=np.mean(img[(h+1)*cell_size-cell_size:(h+1)*cell_size,(w+1)*cell_size-cell_size:(w+1)*cell_size-(cell_size-2)]) #w dec
    if x>100:
        return 0
    else :
        return 1
	
################### check hieght of maze is increasable OR there is a wall ##############
def inch (img):
    x=np.mean(img[(h+1)*cell_size-2:(h+1)*cell_size,(w+1)*cell_size-cell_size:(w+1)*cell_size]) #h inc
    if x>100:
        return 0
    else :
        return 1 
############### check hieght of maze is decreasable OR there is a wall ##################3
def dech (img):
    x=np.mean(img[(h+1)*cell_size-cell_size:(h+1)*cell_size-(cell_size-2),(w+1)*cell_size-cell_size:(w+1)*cell_size]) #h decc
    if x>100:
        return 0
    else :
        return 1
############# search cell in shortest path ##########
def search(h,w,shortestPath):
	for i in range(len(shortestPath)):
		if shortestPath[i]==(h,w):
			return 1
	return 0

########### find value in cells on path ############

def findValue(item):
    for key,value in digitvalue.items():
        if item==key :
            return value
    return 0

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling computeSum
# 					function, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1c_images' folder or not

if __name__ != '__main__':
	
	curr_dir_path = os.getcwd()

	# Importing task_1a and image_enhancer script
	try:

		task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
		sys.path.append(task_1a_dir_path)

		import task_1a
		import image_enhancer

	except Exception as e:

		print('\ntask_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
		exit()

if __name__ == '__main__':
	
	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1c_images/'				# path to directory of 'task_1c_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	# Importing task_1a and image_enhancer script
	try:

		task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
		sys.path.append(task_1a_dir_path)

		import task_1a
		import image_enhancer

	except Exception as e:

		print('\n[ERROR] task_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
		exit()

	# modify the task_1a.CELL_SIZE to 40 since maze images
	# in task_1c_images folder have cell size of 40 pixels
	task_1a.CELL_SIZE = 40

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = task_1a.readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()

	
	no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
	no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

	print('\nDigits in the image = ', digits_list)
	print('\nDigits on shortest path in the image = ', digits_on_path)
	print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

	print('\n============================================')

	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = task_1a.readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()

			
			no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
			no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

			digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

			print('\nDigits in the image = ', digits_list)
			print('\nDigits on shortest path in the image = ', digits_on_path)
			print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	else:

		print('')


