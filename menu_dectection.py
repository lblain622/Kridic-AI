import cv2 as cv
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
from PIL import Image
####Setup####
useCamera = False

cap = cv.VideoCapture(0)


#helper functions
def scan_dectection(img,size,og_img):
    frame = cv.detailEnhance(img, sigma_s=20, sigma_r=0.15)
    #doc_contour = np.array([[0, 0], [width, 0], [width, height], [0, height]])
    imgGrey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGrey, (5, 5), 0)
    edges = cv.Canny(imgBlur, 100, 100) #find edges
    #cv.imshow("Edges", edges)
    kernal = np.ones((5, 5),np.uint8)
   
    dilate = cv.dilate(edges, kernal, iterations=1)
    #cv.imshow("Dilate", dilate)
    closing = cv.morphologyEx(dilate, cv.MORPH_CLOSE, kernal)
    #cv.imshow("Closing", closing)

    #_,threshold = cv.threshold(imgBlur, 100, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    #contours,_ = cv.findContours(threshold, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    contours,hire = cv.findContours(closing, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    max_area=0
    for c in contours:
        area = cv.contourArea(c)
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        if area> max_area and len(approx) == 4:
            points = np.squeeze(approx)
            max_area = area

          
            
    #draw contours
    cv.drawContours(img, [points], -1, (0, 255, 0), 3)
    #set points to orignal image
    multiplier = og_img.shape[1] / size[0]
    og_points = points * multiplier #resize points to orignal image
    og_points = og_points.astype(int)
    warp_img = four_point_transform(og_img, og_points)
    cv.imshow("Warp", warp_img)
    #cv.imshow("Frame", img)

#Resizing the frame/imaged based on width and set a aspect ratio
def resizer(frame,width=500):
    h,w,_ = frame.shape
    height=int((h/w)*width)
    size = (width,height)
    new_frame = cv.resize(frame,size)
    return new_frame,size

###Main####
while True:
    if useCamera:
        
        ret, frame = cap.read()
    else:
        frame = cv.imread("menu_1.jpg")

    
    cv.imshow("frame", frame)

    #new_frame, size = resizer(frame)
    #scan_dectection(new_frame,size,frame)
    pytesseract.image_to_string(Image.open("menu_1.jpg"))

    cv.imshow("Test", frame)



    if cv.waitKey(1) & 0xFF == ord('q'):
        break