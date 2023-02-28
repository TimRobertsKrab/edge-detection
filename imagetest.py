from PIL import Image
import math
import sys

#Command line argument to be the name of the image file
name = sys.argv[1]
try:
    im = Image.open(name)
except FileNotFoundError:
    print("No file")
    exit(0)
# Obtains the name of the file without the file extension
name = name.split(".")[0]

width, height = im.size
grey_image = Image.new('L',(width,height))
edge_image = Image.new('L',(width,height))
binary_image = Image.new('1',(width,height))
threshold = 50
greyscale = []
edge = []
binary = []
gx_list = []
gy_list = []
g_complete = []

#The max value in g_complete will be 255 * sqrt(20)
g_complete_scale = 2*math.sqrt(5)

#convert image to greyscale
for y in range(height):
    for x in range(width):
        r,g,b = im.getpixel((x,y))
        value = int((r+g+b) / 3)
        greyscale.append(value)

grey_image.putdata(greyscale)
grey_image.save(name + "-bw.jpg")

#run a sobel filter across the greyscale image.
#output edges across the horizontal into gx_list.
#output edges across the vertical into gy_list.
for y in range(height):
    for x in range(width):
        if x == 0 or x == width - 1 or y == 0 or y == height - 1:
            gx_list.append(0)
            gy_list.append(0)
            continue
        gx_list.append(grey_image.getpixel((x-1,y-1)) \
		- grey_image.getpixel((x+1,y-1)) \
		+ 2 * grey_image.getpixel((x-1,y)) \
		- 2 * grey_image.getpixel((x+1,y)) \
		+ grey_image.getpixel((x-1,y+1)) \
		- grey_image.getpixel((x+1,y+1)))
        gy_list.append(grey_image.getpixel((x-1,y-1)) \
		+ 2 * grey_image.getpixel((x,y-1)) \
		+ grey_image.getpixel((x+1,y-1)) \
		- grey_image.getpixel((x-1,y+1)) \
		- 2 * grey_image.getpixel((x,y+1)) \
		- grey_image.getpixel((x+1,y+1)))
x_value = 0
y_value = 0

#Combine gx_list and gy_list
for x_edge,y_edge in zip(gx_list,gy_list):
	if x_edge == 0 or y_edge == 0:
		g_complete.append(0)
		continue
	value = int(math.sqrt(x_edge*x_edge + y_edge*y_edge))
	g_complete.append(value)

#Scale g_complete to be in the range 0-255
for edge_full in g_complete:
	#value = (edge_full / 1020) * 255
	value = edge_full / g_complete_scale 
	edge.append(value)
edge_image.putdata(edge)
edge_image.save(name+"-edge.jpg")

#Compute binary image
for pixel in edge:
    if pixel < threshold:
        binary.append(0)
    else:
        binary.append(1)

binary_image.putdata(binary)
binary_image.save(name+"-binary.jpg")


