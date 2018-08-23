# Final Project for CS50
# Converts text from picture to a string, which it
# will then add to a SQL database?

# Using tesseract and OpenCV
# code adapted from https://www.learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/

# This is essentially a wrapper around the command line tool for tesseract
# You first read the image using OpenCV then pass that into the pytesseract
import cv2
import sys
import pytesseract

def im2str(image):
    # Read image path from command line
    #imPath = "/Users/michaelyoung/Documents/Programming/CS50/Final_project/book1.jpg"
    # Unfortunately, Image must be in working directory to work
    imPath = image

    # Uncomment the line below to provide path to tesseract manually
    # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    # Define config parameters.
    # '-l eng'  for using the English language
    # '--oem 1' for using LSTM OCR Engine
    config = ('-l eng --oem 1 --psm 3')

    # Read image from disk
    im = cv2.imread(imPath, cv2.IMREAD_COLOR)

    # can't pass cv2 directly in I guess
    #img_new = "/Users/michaelyoung/Documents/Programming/CS50/Final_project/book1.jpg"

    # Not using OpenCV
    #image = Image.open(img_new)

    # Run tesseract OCR on image
    text = pytesseract.image_to_string(im, config=config)

    # return recognized text
    return text
