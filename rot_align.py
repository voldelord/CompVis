import cv2
import os
import glob
import numpy as np
import progressbar
from multiprocessing import Pool

def correlation(image1, image2):
    res = cv2.matchTemplate(image1, image2, cv2.TM_CCORR_NORMED)
    return res[0,0];


def angle_offset(image1, image2):
	maxCor = -1
	bestRot = 0

	for angle in progressbar.progressbar(range(-5,6)):
		(h, w) = image1.shape[:2];
		M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0) 
		rotated = cv2.warpAffine(image1, M, (h, w)) 

		corr = correlation(rotated, image2)

		if corr > maxCor:
			maxCor = corr
			bestRot = angle
			
	return bestRot;

if __name__ == "__main__":
	aligned_imgs = glob.glob('output_translation_aligned/' +'*.png',recursive=True)
	aligned_imgs.sort()
	aligned_imgs = aligned_imgs[:10]

	try:  
	    os.mkdir("output_rotation_aligned")
	except:
		pass

	previous = cv2.imread(aligned_imgs[0], 0);
	previous_angle = 0;
	cv2.imwrite("output_rotation_aligned/frame_0.png",cv2.imread(aligned_imgs[0],cv2.IMREAD_COLOR))
	for idx, file in enumerate(aligned_imgs[1:]):
		print("Aligning image " + str(idx + 1))
		current = cv2.imread(file, 0);
		angle = angle_offset(previous, current)
		previous = current

		img = cv2.imread(file, cv2.IMREAD_COLOR)
		(h, w) = img.shape[:2];
		M = cv2.getRotationMatrix2D((w / 2, h / 2), previous_angle + angle, 1.0)
		adjusted_img = cv2.warpAffine(img, M, (h, w)) 
		cv2.imwrite("output_rotation_aligned/frame_" + str(idx + 1) +".png",adjusted_img)

		previous_angle += angle

		print (previous_angle)

