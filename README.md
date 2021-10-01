# Traffic-Surveillance-System

Traffic surveillance systems have been around for quite a while across various cities worldwide. The ubiquitous presence of closed circuit cameras, vehicle plate detection systems and LED lane control lights has made traffic and incident management smooth and efficient. 

In a traffic management system, the surveillance component is the process in which data is collected in the field. This data is used to supply information about conditions in the field to other system components. Surveillance provides the information needed to perform the following functions:
      
      1. Measure traffic and environmental conditions. 
      2. Make control decisions. 
      3. Monitor system performance.

To build a custom object detection system with respect to traffic surveillance like vehicle classification, helmet detection, triple riding detection & number plate detection. So, the complete project aims at developing a model to classify the type of vehicles, helmet detection, number plate detection and triple riding detection.

# Flowchart:
![Untitled](https://user-images.githubusercontent.com/73810961/135345373-d5004c0c-b84a-4d5b-9c56-6a2131b107d5.png)

# Datasets:
Dataset collected by whole team members in real time from different states of India. The locations were selected in such a way that we can get a heterogenous traffic volume and varying traffic flow so that we can observe various categories of vehicles, large number of vehicles so that chances of getting such data set where it can be observed that traffic rules are violated like absence of number plate, helmet and triple riding cases. Also, we collected the dataset in different lighting condition, so that it can work in any lighting condition on real time.

We label the dataset with 6 classes.

      1. Car
      2. Bus
      3. Bike
      4. Auto
      5. Mgv
      6. Truck

![image](https://user-images.githubusercontent.com/73810961/135346376-477e321f-9d77-4776-8c85-1843616a80ab.jpg)

# Model and Training:
We use various types of model like YOLOV3, YOLOV3-tiny, YOLOV4, YOLOV4-tiny, YOLOV4 with Pytorch. For the final model we used **YOLOV3**. 

## How to use the Model
For model weights you have to train it on your own dataset and then use those weights in pipeline.py.

1. Git Clone

       git clone https://github.com/TeamEpicProjects/Traffic-Surveillance-System.git

      There are many folders in this repository, you only have to use **Pipeline** as it contains all the code you need to run the Traffic Surveillance System.


2. Requirement File download

      You need to install all required  libraries. 
      
       cd Pipeline
       Python install -r Req.txt

3. Weights, cfg and names file

      In pipeline.py file you have to give a path to your weights, cfg and names files from line number 51 to 63.
      
      After adding weights file, now you can run pipeline.py
      
       python pipeline.py
       
      In the terminal you will get output as 
      
      **Connected**
      
      **Running at localhost:5000**
      
      Now that your Code is running without any erros, you have to test if it is detecting any objects or not. For that we will use Postman.
      
      Go to the postman, select POST request and add **http://0.0.0.0/5000/image/**
      
      ![image](https://user-images.githubusercontent.com/63397654/135412532-4c64fdb1-a382-43a2-b6ab-2b8ac10c2f92.png)
      
      After seding request you will get output in JSON format which will contain Vehicle Type and Violation type.
      
4. Web Integration

      It's time to deploy the model on the web for that you have to open **Pipeline -> Web_Integration** Folder into seprate VS Code window and start **nodejs server**.
            
            npm install
            npm start
            
      ![image](https://user-images.githubusercontent.com/63397654/135413058-8253e1b0-b301-4086-ac59-eb1a8a306780.png)

