#!/usr/bin/env python

from PIL import Image
import argparse
import os
import cv2
import re


# Create arguments for my program
ap = argparse.ArgumentParser()
# Adding an image to be read argument
ap.add_argument("-f", "--folder", required=True, help="path to input folder with images to be processed")
# Adding an optional process argument. The default is threshold
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())

# Bump the filename by 1
check = 0

# Path to new folder for storing processed images
path = args["folder"] + "/" + "processed_pics"

# Create directory to put processed images in
try:
    os.mkdir(path)
except OSError:
    print(f"Creation of folder {path} failed")
else:
    print(f"Folder created at {path}")

# Open folder and perform operations on content
for img in os.listdir(args["folder"]):
    # Load the example image and convert it to grayscale
    image = cv2.imread(args["folder"]+"/"+img)
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        continue

    # Check to see if we should apply thresholding to preprocess the
    # image
    if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Make a check to see if median blurring should be done to remove
    # noise
    elif args["preprocess"] == "blur1":
        gray = cv2.medianBlur(gray, 1)
    elif args["preprocess"] == "blur3":
        gray = cv2.medianBlur(gray, 3)
    elif args["preprocess"] == "blur5":
        gray = cv2.medianBlur(gray, 5)
    elif  args["preprocess"] == "blur9":
        gray = cv2.medianBlur(gray, 9)

    # TODO: Tweak the blurring
    # Or should gaussian blur be performed
    elif args["preprocess"] == "gaus":
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Write the grayscale image to disk as a temporary file so we can
    # apply OCR to it

    filename = f"{format(os.getpid()+check)}.png"
    check += 1
    cv2.imwrite(path + "/" + filename, gray)

# TODO: Make "every" read photo OCR'able
