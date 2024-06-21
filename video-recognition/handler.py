#__copyright__   = "Copyright 2024, VISA Lab"
#__license__     = "MIT"

import subprocess
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('lambda')
    s3 = boto3.client('s3')

    # print(f"Hello the event is {event}")
    
    #get details
    bucketName = event['Records'][0]['s3']['bucket']['name']
    videoKey = event['Records'][0]['s3']['object']['key']
    
    download_path = f'/tmp/{videoKey}'
    #download file from bucket
    s3.download_file(bucketName, videoKey, download_path)
    
    #get frame key
    frameKey = videoKey.split('.')[0] + '.jpg'
    upload_path = f'/tmp/{frameKey}'
    
    #run subprocess to extract framed
    try:
        subprocess.call(['ffmpeg', '-i', download_path, '-vframes', '1', upload_path])
        print(f"Extracted frame stored at {upload_path}")
    #incase it fails
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract frame: {e}")
        return {
            'statusCode': 500,
            'body': f"Error extracting frame: {e}"
        }
    
    #stage 1 bucket
    stage_1_bucket = '1230531746-stage-1'  
    #upload the file
    s3.upload_file(upload_path, stage_1_bucket, frameKey)
    print(f"Uploaded frame {frameKey} to {stage_1_bucket}")

    #send payload as asked
    payload = {
        'bucket_name': stage_1_bucket,
        'image_file_name': frameKey
    }

    #invoke next lambda func
    resp = client.invoke(
        FunctionName='face-recognition',  
        InvocationType='Event',  
        Payload=json.dumps(payload)
    )
    
    return {
        'statusCode': 200,
        'body': f"Successfully processed {videoKey} and uploaded frame to {stage_1_bucket}"
    }

