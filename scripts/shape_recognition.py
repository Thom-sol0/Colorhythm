import colorhythm.core.processing
import cv2

def extract_key_points(img1):
    akaze = cv2.AKAZE_create()
    kp, des = akaze.detectAndCompute(img1, None)
    return kp, des

image = cv2.imread('img.jpg')
kp1, des1 = extract_key_points(image)

print("Coordinates of the first keypoint of image1: ", kp1[0].pt)
print("Descriptor of the first keypoint of image1:\n", des1[0])


