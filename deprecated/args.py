import argparse
import os
from glob import glob


parser = argparse.ArgumentParser()
parser.add_argument('images', nargs='*', type=str, help='Image files')
args = parser.parse_args()
#args, unknownargs = parser.parse_known_args()

images = []
for image in args.images:
	image_path = os.path.abspath(os.path.expanduser(image))
	for i in glob(image):
		if os.path.isfile(i):
			images.append(i)

if len(images) == 0:
	print('No images provided.')
	exit()
else:
	print('Images to process: {}'.format(images))
