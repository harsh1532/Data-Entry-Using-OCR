import numpy as np
import imutils
import cv2

def align_images(image, template, maxFeatures=1000, keepPercent=0.2):
	# Converting both the input image and template image to Grayscale
	imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	# Using ORB to detect keypoints and extract descriptors
	orb = cv2.ORB_create(maxFeatures)
	(kpsA, descsA) = orb.detectAndCompute(imageGray, None)
	(kpsB, descsB) = orb.detectAndCompute(templateGray, None)
	# Matching the features
	method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
	matcher = cv2.DescriptorMatcher_create(method)
	matches = matcher.match(descsA, descsB, None)

	# Sorting the matches by their distance for keeping the best points
	matches = sorted(matches, key=lambda x: x.distance)
	keep = int(len(matches) * keepPercent)
	# print("No. of Best Matches:",keep)
	# if keep < 500:
	# 	print("####################################################################################")
	# 	print("Input Image is not similar to that of Template image\nPlease Check the template form")
	# 	exit()
	matches = matches[:keep]

	# Allocating memory for the keypoints (x, y) coordinates from the
	# top matches. We'll use these coordinates to compute our
	# homography matrix
	ptsA = np.zeros((len(matches), 2), dtype="float")
	ptsB = np.zeros((len(matches), 2), dtype="float")
	
	for (i, m) in enumerate(matches):
		ptsA[i] = kpsA[m.queryIdx].pt
		ptsB[i] = kpsB[m.trainIdx].pt

	# Computing the homography matrix between the two sets of matched points
	(H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
	# Getting the Height and Width of the template image
	(h, w) = template.shape[:2]
	aligned = cv2.warpPerspective(image, H, (w, h))
	# Return the Aligned image
	# aligned = imutils.resize(aligned, width = 550)
	# cv2.imshow("fd", aligned)
	# cv2.waitKey(0)
	return aligned