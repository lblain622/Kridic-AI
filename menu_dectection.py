import cv2 as cv
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
from PIL import Image
####Setup####
useCamera = False

cap = cv.VideoCapture(0)


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
    cv.imshow("Contours", img)
    #set points to orignal image
    multiplier = og_img.shape[1] / size[0]
    og_points = points * multiplier #resize points to orignal image
    og_points = og_points.astype(int)
    warp_img = four_point_transform(img, og_points)
    #cv.imshow("Warp", warp_img)
    #cv.imshow("Frame", img)

def resizer(frame,width=500):
    h,w,_ = frame.shape
    height=int((h/w)*width)
    size = (width,height)
    new_frame = cv.resize(frame,size)
    return new_frame,size

###Main####
def information_found(useCamera = False,imgPath = 'img\menu_1.jpg'):
    if useCamera:
        
        ret, frame = cap.read()
    else:
        frame = cv.imread(imgPath)

    frame,size = resizer(frame)    
    inverted = cv.bitwise_not(frame)
    grey = cv.cvtColor(inverted,cv.COLOR_BGR2GRAY)
    #scan_dectection(inverted,size,frame)
    #thresh,im_bw = cv.threshold(grey,0,255,cv.THRESH_BINARY|cv.THRESH_OTSU)
    #cv.imshow('frame',im_bw)
    cv.imshow('frame',grey)
    cv.imwrite('invert.jpg',inverted)

    
    
   
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    results = pytesseract.image_to_string(Image.open("invert.jpg"))
    return results
