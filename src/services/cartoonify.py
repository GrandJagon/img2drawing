import cv2
import os
from cv2 import bitwise_not
from cv2 import imshow
import numpy as np
from PIL import Image



nbr_bilateral_filters = 50 

medianBlur = 13 
nbrLines = 90


def comicFromPath(img_path):
    # Edge detection
    img = cv2.imread(img_path)
    return comic(img)
    

def comic(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.medianBlur(gray, medianBlur) 
    edges = cv2.Canny(edges, 25, nbrLines, apertureSize=3) 

    # Fattens the edges
    kernel = np.ones((4,4), dtype=np.float)  / 12
    edges = cv2.filter2D(edges, 0, kernel)
    edges = cv2.threshold(edges, 50, 250, 0)[1]

    # Applies n filter to smooth the img
    for i in range(nbr_bilateral_filters):
        img = cv2.bilateralFilter(img, 9, 20, 10)

    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    shifted = cv2.pyrMeanShiftFiltering(img, 10, 20)

    cartoon =  cv2.subtract(shifted, edges)
    
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

    final_img = Image.fromarray(cartoon, 'RGB')
    
    return final_img


   


    