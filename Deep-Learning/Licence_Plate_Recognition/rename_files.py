import os
import glob

def rename_images_in_folder():
	
	path0="/home/ghassenetanabene/Documents/solutions_existantes/work/Hawk_Eye/Licence_Plate_Recognition/data/train/"
	

	for dirname in os.listdir(path0):
	    if os.path.isdir(path0+dirname):
	        k=0
	        number_items=len(glob.glob("{}{}/*".format(path0,dirname)))
	        for i, filename in enumerate(os.listdir(path0+dirname)):
	            print(dirname,"\n")
	            os.rename(path0+dirname + "/" + filename, path0+dirname + "/"+dirname+"_" + str(k) + ".jpg")
	            k+=1
	        print(number_items==len(glob.glob("{}{}/*".format(path0,dirname))),"\n")

rename_images_in_folder()
