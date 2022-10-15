import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
# Unccoment to use with screen captures
# from screen_funcs import get_screen, screencap, resize_image

ftypes = [
	("JPG", "*.jpg;*.JPG;*.JPEG"), 
	("PNG", "*.png;*.PNG"),
	("GIF", "*.gif;*.GIF"),
	("All files", "*.*")
]

# default values
#lower_hsv = np.array([0, 0, 0])
#upper_hsv = np.array([179, 255, 255])
lower_hsv = np.array([179, 0, 216])
upper_hsv = np.array([180, 0, 136])


# Trackbar callback function
def nothing(x):
	update_hsvs()
	print(lower_hsv, upper_hsv)

# Get the current positions of all trackbars and update
# the global HSV values
def update_hsvs():
	global lower_hsv, upper_hsv
	
	# Update the global HSV values with the trackbar values
	lower_hsv = np.array([
		cv2.getTrackbarPos('Low H', 'Controls'),
		cv2.getTrackbarPos('Low S', 'Controls'),
		cv2.getTrackbarPos('Low V', 'Controls')
	], np.uint8)
		
	upper_hsv = np.array([
		cv2.getTrackbarPos('High H', 'Controls'),
		cv2.getTrackbarPos('High S', 'Controls'),
		cv2.getTrackbarPos('High V', 'Controls')
	], np.uint8)

LOAD_IMAGE_FROM_FILE = False
def main():
	image_src = None
	
	# Open dialog for reading the image file
	root = tk.Tk()
	root.withdraw() # hide the root window
	
	file_path = filedialog.askopenfilename(filetypes=ftypes)
	if not file_path:
		print("No file selected")
		return
		
	# Read the image
	image_src = cv2.imread(file_path)
	
	
	# Unccoment to use with screen captures
	# image_src = screencap(0, 0, *get_screen())
	
	# Create a window named 'Controls' for trackbar
	cv2.namedWindow('Controls', 2)
	
	#cv2.resizeWindow('Controls', 550, 10)
	cv2.resizeWindow('Controls', 500, 300)
	
	# Create trackbars for lower HSV values
	cv2.createTrackbar('Low H', 'Controls', lower_hsv[0], 179, nothing)
	cv2.createTrackbar('Low S', 'Controls', lower_hsv[1], 255, nothing)
	cv2.createTrackbar('Low V', 'Controls', lower_hsv[2], 255, nothing)
	
	# Create trackbars for upper HSV values
	cv2.createTrackbar('High H', 'Controls', upper_hsv[0], 179, nothing)
	cv2.createTrackbar('High S', 'Controls', upper_hsv[1], 255, nothing)
	cv2.createTrackbar('High V', 'Controls', upper_hsv[2], 255, nothing)
	
	while True:
		# Create the hsv from the bgr image
		image_hsv = cv2.cvtColor(image_src, cv2.COLOR_BGR2HSV)
		image_mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
		image_res = cv2.bitwise_and(image_src, image_src, mask=image_mask)
		
		# Show all the windows
		# cv2.imshow("BGR", image_src)
		# cv2.imshow("HSV", image_hsv)
		# cv2.imshow("Mask", image_mask)
		# add text to image
		
		# stack the mask, orginal frame and the filtered result
		stacked = np.hstack((
			image_src,
			cv2.cvtColor(image_mask, cv2.COLOR_GRAY2BGR),
			image_res
		))
		
		
		# Show this stacked frame at 40% of the size.
		# Uncomment below to resize the stacked images to 50% of the original size
		# cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.5, fy=0.5))
		cv2.imshow('Trackbars', stacked)
		
		# If the user presses ESC then exit the program
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

if __name__== '__main__':
	main()
