
from typing import final
from flask import Flask, jsonify, request, make_response, url_for, redirect 
from numpy.core.fromnumeric import shape
from gevent.pywsgi import WSGIServer
from PIL import Image
from utilname import yolo
from utilname import core
import numpy as np
import datetime
import matplotlib.pyplot as plt
import glob
import os
import cv2
import time
import imutils
import requests
import json
import uuid
import io
import requests 
import shutil 
import boto3
import sys

import uuid
from flask_cors import CORS, cross_origin
#######################################################################################################
port=5000
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

s3=boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIA5NRBQ6YAESL6BXXV',
    aws_secret_access_key='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'
)


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
########################################################################################################

plate_wgh_pth = resource_path(r'checkpoint\NUm_plate\yolov4_training_final.weights')
plate_cfg_pth = resource_path(r'checkpoint\NUm_plate\yolov4_training.cfg')
plate_label_pth = resource_path(r'checkpoint/NUm_plate/objplate.names')

# Vehicle Detection Checkpoint
vd_wgh_pth = resource_path(r'checkpoint/vehicleDetection/yolov4_vehicle_detection-288.weights')
vd_cfg_pth = resource_path(r'checkpoint/vehicleDetection/yolov4_vehicle_detection-288.cfg')
vd_label_pth =resource_path(r'checkpoint/vehicleDetection/yolov4_vehicle_detection-288.names')

# Helemet - Tripple Ridding Checkpoint
violation_wgh_pth = resource_path(r'checkpoint\helmat\yolov4-training-288-final_final.weights')
violation_cfg_pth = resource_path(r'checkpoint\helmat\yolov4-training-288.cfg')
violation_label_pth = resource_path(r'checkpoint\helmat\helmet-yolov4-288.names')

# Loading Plate Detection Model
platedetection = yolo.LoadYOLO(input_h=256, input_w=256, \
    labelPath=plate_label_pth, cfgPath=plate_cfg_pth, weightPath=plate_wgh_pth)
# Loading OCR Model
# Loading Vehicle Detection Model
vehicledetection = yolo.LoadYOLO(input_h=288, input_w=288, \
    labelPath=vd_label_pth, cfgPath=vd_cfg_pth, weightPath=vd_wgh_pth)
# Loading Helemet - Tripple Riddingn Model
helemt = yolo.LoadYOLO(input_h=288, input_w=288, \
    labelPath=violation_label_pth, cfgPath=violation_cfg_pth, weightPath=violation_wgh_pth)

#####################################################################################################################
@app.route('/',methods=['GET'])
def welcommessage():
    return 'Hello Welcome to the API Building'
