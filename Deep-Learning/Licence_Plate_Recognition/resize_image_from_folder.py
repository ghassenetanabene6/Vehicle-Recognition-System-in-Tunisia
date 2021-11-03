import cv2
import glob
from pathlib import Path

#path=Path("./tunisie")	
#path=path.glob("*.jpg")
#path = glob.glob("./tunisie/*.jpg")

def resize_images_in_folder():
	images=[]

	k,j=0,0
	#path = glob.glob("/home/ghassenetanabene/Documents/solutions_existantes/work/Hawk_Eye/Licence_Plate_Recognition/helloDAta/dataset/{}/*.jpg".format(k))
	while(k<10):
	    for imagepath in glob.glob("/home/ghassenetanabene/Documents/solutions_existantes/work/Hawk_Eye/Licence_Plate_Recognition/helloDAta/dataset/{}/*.jpg".format(k)):
		img=cv2.imread(str(imagepath))
		img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                         
		img=cv2.resize(img,(28,28))
		cv2.imwrite("/home/ghassenetanabene/Documents/solutions_existantes/work/Hawk_Eye/Licence_Plate_Recognition/data/train/class_{}/{}.jpg".format(k,j),img)
		images.append(img)
		j+=1
	    j=0
	    k+=1
        #print(images)
        

