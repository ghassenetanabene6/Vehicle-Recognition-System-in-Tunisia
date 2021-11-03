from PIL import Image

from resizeimage import resizeimage
import cv2

hello= cv2.imread("./WISCONSIN.jpg")
dim=hello.shape
#print(size)
with open('3_true_plate.jpeg', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [dim[1], dim[0]])
        cover.save('a2.jpeg', image.format)
