from PIL import Image
import math

#change to whatever image you want
im = Image.open("Chemistry-building-image.jpg")
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

#convert image to greyscale
for y in range(height):
    for x in range(width):
        r,g,b = im.getpixel((x,y))
        value = int((r+g+b) / 3)
        greyscale.append(value)

grey_image.putdata(greyscale)
grey_image.save("bw.jpg")

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

#combine gx_list and gy_list.
for y in range(height):
	for x in range(width):
		if x == 0 or x == width - 1 or y == 0 or y == height - 1:
			g_complete.append(0)
			continue
		x_value = gx_list[y*width + x]
		y_value = gy_list[y*width + x]
		value = int(math.sqrt(x_value*x_value + y_value*y_value))
		g_complete.append(value)

#scale the values to be in the range 0-255
for y in range(height):
    for x in range(width):
        value = (g_complete[y*width + x] / 1020) * 255
        edge.append(value)
edge_image.putdata(edge)
edge_image.save("edge.jpg")

#convert edge image to binary image
for y in range(height):
    for x in range(width):
    	if edge[y*width + x] < threshold:
    		binary.append(0)
    	else:
    		binary.append(1)
binary_image.putdata(binary)
binary_image.save("binary.jpg")

