# Elastic Video Analysis Application Using AWS PaaS

## Overview
This project involves developing an elastic video analysis application using AWS Platform as a Service (PaaS) resources. The application processes videos to recognize faces, leveraging AWS Lambda and other supporting services. The project aims to implement a scalable and cost-effective cloud solution.

## Project Description
The project consists of a multi-stage pipeline to process videos using AWS Lambda functions. The pipeline includes the following stages:

1. **Video Upload**: Users upload videos to an input S3 bucket.
2. **Stage 1 - Video Splitting**: A Lambda function splits the video into frames and stores them in an intermediate S3 bucket.
3. **Stage 2 - Face Recognition**: Another Lambda function extracts faces from the frames using a pre-trained deep learning model and stores the results in an output S3 bucket.

## Key Features
- **Serverless Architecture**: Utilizes AWS Lambda for processing, eliminating the need for managing servers.
- **Scalable Processing**: Automatically scales out and in based on the video upload demand.
- **Efficient Storage**: Uses S3 buckets to store videos, frames, and recognition results.

## How It Works
1. Users upload videos to the input S3 bucket.
2. The video-splitting Lambda function is triggered, which processes the video and stores frames in the intermediate S3 bucket.
3. The face-recognition Lambda function is then triggered to process the frames, recognize faces, and store the results in the output S3 bucket.

This architecture ensures a highly scalable and efficient video analysis application leveraging AWS PaaS services.
