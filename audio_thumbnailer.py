#!/usr/bin/env python3
''' audio thumbnailer script

	exit codes:
		1 - incorrect usage
		2 - Mutagen Error (tag parsing)
		3 - No embedded data
'''

import sys
from io import BytesIO
from PIL import Image
from mutagen import File, MutagenError

DEFAULT_SIZE = 300
# 1 - top left, 2 - top right, 3 - bottom right, 4 - bottom left
#^ CORNER = 1
#^ CORNER = 2
CORNER = 3
#^ COURNER = 4

def usage():
	''' prints usage information
	'''
	print("Usage:\n audiotag-thumbnailer [OPTION...] <input> <output> - Audio File Thumbnailer")
	print("\nHelp Options:\n\t-h, --help\t\tShow help options")
	print("\nApplication Options:\n\t-s=SIZE ,--size=SIZE")
	print("\t-o=OVERLAY, --overlay=OVERLAY\t\tPath to overlay image")
	# print("\t-c=CORNER, --corner=CORNER\t\tCorner number {1,2,3,4}")

def paste_overlay(image, overlay, corner):
	''' calculates offset based on corner number and pastes overlay on image
			arguments:
				image (PIL.Image.Image) : cover image
				overlay (PIL.IMage.Image) : overlay
				corner (int) : x in {1, 2, 3, 4}
								1 - top left
								2 - top right
								3 - bottom right
								4 - bottom left
	'''
	offset = None
	if corner == 1:
		offset = (0, 0, overlay.size[0], overlay.size[1])
	elif corner == 2:
		offset = (image.size[0] - overlay.size[0], 0, image.size[0], overlay.size[1])
	elif corner == 3:
		offset = (0, image.size[1] - overlay.size[0], overlay.size[0], image.size[1])
	elif corner == 4:
		offset = (image.size[0] - overlay.size[0], \
			image.size[1] - overlay.size[0], \
			image.size[0], image.size[1])
	image.paste(overlay, offset, overlay)

def get_img(filename, size=DEFAULT_SIZE, overlay=None):
	''' gets cover from APIC frame and resize
			arguments:
				filename (string): path to source audio file
				size (int) : width of output image
								height is calculated to maintain aspect ratio
				overlay (string) : path to the overlay file
										the overlay is copied onto the image
			returns:
				image (PIL.Image.Image)
	'''
	try:
		audio = File(filename)
	except MutagenError:
		sys.exit(2)
	image = None
	if audio:
		try:
			image = Image.open(BytesIO(audio.tags['APIC:'].data))
			image.thumbnail((size, int(image.size[0]/image.size[1])*size), Image.BICUBIC)
		except KeyError:
			sys.exit(3)
		if image:
			if overlay:
				orlay = Image.open(overlay)
				orlay.thumbnail((int(image.size[0]/4)\
					, int(image.size[0]/image.size[1])*(size/4)), Image.BICUBIC)
				paste_overlay(image, orlay, CORNER)
		else:
			sys.exit(3)
	return image

if __name__ == '__main__':
	ARGC = 3
	SIZE = None
	INPUT_FILE = None
	OUTPUT_FILE = None
	OVERLAY = None
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '-h' or sys.argv[i] == '--help':
			usage()
			sys.exit(0)
		elif (sys.argv[i].split("=")[0] == "--size" or \
			sys.argv[i].split("=")[0] == "-s") and \
				len(sys.argv[i].split("=")) == 2:
			SIZE = sys.argv[i].split("=")
			try:
				SIZE = int(SIZE[1])
			except ValueError as ase:
				print("Cannot parse integer value \'{}\' for \'{}\'".format(SIZE[1], SIZE[0]))
				usage()
				sys.exit(1)
		elif (sys.argv[i].split("=")[0] == "--overlay" or \
			sys.argv[i].split("=")[0] == "-o") and \
				len(sys.argv[i].split("=")) == 2:
			OVERLAY = sys.argv[i].split("=")[1]
		elif not INPUT_FILE:
			INPUT_FILE = sys.argv[i].replace("file://", "")
		elif not OUTPUT_FILE:
			OUTPUT_FILE = sys.argv[i].replace("file://", "")

	ARGC += 1 if SIZE else 0
	ARGC += 1 if OVERLAY else 0

	if len(sys.argv) == ARGC:
		if OUTPUT_FILE.split(".")[-1] == "png":
			get_img(INPUT_FILE, SIZE, overlay=OVERLAY).save(OUTPUT_FILE, "png")
		elif OUTPUT_FILE.split(".")[-1] == "jpg" or OUTPUT_FILE.split(".")[-1] == "jpeg":
			get_img(INPUT_FILE, SIZE, overlay=OVERLAY).save(OUTPUT_FILE, "jpeg")
		else:
			get_img(INPUT_FILE, SIZE, overlay=OVERLAY).save(OUTPUT_FILE + ".png", "png")
	else:
		usage()
		sys.exit(1)
