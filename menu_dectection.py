import cv2 as cv
import numpy as np 
from utlis import *
##########Settings #########################
useCamera = False
camera = cv.VideoCapture()
ImgPath ="img\menu_1.jpg"

heightImg = 640
widthImg = 480
###########################################

while True:
    imgBlank = np.zeros((heightImg, widthImg), np.uint8) #for testing
    if useCamera:
        success, img = camera.read()
    else:
        img = cv.imread(ImgPath)
    img = cv.resize(img, (widthImg, heightImg))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5,5), 1)
    #thresholds = utlis.valTrackbars() #get bar values for thesfolds
    #kernel = np.ones((5,5))
    #imgDialed = cv.dilate(thresholds,kernel,iterations=2) #applying dialations
    #imgThreshold = cv.erode(imgDialed, kernel, iterations=1) #applying edorsions



    imgArray= ([img, imgGray,imgBlank, imgBlank],[imgBlank, imgBlank, imgBlank, imgBlank])
    labels = [["Original", "Gray", "Dialated", "Threshold"], ["Contours", "Warp", "Warp Gray", "Warp Threshold"]]
    stackedImage = stackImages( 0.75,imgArray)
    cv.imshow("Result", stackedImage)