'''
Assignment 2 : Image Enhancement and Filtering

Breno Cunha Queiroz - 11218991
Course SCC0251 - USP
26/04/2020 - semestre 3
'''
import numpy as np
import imageio
import math

###############################################################
########################### FUNCTIONS #########################
###############################################################

#------------ Bilateral Filter ------------#
def gaussian(x, sigma):
    return (1/(2*math.pi*sigma*sigma))*math.exp(-x*x/(2*sigma*sigma))

def bilateralFilter():
    global newImg
    global img
    # Filter size
    n = int(input())
    # Spatial
    s = float(input())
    # Range
    r = float(input())

    mid = int(n/2)

    # Filter coords
    cords = []
    for row in range(n):
        for col in range(n):
            dcol = -mid+col;
            drow = -mid+row;
            cords.append([drow,dcol])

    # Generate spatial component
    sg = np.zeros((n,n))
    for [drow, dcol] in cords:
        sg[drow][dcol] = gaussian(math.sqrt(dcol*dcol + drow*drow), s)

    for x,row in enumerate(refImg):
        for y,col in enumerate(row):
                If = 0 # New center pixel value
                Wp = 0 # Normalization factor
                Ic = float(refImg[x][y]) # Center pixel value
                for [frow, fcol] in cords:
                    Ii = 0
                    if x+frow>=0 and x+frow<len(refImg) and y+fcol>=0 and y+fcol<len(row):
                        Ii = float(refImg[x+frow][y+fcol]) # i pixel value
                    gri = gaussian(Ii-Ic, r)
                    wi = gri * sg[frow][fcol]
                    Wp = Wp + wi
                    If = If + wi*Ii
                If = If/Wp
                newImg[x][y] = If

#------------ Laplacian Filter ------------#
def laplacianFilter():
    global newImg
    global img
    c = float(input())
    kernel = int(input())

    k1 = [[0,-1,0],[-1,4,-1],[0,-1,0]]
    k2 = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]

    # Filter coords
    n = 3
    mid = int(n/2)
    coords = []
    for row in range(n):
        for col in range(n):
            dcol = -mid+col;
            drow = -mid+row;
            coords.append([drow,dcol])

    # 1 - Convolving the original image
    If = np.zeros(newImg.shape)
    for x,row in enumerate(If):
        for y,col in enumerate(row):
                Ifc = 0 # New center pixel value
                for [frow, fcol] in coords:
                    Ii = 0
                    if x+frow>=0 and x+frow<len(refImg) and y+fcol>=0 and y+fcol<len(row):
                        Ii = float(refImg[x+frow][y+fcol]) # i pixel value

                    if kernel == 1:
                        Ifc=Ifc+Ii*k1[frow+1][fcol+1]
                    elif kernel == 2:
                        Ifc=Ifc+Ii*k2[frow+1][fcol+1]

                If[x][y] = Ifc

    # 2 - Scaling filtered image
    IfMax = If.max()
    IfMin = If.min()

    for x,row in enumerate(If):
        for y,col in enumerate(row):
            If[x][y] = (If[x][y]-IfMin)*255/(IfMax-IfMin)

    # 3 - Add filtered image
    for x,row in enumerate(If):
        for y,col in enumerate(row):
            If[x][y] = c*If[x][y]+float(refImg[x][y])

    # 4 - Scaling final image
    IfMax = If.max()
    IfMin = If.min()

    for x,row in enumerate(newImg):
        for y,col in enumerate(row):
            newImg[x][y] = (If[x][y]-IfMin)*255/(IfMax-IfMin)

#------------ Vignette Filter ------------#
def vignetteFilter():
    global newImg
    global refImg
    r = float(input())# σrow
    c = float(input())# σcol

    [height, width] = refImg.shape

    # Create column and row vectors 
    rowVec = np.array([[gaussian(i-int(height/2), r)] for i in range(height)])
    colVec = np.array([[gaussian(i-int(width/2), c) for i in range(width)]])
    # Gen matrix 
    image = rowVec.dot(colVec)

    # Multiply matrix with reference image
    image = np.multiply(image, refImg)

    # Scaling final image
    imgMax = image.max()
    imgMin = image.min()
    for x,row in enumerate(image):
        for y,col in enumerate(row):
            image[x][y] = (image[x][y]-imgMin)*255/(imgMax-imgMin)

    # Save to image 
    newImg = image.astype(np.uint8)

def evaluate():
    global newImg
    global refImg
    diff = 0
    for x,row in enumerate(refImg):
        for y,col in enumerate(row):
            m = float(newImg[x][y])
            r = float(refImg[x][y])
            diff += np.power(m-r,2)
    print("{0:.4f}".format(np.sqrt(diff),4))

###############################################################
########################### MAIN CODE #########################
###############################################################

# Input file name
file = str(input()).rstrip()
# Read image
refImg = imageio.imread(file)
# Result image
newImg = imageio.imread(file)

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

