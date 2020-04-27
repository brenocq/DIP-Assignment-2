'''
Assignment 2 : Image Enhancement and Filtering

Breno Cunha Queiroz - 11218991
Course SCC0251 - USP
26/04/2020 - semestre 3
'''
import numpy as np
import imageio

###############################################################
########################### FUNCTIONS #########################
###############################################################

def bilateralFilter():
    global newImg
    global img
    # Filter size
    n = int(input())
    # Spatial
    s = float(input())
    # Range
    r = float(input())

def laplacianFilter():
    global newImg
    global img
    c = float(input())
    kernel = int(input())

def vignetteFilter():
    global newImg
    global img
    row = float(input())
    col = float(input())

def evaluate():
    global newImg
    global img
    diff = 0
    for x,row in enumerate(img):
        for y,col in enumerate(row):
            m = float(newImg[x][y])
            r = float(img[x][y])
            diff += np.power(m-r,2)
    print("{0:.4f}".format(np.sqrt(diff),4))

###############################################################
########################### MAIN CODE #########################
###############################################################

# Input file name
file = str(input()).rstrip()
# Read image
refImg = imageio.imread("../images/"+file)
# Result image
newImg = imageio.imread("../images/"+file)

# Method 
M = int(input())
# Save file?
S = int(input())

# Run selected transformation
if M == 1:
    bilateralFilter()
elif M == 2:
    laplacianFilter()
elif M == 3:
    vignetteFilter()

# Show image result
evaluate()

# Save image
if S == 1:
    imageio.imwrite("output_img.png",newImg)

