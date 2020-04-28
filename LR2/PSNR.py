import cv2

img1 = cv2.imread("grey.bmp")
img2 = cv2.imread("result.bmp")
psnr = round((cv2.PSNR(img1, img2)), 5)

print('PSNR = ', psnr)


# MSE is zero means no noise is present in the signal . 
# Therefore PSNR have no importance. 
