#!/usr/bin/env python3
''' audio thumbnailer script

	exit codes:
		1 - incorrect usage
		2 - Mutagen Error (tag parsing)
		3 - No embedded data
'''

import sys
from io import BytesIO
from urllib import request
from PIL import Image
from mutagen import File, MutagenError

DEFAULT_SIZE = 192

def get_img(filename, size=(DEFAULT_SIZE, DEFAULT_SIZE)):
	''' get cover from APIC frame and resize
			arguments:
				filename (string): path to source audio file
				size (tuple) : dimension of output image (w, h)
			returns:
				image (PIL.Image.Image)

	'''
	try:
		audio = File(filename)
	except MutagenError:
		sys.exit(2)
	image = None
	if audio:
		image = Image.open(BytesIO(audio.tags['APIC:'].data))
		image.thumbnail(size)
	return image

if __name__ == '__main__':
	# If we have 2 args
	if len(sys.argv) == 3:
		INPUT_FILE = request.url2pathname(sys.argv[1]).replace('file://', '')
		OUTPUT_FILE = request.url2pathname(sys.argv[2]).replace('file://', '')
		IMAGE = get_img(INPUT_FILE)
		IMAGE.save(OUTPUT_FILE, 'png') if IMAGE else sys.exit(3)
	sys.exit(1)
