import object_detection_yolo as LP_detection
import Hawk_Eye_LP_recognition as LP_reco
from cv2 import imwrite
#Licence plate detection
LP_extracted,newImage,top=LP_detection.LP_detection()

#Licence plate recognition
final_img=LP_reco.LP_recognition(LP_extracted,newImage,top)

#Saving the final result
path_to_final_img="D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\final_image.jpg"
imwrite(path_to_final_img,final_img)
#showing result
#cv2.imshow("Finally You Win!!",final_img)
#cv2.waitKey(0)
print(path_to_final_img)

