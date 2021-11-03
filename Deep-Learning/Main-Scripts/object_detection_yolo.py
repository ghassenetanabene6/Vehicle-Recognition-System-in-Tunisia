import argparse
import sys
from numpy import argmax,uint8
import os.path
from cv2.dnn import readNetFromDarknet,DNN_BACKEND_OPENCV,DNN_TARGET_CPU,NMSBoxes,blobFromImage
from cv2 import imwrite,rectangle,FILLED,putText,FONT_HERSHEY_SIMPLEX,getTextSize,VideoCapture,VideoWriter,VideoWriter_fourcc,CAP_PROP_FRAME_WIDTH,waitKey,getTickFrequency

# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4  #Non-maximum suppression threshold

inpWidth = 416  #608     #Width of network's input image
inpHeight = 416 #608     #Height of network's input image

directory="D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\"
parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
parser.add_argument('--image', help='Path to image file.')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

# Load names of classes
classesFile = "D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\Licence_plate_detection\\classes.names";

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.

modelConfiguration = "D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\Licence_plate_detection\\darknet-yolov3.cfg";
modelWeights = "D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\Licence_plate_detection\\lapi.weights";

net = readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(DNN_BACKEND_OPENCV)
net.setPreferableTarget(DNN_TARGET_CPU)

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom,frame):
    # Draw a bounding box.
    #    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    global LP_extracted
    LP_extracted=frame[top+6:bottom-6, left+6:right-6]
    imwrite(directory+"Licence_Plate_extracted.jpg",LP_extracted)     	#extracting the licence plate
    
    rectangle(frame, (left, top), (right, bottom), (128, 190, 82), 3) #141, 214, 88
    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])

    rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (128, 190, 82), FILLED)
    #cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine),    (255, 255, 255), cv.FILLED)
    putText(frame, label, (left, top), FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 2)
    #return(LP_extracted)

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        #print("out.shape : ", out.shape)
        for detection in out:
            #if detection[4]>0.001:
            scores = detection[5:]
            classId = argmax(scores)
            #if scores[classId]>confThreshold:
            confidence = scores[classId]
            #if detection[4]>confThreshold:
                #print(detection[4], " - ", scores[classId], " - th : ", confThreshold)
                #print(detection)
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height,frame)
        #PLicence=drawPred(classIds[i], confidences[i], left, top, left + width, top + height,frame)
    return(top) #added to know where we will put the text in the final image

def LP_detection():
	#LP_extracted=""
	# Process inputs
	#winName = 'Deep learning object detection in OpenCV'
	#cv.namedWindow(winName, cv.WINDOW_NORMAL)

	outputFile = "yolo_out_py.avi"
	if (args.image):
	    # Open the image file
	    if not os.path.isfile(args.image):
	    	#print("Input image file ", args.image, " doesn't exist")
	    	sys.exit(1)
	    cap = VideoCapture(args.image)
	    outputFile = args.image[:-4]+'_yolo_out_py.jpg'
	    hasFrame, frame = cap.read()
	    	    # Create a 4D blob from a frame. 
	    blob = blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

	    # Sets the input to the network
	    net.setInput(blob)

	    # Runs the forward pass to get output of the output layers
	    outs = net.forward(getOutputsNames(net))

	    # Remove the bounding boxes with low confidence
	    #postprocess(frame, outs)

	    top=postprocess(frame, outs)

	    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
	    t, _ = net.getPerfProfile()
	    label = 'Inference time: %.2f ms' % (t * 1000.0 / getTickFrequency())
	    #cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))


	    return LP_extracted ,frame.astype(uint8),top
	else: return(None)

"""
	elif (args.video):
	    # Open the video file
	    if not os.path.isfile(args.video):
	    	#print("Input video file ", args.video, " doesn't exist")
	    	sys.exit(1)
	    cap = VideoCapture(args.video)
	    outputFile = args.video[:-4]+'_yolo_out_py.avi'
	else:
	    # Webcam input
	    cap = VideoCapture(0)

	# Get the video writer initialized to save the output video
	if (not args.image):
	    vid_writer = VideoWriter(directory+outputFile, VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(CAP_PROP_FRAME_WIDTH)),round(cap.get(CAP_PROP_FRAME_HEIGHT))))
        
	while waitKey(1) < 0:

	    # get frame from the video
	    hasFrame, frame = cap.read()

	    # Stop the program if reached end of video
	    if not hasFrame:
	    	#print("Done processing !!!")
	    	#print("Output file is stored as ", outputFile)
	    	#cv.waitKey(3000)
	    	break

	    # Create a 4D blob from a frame. 
	    blob = blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

	    # Sets the input to the network
	    net.setInput(blob)

	    # Runs the forward pass to get output of the output layers
	    outs = net.forward(getOutputsNames(net))

	    # Remove the bounding boxes with low confidence
	    #postprocess(frame, outs)

	    top=postprocess(frame, outs)

	    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
	    t, _ = net.getPerfProfile()
	    label = 'Inference time: %.2f ms' % (t * 1000.0 / getTickFrequency())
	    #cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

	    # Write the frame with the detection boxes
	    if (args.image):
	    	#cv.imwrite(directory+outputFile, frame.astype(np.uint8))
	    	return LP_extracted ,frame.astype(uint8),top
	    else:
	    	vid_writer.write(directory+frame.astype(uint8))
	return(LP_extracted,top)
"""
#LP_extracted ,a,top=LP_detection()
#print(LP_extracted,a,top)
