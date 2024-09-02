import cv2 as cv
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
from PIL import Image


useCamera = False
def resizer(frame,width=500):
    h,w,_ = frame.shape
    height=int((h/w)*width)
    size = (width,height)
    new_frame = cv.resize(frame,size)
    return new_frame,size

def information_found( imgPath):
    
    frame = cv.imread(imgPath)
    if frame is None:
        print("Failed to read image from path")
        return None
    frame, size = resizer(frame)
    cv.imwrite('menu.jpg', frame)
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

    results = pytesseract.image_to_string(frame)

    return results

