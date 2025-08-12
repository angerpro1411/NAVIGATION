import cv2


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







# Load image and convert to HSV
image = cv2.imread("15.png")
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Mouse callback function
def show_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_val = hsv_image[y, x]  # Note: image[y, x]
        print(f"HSV at ({x}, {y}): {hsv_val}")

# Display image and set mouse callback
cv2.imshow('HSV Image', hsv_image)
cv2.imshow("orginal", image)
cv2.setMouseCallback('HSV Image', show_hsv)

filtered_origin = backgr_removal(image)


cv2.imshow("filtered", filtered_origin)


cv2.waitKey(0)
cv2.destroyAllWindows()
