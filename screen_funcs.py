import cv2
import pyautogui
from PIL import ImageGrab


# Get the screen resolution
def get_screen():
	return pyautogui.size()

# Get the screenshot for the given region
def screencap(x1, y1, x2, y2):
	img = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	return img

# Resize the image to a percentile of the original 
# size
def resize_image(img, scale):
	width, height = int(img.shape[1] * scale), int(img.shape[0] * scale)
	dim = (width, height)
	return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
