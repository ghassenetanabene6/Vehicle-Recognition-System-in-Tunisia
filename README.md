# Vehicle-Recognition-System-in-Tunisia


This project is about developping a vehicle recognition system in Tunisia. It demonstrates the outcome of the summer internship (2 months) for second year students of the National School for Computer Sciences.

**Problem setting :**

The number of vehicles in the world is increasing rapidly every year, particularly in Tunisia. Therefore, several difficulties will be found to discover the vehicles identities when there is some problems such as parking violation enforcement, highway toll payment and also finding stolen cars. Added to that, it is impossible sometimes to identify the vehicle’s owner who escaped from authorities after causing an accident. This fact leads to develop an autonomous licence plate recognition system to identify vehicles and facilitate traffic management which is a popular and active research topic in the field of computer vision, image processing and intelligent transport systems.


**Main Goals :** 

This project aims to solve the problem of vehicle identification in Tunisia using Deep Learning models. To do that, our mission is to find a solution based on DL models and image processing to accomplish the following tasks :
- Detecting the presence of the vehicle’s licence plate.
- Image segmentation and extraction of the text written on the licence plate.
- Text classification with deep learning.
- Development of a desktop application (UI) using .Net

📍 **Keywords :** Python, Computer Vision, Deep Learning, Image segmentaton, Yolo, Faster-RCNN, Tensorflow, Keras, OpenCV, c# (.Net)  

📓 **Paper** : <a href="./Documentation/Report - Hawk Eye Tunisia - Vehicle Recognition System.pdf"> Report.pdf</a> or <a href="https://drive.google.com/file/d/1eu5EJU74HGsw568w4aWfh3WxRSMfUvvq/view?usp=sharing">Link</a>.
<hr>
### :round_pushpin: Requirements

```shell
!pip install -r Deep-Learning/requirements.txt
```

In the AI part of this project, we have : 

1- Vehicle license plate detection using Yolo :
The licence plate detection folder contains these necessary files : **lapi.weights , darknet-yolov3.cfg , classes.names**
which will be called by for the ```object_detection_yolo.py``` script.

2- Text segmentation

3- Character classification using deep learning model based on CNN architecture : 

After training our CNN model, the ```Deep-Learning/Main-Scripts/Hawk_Eye_LP_recognition.py``` script needs to import our saved model ```ocrmodel.h5```.

- The final script ```Deep-Learning/Main-Scripts/main_vehicle_to_LP.py``` use the previous scripts for the detection and classification of the tunisian LP.

We can run the main script with this command :

```shell
!python main_vehicle_to_LP.py --image=path
```
Where :
- **The input :** vehicle image 
- **The output :** path of the final image containing the result of the LP detection (green box) and a text showing the result of the LP recognition.
<hr>
<h3>Demo :</h3> 

<img src="./Documentation/Demo.gif">

<a href="https://drive.google.com/file/d/1-Hjc64SEU_dnliqNb6DL2Cib_bxoqrz5/view?usp=sharing"> video_demo.mp4</a>
<hr>
<h3>Screenshots :</h3>

📝 The user interface 
<img src="./Documentation/Screenshots/0.png">

<img src="./Documentation/Screenshots/1.png">

<img src="./Documentation/Screenshots/4.0.png">

<img src="./Documentation/Screenshots/4.1.png">


<hr>

📅 **Last Update On** : June 2020.


✉️ **Contact :**

email : ghassene.tanabene@gmail.com

linkedin : https://www.linkedin.com/in/ghassene-tanabene/
