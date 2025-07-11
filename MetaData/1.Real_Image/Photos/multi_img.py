import cv2
import imutils
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class ColorLabeler:
    def __init__(self):
        # initialize the colors dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255)})
        # allocate memory for the L*a*b* image, then initialize
        # the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []
        # loop over the colors dictionary
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)
        # convert the L*a*b* array from the RGB color space
        # to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
		
    def label(self, image, c):
        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        # initialize the minimum distance found thus far
        minDist = (np.inf, None)
        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)
            # if the distance is smaller than the current distance,
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)
        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]


class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, c, espilon):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, espilon * peri, True)
				# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
		elif len(approx) == 6:
			shape = "hexagon"
		elif len(approx) == 7:
			shape = "heptagon"                        
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
		# return the name of the shape
		return shape,approx


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale,scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def nothing(x) :
    pass

def imageCenter(image) : 
    (h,w) = image.shape[:2]
    cv2.circle(image, (w//2, h//2), 7, (255, 0, 0), -1) #where w//2, h//2 are the required frame/image centeroid's XYcoordinates.

def pixel_color(img,x,y) :
    imgRGB = cv2.imread(img)
    imgHSV = cv2.cvtColor(imgRGB,cv2.COLOR_BGR2HSV)
    #in order B G R
    #img[row,column], row means y, column means x
    # b,g,r = imgRGB[int(x),int(y)]
    # print(r,g,b)
    h,s,v = imgHSV[int(y),int(x)]
    # print(h,s,v)

    #red
    redLower = np.array([136,87,111], np.uint8)
    redUpper = np.array([180,255,255], np.uint8)


    #green
    # greenLower = np.array([25,40,72], np.uint8)
    # greenUpper = np.array([102,255,255], np.uint8)

    greenLower = np.array([15, 40, 50])
    greenUpper = np.array([179,116,104], np.uint8)    

    # greenLower = np.array([35, 40, 60])
    # greenUpper = np.array([85, 255, 255])    

    #blue
    blueLower = np.array([94,80,2], np.uint8)
    blueUpper = np.array([120,255,255], np.uint8)
    
    #yellow
    yellowLower = np.array([23,59,119], np.uint8)
    yellowUpper = np.array([54,255,255], np.uint8)

    #orange
    orangeLower = np.array([0,50,80], np.uint8)
    orangeUpper = np.array([20,255,255], np.uint8)    

    #purple
    purpleLower = np.array([130,80,80], np.uint8)
    purpleUpper = np.array([150,255,255], np.uint8)        

    redCheck = all([h,s,v] >= redLower) and all([h,s,v] <= redUpper)
    greenCheck = all([h,s,v] >= greenLower) and all([h,s,v] <= greenUpper)
    blueCheck = all([h,s,v] >= blueLower) and all([h,s,v] <= blueUpper)
    yellowCheck = all([h,s,v] >= yellowLower) and all([h,s,v] <= yellowUpper)
    orangeCheck = all([h,s,v] >= orangeLower) and all([h,s,v] <= orangeUpper)
    purpleCheck = all([h,s,v] >= purpleLower) and all([h,s,v] <= purpleUpper)            

    if redCheck == 1:
        return "Red"
    elif greenCheck == 1:
        return "Green"
    elif blueCheck == 1:
        return "Blue"
    elif yellowCheck == 1:
         return "Yellow"
    elif orangeCheck == 1:
         return "Orange"
    elif purpleCheck == 1:
         return "Purple"
    else :
        return "No color detected"
    
    return "No color detected"

def adjustBrightness(img, factor = 1.2):
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(imgHsv)
    v = np.clip(v*factor, a_min = 0, a_max = 255).astype(np.uint8)
    imgHsv = cv2.merge([h,s,v])
    return cv2.cvtColor(imgHsv,cv2.COLOR_HSV2BGR)

def ObjectLabeler(shape, color):
    if (color == "Green") and (shape == "circle"):
        return "Tree"
    elif (shape == "square") or (shape == "rectangle") or (shape == "pentagon") or ((shape == "hexagon")):
        return "House"
    else :
        return "Undefined Object"
    
    return "Undefined Object"


def reduce_shadow(image,threshold_darkpixel=65,kernel_size=11,):

    kernel_size=11
    total_pixel_in_kernel = kernel_size*kernel_size
    Eighty_percent_kernel = int(total_pixel_in_kernel*0.8)
    gr_pixel_in_total = 0
    half_size_kernel = int((kernel_size-1)/2)
    found_grkernel = 0
    
    #create a storage for ground kernel
    kernel_blue = np.zeros((kernel_size,kernel_size))
    kernel_red = np.zeros((kernel_size,kernel_size))
    kernel_green = np.zeros((kernel_size,kernel_size))

    kernel_copy = cv2.merge([kernel_blue,kernel_red,kernel_green])

    # Convert to LAB and split channels
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)

    Blue,Green,Red = cv2.split(image)
 
    height, width, _ = image.shape 
    
    ground_mark = np.zeros((height, width))

    thres_hold  = np.percentile(L, 15)

    low_thresHold = np.percentile(L, 30)
    high_thresHold = np.percentile(L,80)



    for j in range(0, height) :
        for i in range(0, width) :
            if L[j,i] > low_thresHold and L[j,i] < high_thresHold:
                #mark for background pixel
                ground_mark[j,i] = 1

                
    #copy kernel
    for y in range(0+half_size_kernel,height-half_size_kernel+1,1):
        for x in range(0+half_size_kernel,width-half_size_kernel+1,1):
            #figure out the pixel that we think maybe back-ground pixel
            if ground_mark[y,x] == 1 :
                #check region around back ground pixel
                for j in range(y-half_size_kernel,y+half_size_kernel,1):
                    for i in range(x-half_size_kernel,x+half_size_kernel,1):
                        if ground_mark[y,x] == 1 :
                            gr_pixel_in_total = gr_pixel_in_total + 1

                if gr_pixel_in_total > Eighty_percent_kernel :
                    #this kernel is back-ground kernel
                    #we will copy this kernel
                    found_grkernel = 1
                    cnt_col = 0
                    cnt_row = 0
                    for j in range(y-half_size_kernel,y+half_size_kernel): 
                        cnt_col = 0        
                        for i in range(x-half_size_kernel,x+half_size_kernel):
                            kernel_copy[cnt_row,cnt_col] = image[j,i]
                            cnt_col = cnt_col + 1
                        cnt_row = cnt_row + 1
            if found_grkernel == 1:
                gr_pixel_in_total = 0
                cnt_row = 0
                cnt_col = 0
                break
        if found_grkernel == 1:
            break

    for j in range(0, height) :
        for i in range(0, width) :
            if L[j,i] < thres_hold :

                total_color = Blue[j,i] + Green[j,i] + Red[j,i]

                if total_color < 30 :
                    Blue[j,i] = Blue[j,i]*6
                    Green[j,i] = Green[j,i]*6
                    Red[j,i] = Red[j,i]*6
                elif total_color >= 30 and total_color < 60 :
                    Blue[j,i] = Blue[j,i]*5
                    Green[j,i] = Green[j,i]*5
                    Red[j,i] = Red[j,i]*5
                elif total_color >= 60 and total_color < 90 :
                    Blue[j,i] = Blue[j,i]*4
                    Green[j,i] = Green[j,i]*4
                    Red[j,i] = Red[j,i]*4
                elif total_color >= 90 and total_color < 150 :
                    Blue[j,i] = Blue[j,i]*1.5
                    Green[j,i] = Green[j,i]*1.5
                    Red[j,i] = Red[j,i]*1.5
            total_color = 0




    new_img = cv2.merge([Blue,Green,Red])

    # return new image
    return new_img

# With photos who includes complex backgr, but color difference between backgr and object is clear. 
# We can use this func to remove back-gr.
# Not effective with tooo bright or too dark photos 
def backgr_removal(image,threshold_gr=50,kernel_size=11):

    total_pixel_in_kernel = kernel_size*kernel_size
    Eighty_percent_kernel = int(total_pixel_in_kernel*0.8)
    gr_pixel_in_total = 0
    half_size_kernel = int((kernel_size-1)/2)
    # Convert image from BGR to HSV
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract the all channels from hsv
    h,s,v_channel = cv2.split(hsv_img)
    height, width, _ = hsv_img.shape

    #run thourgh all image
    for y in range(0+half_size_kernel,height-half_size_kernel+1,1):
        for x in range(0+half_size_kernel,width-half_size_kernel+1,1):
            #find a dark pixel
            if h[y,x] < threshold_gr :
                
                #check dark region around dark pixel
                for j in range(y-half_size_kernel,y+half_size_kernel,1):
                    for i in range(x-half_size_kernel,x+half_size_kernel,1):
                        if h[j,i] < threshold_gr :
                            gr_pixel_in_total = gr_pixel_in_total + 1
                
                if gr_pixel_in_total > Eighty_percent_kernel :
                    #change the brightness of dark region
                    for j in range(y-half_size_kernel,y+half_size_kernel):
                        for i in range(x-half_size_kernel,x+half_size_kernel):
                            image[j,i] = [255,255,255]
            gr_pixel_in_total = 0


    # return new image
    return image


#from the coodination potision of object, we calculate the angle between
#2 vectors, first vector is drone towards east,
#second vector is drone toward object as trigonomectric circle.
def PositionDetector(x,y):
    if x == 0 :
        #north    
        if y > 0 :
            tanA = 99999
        #south
        elif y < 0 :
            tanA = -99999
        #center of photo
        else :
            tanA = 100000
    else :
        tanA = float(y/x)
    return tanA  

def LightBalance(image) :
     image = cv2.equalizeHist(image)
     return image

#create trackbar for canny edge detection threshold
cv2.namedWindow("Parameters")
cv2.createTrackbar("ThresLow","Parameters", 45, 255, nothing)
cv2.createTrackbar("ThresHigh","Parameters", 164, 255, nothing)

#create trackbar for kernel
cv2.createTrackbar("kernel va1", "Parameters", 3, 10, nothing)
cv2.createTrackbar("kernel va2", "Parameters", 3, 10, nothing)

#create trackbar for espilon
cv2.createTrackbar("Espilonx10000","Parameters",0,1200,nothing)

#create trackbar for contour Area
cv2.createTrackbar("AreaMin","Parameters",500,5000,nothing)
cv2.createTrackbar("AreaMax","Parameters",2500,10000,nothing)

#create trackbar for Filter
cv2.createTrackbar("Spatial Window","Parameters",45,100,nothing)
cv2.createTrackbar("Color Window","Parameters",60,100,nothing)

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

fileName = "12.png"

image = cv2.imread(fileName)
imageOrigin = image.copy()

# image = reduce_shadow(image)
#open a file to write results
file = open("output.txt","a")

#adjust brightness
image = adjustBrightness(image)

#get two first value of img.shape array
(h,w) = image.shape[:2]

#first parameter of this filter is spatial window radius
#If sp is small, only nearby pixels affect the result — 
#   so smoothing is localized.
#If sp is large, even pixels farther away 
#   (but with similar color) can be grouped — 
#       leading to larger smoothed regions.
# Large sp parameter creates heavy calculation, slow calculation
#   ,so the computer could take a lot of time to calculate it.
#       Even the program crashes.
BackGrRmv_Or_ShiftFil = 1
if (BackGrRmv_Or_ShiftFil == 0) :
    filtered = cv2.pyrMeanShiftFiltering(image, 30, 45)   
else : 
    filtered = backgr_removal(image) 

# applying different thresholding : START
# techniques on the input image 
gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

#Historical equalization
gray = LightBalance(gray)


#loop for control contour detection and edge detection
while True :
    imgContour = image.copy()


    


    #create variables for Filter Trackbars
    SP = cv2.getTrackbarPos("Spatial Window","Parameters")
    SR = cv2.getTrackbarPos("Color Window","Parameters")

    # thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
    #                                         cv2.THRESH_BINARY, 199, 5) 
    
    # thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                         cv2.THRESH_BINARY, 199, 5)     
    # applying different thresholding : END


    #create variable for trackbar
    ThresLow = cv2.getTrackbarPos("ThresLow","Parameters")
    ThresHigh = cv2.getTrackbarPos("ThresHigh","Parameters")
    
    #canny edge detection
    edges1 = cv2.Canny(image=filtered,threshold1 = ThresLow,threshold2 = ThresHigh)

    #closing image :: END
    #create variable for kernel trackbar
    Kernel_Trackbar1 = cv2.getTrackbarPos("kernel va1", "Parameters")
    Kernel_Trackbar2 = cv2.getTrackbarPos("kernel va2", "Parameters")    
    
    kernel = np.ones((Kernel_Trackbar1,Kernel_Trackbar2), np.uint8)
    closing = cv2.morphologyEx(edges1, cv2.MORPH_CLOSE, kernel, iterations = 1)
    
    
    # find contours in the thresholded image
    cnts,hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    
    # initialize the shape detector and color labeler
    sd = ShapeDetector()
    cl = ColorLabeler()

    # loop over the contours
    for c in cnts:
        
        #calculate contour area for removing small contour(noise)
        area = cv2.contourArea(c)
        areaMin = cv2.getTrackbarPos("AreaMin","Parameters")

        areaMax = cv2.getTrackbarPos("AreaMax","Parameters")
        
        Espilonx10000 = cv2.getTrackbarPos("Espilonx10000","Parameters")
        espilon = Espilonx10000/10000

        #put contour detection in a specific condition

        #check contour is closed or not, but not effective with complicated photos.
        # if cv2.isContourConvex(c):

        if (area > areaMin and area < areaMax): # and area < areaMax :
            # compute the center of the contour
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]) )
            cY = int((M["m01"] / M["m00"]) )

            #Real position compare to drone
            rX = cX - w/2
            rY = h/2 - cY

            # detect the shape of the contour and label the color
            (shape,approx) = sd.detect(c,espilon)
            
            color = pixel_color(fileName,cX,cY)

            #object labeler
            object = ObjectLabeler(shape,color)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape and labeled
            # color on the image
            c = c.astype("float")
            c = c.astype("int")
            text = "{} {}".format(color, shape)
            cv2.drawContours(imgContour, [approx], -1, (0, 255, 0), 2)

            cv2.putText(imgContour, text, (cX, cY),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)

            #Print the real coordination offset with top-left corner.
            # cv2.putText(imgContour,"({},{})".format(cX,cY),(cX, cY+40),
            # 	cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 255, 0), 2)

            #Print the new coordination offset with center of image.
            cv2.putText(imgContour,"({},{})".format(rX,rY),(cX, cY+20),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)
            
            cv2.putText(imgContour, object, (cX, cY+40),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)

            cv2.putText(imgContour, " tanA={:.2f}".format(PositionDetector(rX,rY)), (cX, cY+60),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2) 

    # show the output image

    imgStack = stackImages(1,([imageOrigin,gray,filtered],[edges1,closing,imgContour]))

    cv2.imshow("ImageStack", imgStack)
    cv2.imshow("Image",imgContour)

    # cv2.imshow("MeanC",thresh1)
    # cv2.imshow("Gaussian",thresh2)

    cv2.waitKey(300)

file.close()