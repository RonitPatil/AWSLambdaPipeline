# Use a slim version of Python 3.8 as the base image
ARG RUNTIME_VERSION="3.8"
ARG DISTRO_VERSION="3.12"
ARG FUNCTION_DIR="/home/app/"

FROM alpine:latest
FROM python:${RUNTIME_VERSION} AS python-alpine

RUN python${RUNTIME_VERSION} -m pip install --upgrade pip

FROM python-alpine AS build-image

ARG FUNCTION_DIR
ARG RUNTIME_VERSION

RUN mkdir -p ${FUNCTION_DIR}

RUN mkdir -p /home/app/model/checkpoints && \
    chmod -R 777 /home/app/model

ENV FVCHECKPOINT=/home/app/model/checkpoints

RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}
FROM python-alpine
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
RUN pip install --no-cache-dir facenet-pytorch --no-deps

# Install PyTorch, torchvision, and torchaudio with CPU-only builds
RUN pip install \
    torch==1.10.2+cpu \
    torchvision==0.11.3+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY requirements.txt ${FUNCTION_DIR}

RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}
COPY entry.sh /

# Copy the Python script
# COPY face-recognition-code.py ${FUNCTION_DIR}
COPY data.pt ${FUNCTION_DIR}

# Copy function code
COPY handler.py ${FUNCTION_DIR}
RUN chmod 777 /entry.sh

ENTRYPOINT [ "/entry.sh" ]
# Set the CMD to your handler (assuming the use of AWS Lambda RIE for local testing)
CMD ["handler.handler"]
