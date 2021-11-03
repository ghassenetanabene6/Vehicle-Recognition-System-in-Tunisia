import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D
from tensorflow.keras import optimizers
import datetime


#tf.compat.v1.disable_v2_behavior() #not used in v1.1


#directory="/home/ghassenetanabene/Documents/solutions_existantes/work/Hawk_Eye/"
directory="D:/Hawk_Eye_version_1.0_LP_recog/Hawk_Eye_version_1.0_LP_recog/"

class stop_training_callback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('val_acc') > 0.992):
      self.model.stop_training = True
      
"""
!rm -rf logs
log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
"""     
def training():
	batch_size = 1
#callbacks = [tensorboard_callback, stop_training_callback()]
	model.fit_generator(
	      train_generator,
	      steps_per_epoch = train_generator.samples // batch_size,
	      validation_data = validation_generator, 
	      validation_steps = validation_generator.samples // batch_size,
	      epochs = 80) 
	model.save("ocrmodel.h5")
	print("Saved model to disk")
	     
def model_requirements():
	train_datagen = ImageDataGenerator(rescale=1./255, width_shift_range=0.1, height_shift_range=0.1)
	train_generator = train_datagen.flow_from_directory(
        directory+'Licence_Plate_Recognition/data/train',  # this is the target directory
        target_size=(28,28),  # all images will be resized to 28x28
        batch_size=1,
        class_mode='categorical')

	validation_generator = train_datagen.flow_from_directory(
        directory+'Licence_Plate_Recognition/data/val',  # this is the target directory
        target_size=(28,28),  # all images will be resized to 28x28        batch_size=1,
        class_mode='categorical')
        
       #creating model
	model = Sequential()
	model.add(Conv2D(32, (24,24), input_shape=(28, 28, 3), activation='relu', padding='same'))
	# model.add(Conv2D(32, (20,20), input_shape=(28, 28, 3), activation='relu', padding='same'))
	# model.add(Conv2D(32, (20,20), input_shape=(28, 28, 3), activation='relu', padding='same'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.4))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(11, activation='softmax'))

	model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=0.00001), metrics=['accuracy'])
def histogram_of_pixel_projection(img):
    """
    This method is responsible for licence plate segmentation with histogram of pixel projection approach
    :param img: input image
    :return: list of image, each one contain a digit
    """
    # list that will contains all digits
    caracrter_list_image = list()

    # img = crop(img)

    # Add black border to the image
    BLACK = [0, 0, 0]
    img = cv2.copyMakeBorder(img, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=BLACK)

    # change to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Change to numpy array format
    nb = np.array(gray)

    # Binarization
    nb[nb > 120] = 255
    nb[nb < 120] = 0

    # compute the sommation
    x_sum = cv2.reduce(nb, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
    y_sum = cv2.reduce(nb, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32S)

    # rotate the vector x_sum
    x_sum = x_sum.transpose()

    # get height and weight
    x = gray.shape[1]
    y = gray.shape[0]

    # division the result by height and weight
    x_sum = x_sum / y
    y_sum = y_sum / x

    # x_arr and y_arr are two vector weight and height to plot histogram projection properly
    x_arr = np.arange(x)
    y_arr = np.arange(y)

    # convert x_sum to numpy array
    z = np.array(x_sum)

    # convert y_arr to numpy array
    w = np.array(y_sum)

    # convert to zero small details
    z[z < 15] = 0
    z[z > 15] = 1

    # convert to zero small details and 1 for needed details
    w[w < 20] = 0
    w[w > 20] = 1

    # vertical segmentation
    test = z.transpose() * nb

    # horizontal segmentation
    test = w * test

    # plot histogram projection result using pyplot
    horizontal = plt.plot(w, y_arr)
    #plt.show()
    vertical = plt.plot(x_arr ,z)
    #plt.show()
    #plt.show(horizontal)
    #plt.show(vertical)

    f = 0
    ff = z[0]
    t1 = list()
    t2 = list()
    for i in range(z.size):
        if z[i] != ff:
            f += 1
            ff = z[i]
            t1.append(i)
    rect_h = np.array(t1)

    f = 0
    ff = w[0]
    for i in range(w.size):
        if w[i] != ff:
            f += 1
            ff = w[i]
            t2.append(i)
    rect_v = np.array(t2)

    # take the appropriate height
    rectv = []
    rectv.append(rect_v[0])
    rectv.append(rect_v[1])
    max = int(rect_v[1]) - int(rect_v[0])
    for i in range(len(rect_v) - 1):
        diff2 = int(rect_v[i + 1]) - int(rect_v[i])

        if diff2 > max:
            rectv[0] = rect_v[i]
            rectv[1] = rect_v[i + 1]
            max = diff2

    # extract caracter
    for i in range(len(rect_h) - 1):

        # eliminate slice that can't be a digit, a digit must have width bigger then 8
        diff1 = int(rect_h[i + 1]) - int(rect_h[i])

        if (diff1 > 5) and (z[rect_h[i]] == 1):
            # cutting nb (image) and adding each slice to the list caracrter_list_image
            caracrter_list_image.append(nb[int(rectv[0]):int(rectv[1]), rect_h[i]:rect_h[i + 1]])

            # draw rectangle on digits
            cv2.rectangle(img, (rect_h[i], rectv[0]), (rect_h[i + 1], rectv[1]), (0, 255, 0), 1)

    # Show segmentation result
    image = plt.imshow(img)
    #plt.show() ################################################################
    #plt.show(image)

    return caracrter_list_image


def show_segments(char):
    for i in range(len(char)):
	    #img=char[i]
	    #img=img.reshape(66,16)
	    plt.subplot(1, 10, i+1)
	    plt.imshow(char[i], cmap='gray')
	    plt.axis('off')
	    #print(char[i].shape)
    
def fix_dimension(img): 
  new_img = np.zeros((28,28,3))
  for i in range(3):
    new_img[:,:,i] = img
  return new_img
  
def show_results(char,model):
    dic = {}
    characters = '0123456789T'
    for i,c in enumerate(characters):
        dic[i]=c

    output = []
    for i,ch in enumerate(char): #iterating over the characters
        img_ = cv2.resize(ch, (28,28))
        img = fix_dimension(img_)
        img = img.reshape(1,28,28,3) #preparing image for the model
        y_ = model.predict_classes(img)[0] #predicting the class
        #print(y_)
        character = dic[y_] #
        if(character=="T"):
            output.append("Tunisie")
        else:
            output.append(character) #storing the result in a list
        
    plate_number = ''.join(output)
    #print(show_results())
    return(output)

    
def LP_recognition(img):
	#img = cv2.imread(LP_img)
	char=histogram_of_pixel_projection(img)
	model_requirements()
	model = tf.keras.models.load_model('D:/Hawk_Eye_version_1.0_LP_recog/Hawk_Eye_version_1.0_LP_recog/Licence_Plate_Recognition/ocrmodel.h5')
	show_segments(char)
	plt.figure(figsize=(10,6))
	#char=K[1]
	for i,ch in enumerate(char):
	    img = cv2.resize(ch, (28,28))
	    plt.subplot(3,4,i+1)
	    plt.imshow(img,cmap='gray')
	    plt.title(f'predicted: {show_results(char,model)[i]}')
	    plt.axis('off')
	    plt.savefig(directory+'prediction_result.jpg')

	output=show_results(char,model)
	print("The Tunisian Licence Plate is : "+' '.join(output))    
	#plt.show()

#LP_recognition("test.png")
