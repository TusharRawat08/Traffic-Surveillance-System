import cv2
import numpy as np
import os

class LoadYOLO():
    def __init__(self, labelPath, cfgPath, weightPath, input_w, input_h, threshold=0.5):
        self.labels = open(labelPath).read().strip().split("\n")
        
        # initialize a list of colors to represent each possible class label
        np.random.seed(69)
        #self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")
        self.net = cv2.dnn.readNetFromDarknet(
            cfgPath, weightPath
        )
        self.output_layers_names = self.net.getUnconnectedOutLayersNames()
        self.threshold = threshold
        self.input_w = input_w
        self.input_h = input_h

    def detect(self, imPlate):

        #self.image = cv2.imread(imPlate)
        self.image = imPlate
        (self.H, self.W) = self.image.shape[:2]

        self.blob = cv2.dnn.blobFromImage(
            self.image, 1/255., (self.input_w,self.input_h),
            swapRB=True, crop=False
        )
		# construct a blob from the input image and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes and
		# associated probabilities
        self.net.setInput(self.blob)
        self.layerOutputs = self.net.forward(self.output_layers_names)

        return self.process_output(self.layerOutputs)

    def process_output(self, layerOutputs):
		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        #loop over layer outputs
        for output in layerOutputs:
            #lopp over each detection 
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence>self.threshold:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[:4] * np.array([self.W, self.H, self.W, self.H])
                    (centerX, centerY, width, height) = box.astype("int")
                    
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width/2))
                    y = int(centerY - (height/2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.threshold, 0.3)
        bboxes = []
        outlabels = []
        
        # ensure at least one detection exists
        if len(indexes)>0:
            for i in indexes.flatten():
                # extract the bounding box coordinates
                
                for k in range(len(boxes[i])):
                    if boxes[i][k]<0:
                        boxes[i][k]=0

                x,y,w,h = boxes[i] 

                H,W = self.image.shape[:2]
                if x+w>W and x>0 and w>0:
                    wid = W-(x+w)
                    if x>w:
                        x += wid
                    else:
                        w +=wid

                if y+h>H and y>0 and h>0:
                    wid = H-(y+h)
                    if y>h:
                        y += wid
                    else:
                        h +=wid

                label = f"{self.labels[classIDs[i]]}"
                confidence = str(round(confidences[i], 3))
                
                bboxes.append([x,y,w,h])
                outlabels.append(label)

            return list(zip(bboxes, outlabels))
        else:
            return 'None Detected'

    
