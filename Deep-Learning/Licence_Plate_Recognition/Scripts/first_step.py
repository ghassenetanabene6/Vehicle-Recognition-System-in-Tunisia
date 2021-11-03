import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D
from tensorflow.keras import optimizers
import os

def create_folder(dirName):
    try:
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists") 

#    Match contours to licence plate or character template
def find_contours(dimensions, img,j,k,cc) :

    # Find all contours in the image
    cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Retrieve potential dimensions
    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]
    
    # Check largest 5 or  15 contours for license plate or character respectively
    cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:15]
    
    ii = cv2.imread('contour.jpg')
    
    x_cntr_list = []
    target_contours = []
    img_res = []
    for cntr in cntrs :
        #detects contour in binary image and returns the coordinates of rectangle enclosing it
        intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)
        
        #checking the dimensions of the contour to filter out the characters by contour's size
        if intWidth > lower_width and intWidth < upper_width and intHeight > lower_height and intHeight < upper_height :
            x_cntr_list.append(intX) #stores the x coordinate of the character's contour, to used later for indexing the contours

            char_copy = np.zeros((44,24))
            #extracting each character using the enclosing rectangle's coordinates.
            char = img[intY:intY+intHeight, intX:intX+intWidth]
            char = cv2.resize(char, (20, 40))
            
            cv2.rectangle(ii, (intX,intY), (intWidth+intX, intY+intHeight), (50,21,200), 2)
            plt.imshow(ii, cmap='gray')
            
            #             Make result formatted for classification: invert colors
            char = cv2.subtract(255, char)

            # Resize the image to 24x44 with black border
            char_copy[2:42, 2:22] = char
            char_copy[0:2, :] = 0
            char_copy[:, 0:2] = 0
            char_copy[42:44, :] = 0
            char_copy[:, 22:24] = 0

            img_res.append(char_copy) #List that stores the character's binary image (unsorted)
            
    #Return characters on ascending order with respect to the x-coordinate (most-left character first)
            
    #plt.show()
    
    #arbitrary function that stores sorted list of character indeces
    indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
    img_res_copy = []
    for idx in indices:
        img_res_copy.append(img_res[idx])# stores character images according to their index
    img_res = np.array(img_res_copy)

    return img_res
    
    
    
    
# Find characters in the resulting images
def segment_characters(image,j,k,cc) :

    # Preprocess cropped license plate image
    img_lp = cv2.resize(image, (333, 75))
    img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
    
    
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),image)
    #k+=1
    inc(cc,k)
    
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_lp)
    #k+=1
    inc(cc,k)
    
    plt.imshow(img_gray_lp, cmap='gray')
    #plt.show()
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_gray_lp)
    #k+=1
    inc(cc,k)
        
    _, img_binary_lp = cv2.threshold(img_gray_lp, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    plt.imshow(img_binary_lp, cmap='gray')
    #plt.show()
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_binary_lp)
    #k+=1
    inc(cc,k)
    
    img_binary_lp = cv2.erode(img_binary_lp, (3,3))
    
    plt.imshow(img_binary_lp, cmap='gray')
    #plt.show()
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_binary_lp)
    #k+=1
    inc(cc,k)
    
    img_binary_lp = cv2.dilate(img_binary_lp, (3,3))
    
    plt.imshow(img_binary_lp, cmap='gray')
    #plt.show()
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_binary_lp)
    #k+=1
    inc(cc,k)
    LP_WIDTH = img_binary_lp.shape[0]
    LP_HEIGHT = img_binary_lp.shape[1]

    # Make borders white
    img_binary_lp[0:3,:] = 255
    img_binary_lp[:,0:3] = 255
    img_binary_lp[72:75,:] = 255
    img_binary_lp[:,330:333] = 255
    plt.imshow(img_binary_lp, cmap='gray')
    #plt.show()
    
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_binary_lp)
    #k+=1
    inc(cc,k)

    # Estimations of character contours sizes of cropped license plates
    dimensions = [LP_WIDTH/6, LP_WIDTH/2, LP_HEIGHT/10, 2*LP_HEIGHT/3]
    plt.imshow(img_binary_lp, cmap='gray')
    #plt.show()
    cv2.imwrite('contour.jpg',img_binary_lp)
    cv2.imwrite('./first_step/plate{}/{}.jpg'.format(j,cc),img_binary_lp)
    #k+=1
    inc(cc,k)
	
    # Get contours within cropped license plate
    char_list = find_contours(dimensions, img_binary_lp,j,k,cc)

    return char_list    
    
    
model = tf.keras.models.load_model('ocrmodel.h5')   
    
def fix_dimension(img): 
  new_img = np.zeros((28,28,3))
  for i in range(3):
    new_img[:,:,i] = img
  return new_img
  
def show_results(char):
    dic = {}
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i,c in enumerate(characters):
        dic[i] = c

    output = []
    for i,ch in enumerate(char): #iterating over the characters
        img_ = cv2.resize(ch, (28,28))
        img = fix_dimension(img_)
        img = img.reshape(1,28,28,3) #preparing image for the model
        y_ = model.predict_classes(img)[0] #predicting the class
        character = dic[y_] #
        output.append(character) #storing the result in a list
        
    plate_number = ''.join(output)
    
    return plate_number

#print(show_results())    
    
def final_img(char,j,k,cc):
    plt.figure(figsize=(10,6))
    for i,ch in enumerate(char):
        img = cv2.resize(ch, (28,28))
        plt.subplot(3,4,i+1)
        plt.imshow(img,cmap='gray')
        plt.title(f'predicted: {show_results(char)[i]}')
        #plt.axis('off')
        plt.savefig('./first_step/plate{}/prediction_result{}.jpg'.format(j,k))
        #k+=1
        inc(cc,k)
    #plt.show()



k=0
j=1
cc="plate_"
def inc(cc,k):
    cc+="_{}".format(k)
    k+=1
#L=['car_plate.png','messigray.png','1_true_plate.JPG','3_true_plate.jpeg','GEORGIA.jpg','LOUISIANA.jpg','a.jpeg']
L=['car_plate.png','messigray.png']
for i in L:
    dirName="./first_step/plate{}".format(j)
    create_folder(dirName)
    img = cv2.imread(i)
    char = segment_characters(img,j,k,cc)
    final_img(char,j,k,cc)
    j+=1    
    cc+="plate_{}".format(j)
    k=0


#img = cv2.imread('messigray.png')   #No X ; 2=7
#img = cv2.imread('WISCONSIN.jpg')   #correct
#img = cv2.imread('1_true_plate.JPG')    #unknown ! dim or form or orientation
#img = cv2.imread('3_true_plate.jpeg')  #1 is only detected  
#img = cv2.imread('GEORGIA.jpg')   #D=0 ; 2=Z
#img = cv2.imread('LOUISIANA.jpg')   
#img = cv2.imread('a.jpeg') 
	
