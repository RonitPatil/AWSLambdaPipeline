import boto3
import json
import subprocess
import os

import os
import imutils
import cv2
import json
from PIL import Image, ImageDraw, ImageFont
from facenet_pytorch import MTCNN, InceptionResnetV1
from shutil import rmtree
import numpy as np
import torch
import boto3
import tempfile

#handler code
def handler(event, context):
    client = boto3.client('s3')
    print("Event:", json.dumps(event))

    #get bucket name and key
    bucketName = event['bucket_name']
    key = event['image_file_name']
    
    #download image form s3
    download_path = f'/tmp/{key}'
    client.download_file(bucketName, key, download_path)

    # script_path = '/home/app/face-recognition-code.py' 

    # command = ['python', script_path, download_path]
    
    try:
        #call function with download path
        recognized_name = face_recognition_function(download_path)
        print("Recognition Output:", recognized_name)

    except Exception as e:
        print("Error during face recognition:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Error in face recognition process')
        }

    #save results
    outputBucket = '1230531746-output'
    outputKey = key.replace('.jpg', '.txt')
    client.put_object(Bucket=outputBucket, Key=outputKey, Body=recognized_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Face recognition completed successfully')
    }


tempfile.tempdir = "/tmp"

os.environ['TORCH_HOME'] = '/tmp/torch'
#face recognition code as provided
mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # initializing mtcnn for face detection
resnet = InceptionResnetV1(pretrained='vggface2').eval() # initializing resnet for face img to embeding conversion
print("Face recognition function has started ")
def face_recognition_function(key_path):
    # Face extraction
    img = cv2.imread(key_path, cv2.IMREAD_COLOR)
    boxes, _ = mtcnn.detect(img)

    # Face recognition
    key = os.path.splitext(os.path.basename(key_path))[0].split(".")[0]
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    face, prob = mtcnn(img, return_prob=True, save_path=None)
    saved_data = torch.load('data.pt')  # loading data.pt file
    if face != None:
        emb = resnet(face.unsqueeze(0)).detach()  # detech is to make required gradient false
        embedding_list = saved_data[0]  # getting embedding data
        name_list = saved_data[1]  # getting list of names
        dist_list = []  # list of matched distances, minimum distance is used to identify the person
        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)
        idx_min = dist_list.index(min(dist_list))
        print(f"Face recognised as {name_list[idx_min]}")

        # Save the result name in a file
        with open("/tmp/" + key + ".txt", 'w+') as f:
            f.write(name_list[idx_min])
        return name_list[idx_min]
        
    else:
        print(f"No face is detected")
    return