@app.route('/image/',methods=['POST'])
def getimage():
    data=[]
   
    userid=''
    timsestamp=''
    withoutVehicle = False
    final_saved_data_in_firebase=[]
    outputdata=[]
    filestr=request.files['files']
    npimg=np.fromfile(filestr,np.uint8)
    frame=cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    unique_id = uuid.uuid1()
    var2 = str(unique_id)+str(time.time())+".jpg"
    def vehicle_detection(frame):
        outputvehicle = vehicledetection.detect(frame)
        vehicle_detail = []
        if type(outputvehicle)!=str:
            vehicle_detail = outputvehicle
            return vehicle_detail
        else:
            vehicle_detail.append([[None,None,None,None], "None Detected"])
            return vehicle_detail
    def num_plate_detection(frame):
        outputplate = platedetection.detect(frame)
        if type(outputplate)!=str:
            return outputplate
        else:
            return "None detected"    
    
    
    def two_wheeler_violations(frame,vehicle):
        try:
            outputdetect = helemt.detect(frame)
            violation=[]

            if type(outputdetect)!=str:
                violation = outputdetect
                return violation
            else:
                violation.append([])
                return violation 
        except Exception as e:
            print("error while detecting the two wheeler",e)
            return [] 
    
    
    def violation_check_box(detect_img):
        violation = []

        if vehicle_type == "bike":
            final_violation=two_wheeler_violations(detect_img,vehicle)
            try:
                for vio in final_violation:
                    cor = vio[0]
                    lab = vio[1]

                    if lab == "Helmet":
                        violation.append([cor,lab])

                    if lab == "No Helmet":
                        violation.append([cor,lab])

                    if lab == "Tripple Riding":
                        violation.append([cor,lab])
            except Exception as e:
                pass

            return violation
       
    vehicle_detail = vehicle_detection(frame)
    ocr_output = []
    file_names = []
    numplate_detail = num_plate_detection(frame)
    if type(numplate_detail)!=str:
            for i in numplate_detail:
                plate = i[0]
                if plate[0]>0 and plate[1]>0 and plate[2]>0 and plate[3]>0:
                    number = 'numberplate'
                    ocr_output.append([plate,number])
                else:
                    ocr_output.append([[0,0,0,0],"None detected"])
    vio_output = []
    # For violations
    if vehicle_detail != [[[None, None, None, None], 'None Detected']]:
        for j in vehicle_detail:
            vehicle = j[0]
            vehicle_type = j[1]
            violation="No violation"
            if vehicle_type=='bike':
                (x,y,w,h) = vehicle
                violation = violation_check_box(frame[y:y+h,x:x+w])
                vio_output.append([vehicle,vehicle_type,violation])
            if vehicle_type in ["car","truck","mgv","bus","auto"]:
                (x,y,w,h) = vehicle
                violation= violation_check_box(frame[y:y+h,x:x+w])
                vio_output.append([vehicle,vehicle_type,violation])
    final_output = []
    for vehicle,vehicle_type,violation in vio_output:
        fin = []
        fin.append(vehicle)
        fin.append(vehicle_type)
        if len(ocr_output)>0:
            for plate,number in ocr_output:
                if plate[0] > vehicle[0] and plate[0] < vehicle[0]+vehicle[2] and plate[1] > vehicle[1] and plate[1] < vehicle[1]+vehicle[3] and plate[0]+plate[2] > vehicle[0] and plate[0]+plate[2] < vehicle[0]+vehicle[2] and plate[1]+plate[3] > vehicle[1] and plate[1]+plate[3] < vehicle[1]+vehicle[3]:

                    fin.append(plate)
                    fin.append(number)

                    ocr_output.remove([plate,number])
                    break
        if len(fin)==2:
            fin.append([0,0,0,0])
            fin.append("None detected")
        fin.append(violation)
        final_output.append(fin)
    def save_output(final_outcome, frame):
        
        for vehicle_detail in final_outcome:
            vio_name=[]
            x,y,w,h = vehicle_detail[0]
            x_num,y_num,w_num,h_num = vehicle_detail[2]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(frame, vehicle_detail[1], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0,0,255), 2)
            cv2.rectangle(frame,(x_num,y_num),(x_num+w_num,y_num+h_num),(255,0,0),3)
            cv2.putText(frame, vehicle_detail[3], (x_num, y_num - 5), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0,0,255), 2)
            violation = vehicle_detail[4]

            if violation:
                for cor,name in violation:
                    x_vio, y_vio, w_vio, h_vio = cor
                    cv2.rectangle(frame,(x_vio+x,y_vio+y),(x_vio+x+w_vio,y_vio+h_vio+y),(0,255,0),3)
                    cv2.putText(frame, name, (x+x_vio, y+y_vio - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0,0,255), 2)
                    vio_name.append(name)
            else:
                vio_name = ['None']
            k='https://anprnumberplates.s3.us-east-2.amazonaws.com/'+var2
            temp_var={
                'Vehicle_Type':vehicle_detail[1],
                'Violation':vio_name,
               'Url': k
            }
            outputdata.append(temp_var)
        small = cv2.resize(frame, (0,0), fx=0.9, fy=0.9)
        cv2.imwrite(var2,small)  
        print(var2)
        file_names.append(var2)
        return outputdata
    data=save_output(final_output, frame)    
    result={"result":data}
    print(result)

    s3.Bucket('anprnumberplates').upload_file(Filename=var2,Key=var2)
    file_names.append(var2)
    print('Files is uploaded to S3')
    k='https://anprnumberplates.s3.us-east-2.amazonaws.com/'+var2
    return jsonify(result)

if __name__ == '__main__':
    print('Conneted')
    print('Running at localhost:5000')
    http_server = WSGIServer(("0.0.0.0",5000), app)
    http_server.serve_forever()