from tensorflow.keras.models import load_model
from numpy import array, ones, zeros, arange, uint8
from cv2 import reduce,copyMakeBorder,BORDER_CONSTANT,CV_32S,REDUCE_SUM,COLOR_BGR2GRAY,cvtColor,rectangle,resize,addWeighted,putText,FONT_HERSHEY_DUPLEX,FONT_HERSHEY_SIMPLEX
#import matplotlib.pyplot as plt

directory="D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\"

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
    img = copyMakeBorder(img, 3, 3, 3, 3, BORDER_CONSTANT, value=BLACK)

    # change to gray
    gray = cvtColor(img, COLOR_BGR2GRAY)

    # Change to numpy array format
    nb = array(gray)

    # Binarization
    nb[nb > 120] = 255
    nb[nb < 120] = 0

    # compute the sommation
    x_sum = reduce(nb, 0, REDUCE_SUM, dtype=CV_32S)
    y_sum = reduce(nb, 1, REDUCE_SUM, dtype=CV_32S)

    # rotate the vector x_sum
    x_sum = x_sum.transpose()

    # get height and weight
    x = gray.shape[1]
    y = gray.shape[0]

    # division the result by height and weight
    x_sum = x_sum / y
    y_sum = y_sum / x

    # x_arr and y_arr are two vector weight and height to plot histogram projection properly
    x_arr = arange(x)
    y_arr = arange(y)

    # convert x_sum to numpy array
    z = array(x_sum)

    # convert y_arr to numpy array
    w = array(y_sum)

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
    #horizontal = plt.plot(w, y_arr)
    #plt.show()
    #vertical = plt.plot(x_arr ,z)
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
    rect_h = array(t1)

    f = 0
    ff = w[0]
    for i in range(w.size):
        if w[i] != ff:
            f += 1
            ff = w[i]
            t2.append(i)
    rect_v = array(t2)

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
            rectangle(img, (rect_h[i], rectv[0]), (rect_h[i + 1], rectv[1]), (0, 255, 0), 1)

    # Show segmentation result
    #image = plt.imshow(img)
    #plt.show() ################################################################
    #plt.show(image)

    return caracrter_list_image

"""
def show_segments(char):
    for i in range(len(char)):
	    #img=char[i]
	    #img=img.reshape(66,16)
	    plt.subplot(1, 10, i+1)
	    plt.imshow(char[i], cmap='gray')
	    plt.axis('off')
	    #print(char[i].shape)
"""  
def fix_dimension(img): 
  new_img = zeros((28,28,3))
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
        img_ = resize(ch, (28,28))
        img = fix_dimension(img_)
        img = img.reshape(1,28,28,3) #preparing image for the model
        y_ = model.predict_classes(img)[0] #predicting the class
        #print(y_)
        character = dic[y_] #
        if(character=="T"):
            output.append(" Tunisia ")
        else:
            output.append(character) #storing the result in a list
        
    plate_number = ''.join(output)
    #print(show_results())
    return(output)

def draw_text_on_image(img,title,text,x=150,y=250,w=500,h=100):

    # First we crop the sub-rect from the image
    #x, y, w, h = 150, 250, 500, 100
    sub_img = img[y:y+h, x:x+w]
    white_rect = ones(sub_img.shape, dtype=uint8) * 255

    res = addWeighted(sub_img, 0.6, white_rect, 0.5, 1.0)

    # Putting the image back to its position 
    img[y:y+h, x:x+w] = res
    cpy=img[y:y+h, x:x+w]
    putText(img[y:y+h, x:x+w],  
               title ,  
               (50, 50),  
               fontFace=FONT_HERSHEY_DUPLEX,  
               fontScale=1,  
               color=(128, 190, 82))   #0 100 150 26, 82, 118  


    font = FONT_HERSHEY_SIMPLEX 
    # Create a black image
    #img = np.zeros((512,512,3), np.uint8)
    #93, 173, 226
    putText(img[y:y+h, x:x+w],text,(50,80), font, 1,color=(118, 82, 26),thickness=2)
    return(img)
    #cv2.imshow("img",img)

def LP_recognition(img,newImg,top):
	#img = cv2.imread(LP_img)
	char=histogram_of_pixel_projection(img)
	#model_requirements()    #tf.keras.models.load_model
	model = load_model('D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\Licence_Plate_Recognition\\ocrmodel.h5')
	#show_segments(char)
	#plt.figure(figsize=(10,6))
	#char=K[1]
	'''
	for i,ch in enumerate(char):
	    img = cv2.resize(ch, (28,28))
	    plt.subplot(3,4,i+1)
	    plt.imshow(img,cmap='gray')
	    plt.title(f'predicted: {show_results(char,model)[i]}')
	    plt.axis('off')
	    plt.savefig(directory+'prediction_result.jpg')
        '''
	output=show_results(char,model)
	text=''.join(output)
	title="Licence Plate :"
	newImg_width=newImg.shape[1]
	newImg_height=newImg.shape[0]
	
	final_img=draw_text_on_image(newImg,title,text,newImg_width//2-200,top//2-50,newImg_width//2+25,100)
	return(final_img)
	#print("The Tunisian Licence Plate is : "+' '.join(output))    
	#plt.show()
