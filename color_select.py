import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
# Unccoment to use with screen captures
# from screen_funcs import get_screen, screencap, resize_image


image_hsv = None
# default values
pixel = (0, 0, 0)
ftypes = [
	("JPG", "*.jpg;*.JPG;*.JPEG"), 
	("PNG", "*.png;*.PNG"),
	("GIF", "*.gif;*.GIF"),
	("All files", "*.*")
]

def check_boundaries(value, tolerance:int, sat_and_brightness=False, upper=False) -> int:
	"""
	Checks if the value is within the boundaries of the range.
	
	Parameters
	----------
	value : int
		The value to check.
		
	tolerance : int
		The tolerance for the value.
		
	sat_and_brightness : bool
		The range to check.
		
		True = Saturation and brightness.
		False = Hue.
		
	upper : bool
		True for upper and False for lower.
		
	Returns
	-------
	int
		The value within the boundaries.
	"""
	
	boundary = 0
	
	if sat_and_brightness:
		# set the boundary for saturation and value
		boundary = 255
	else:
		# set the boundary for hue
		boundary = 179
		
	if (value + tolerance) > boundary:
		value = boundary
	elif (value - tolerance) < 0:
		value = 0
	else:
		if upper == True:
			value = value + tolerance
		else:
			value = value - tolerance
			
	return value

def pick_color(event, x, y, flags, param) -> None:
	"""
	Callback function for the mouse click event.
	
	Parameters
	----------
	event : int
		The event type.
		
	x : int
		The x coordinate of the mouse.
		
	y : int
		The y coordinate of the mouse.
		
	flags : int
		The flags.
		
	param : int
		The parameter.
		
	Returns
	-------
	None
	"""
	if event == cv2.EVENT_LBUTTONDOWN:
		pixel = image_hsv[y, x]
		
		# Hue, saturation, and value (brightness) ranges; tolerance could be adjusted.
		# Set range = 0 for hue and range = 1 for saturation and brightness
		# set upper_or_lower = 1 for upper and upper_or_lower = 0 for lower
		hue_upper = check_boundaries(pixel[0], tolerance=10, sat_and_brightness=False, upper=True)
		hue_lower = check_boundaries(pixel[0], tolerance=10, sat_and_brightness=False, upper=False)
		saturation_upper = check_boundaries(pixel[1], tolerance=10, sat_and_brightness=True, upper=True)
		saturation_lower = check_boundaries(pixel[1], tolerance=10, sat_and_brightness=True, upper=False)
		value_upper = check_boundaries(pixel[2], tolerance=40, sat_and_brightness=True, upper=True)
		value_lower = check_boundaries(pixel[2], tolerance=40, sat_and_brightness=True, upper=False)
		
		upper =  np.array([hue_upper, saturation_upper, value_upper])
		lower =  np.array([hue_lower, saturation_lower, value_lower])
		
		print(pixel)
		print(upper, lower)
		
		# A monochrome mask for getting a better vision over the colors 
		image_mask = cv2.inRange(image_hsv, lower, upper)
		cv2.imshow("Mask", image_mask)

def main():
	global image_hsv, pixel
	
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
	
	cv2.imshow("BGR", image_src)
	
	# Create the hsv from the bgr image
	image_hsv = cv2.cvtColor(image_src, cv2.COLOR_BGR2HSV)
	cv2.imshow("HSV", image_hsv)
	
	# Callback function
	cv2.setMouseCallback("HSV", pick_color)
	#cv2.setMouseCallback("BGR", pick_color)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__== '__main__':
	main()
